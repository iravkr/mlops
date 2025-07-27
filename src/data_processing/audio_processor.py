import os
import pandas as pd
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioProcessor:
    def __init__(self, sample_rate=22050, duration=3):
        self.sample_rate = sample_rate
        self.duration = duration

    def extract_features(self, file_path):
        try:
            audio, _ = librosa.load(file_path, sr=self.sample_rate, duration=self.duration)
            
            mfccs = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=13)
            mfccs_mean = np.mean(mfccs.T, axis=0)
            
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)
            spectral_centroid_mean = np.mean(spectral_centroid)
            
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)
            zcr_mean = np.mean(zero_crossing_rate)
            
            features = np.concatenate([mfccs_mean, [spectral_centroid_mean, zcr_mean]])
            return features
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None

    def process_dataset(self, data_dir, csv_file=None):
        features = []
        labels = []
        
        if csv_file and os.path.exists(csv_file):
            # Use CSV file for labels (Kaggle dataset format)
            import pandas as pd
            df = pd.read_csv(csv_file)
            
            for _, row in df.iterrows():
                filename = row['Filename']
                label = row['Class']
                file_path = os.path.join(data_dir, filename)
                
                if os.path.exists(file_path):
                    feature = self.extract_features(file_path)
                    if feature is not None:
                        features.append(feature)
                        labels.append(label)
                else:
                    logger.warning(f"Audio file not found: {file_path}")
        else:
            # Use directory structure for labels (original format)
            for emotion_dir in os.listdir(data_dir):
                emotion_path = os.path.join(data_dir, emotion_dir)
                if not os.path.isdir(emotion_path):
                    continue
                    
                for audio_file in os.listdir(emotion_path):
                    if audio_file.endswith('.wav'):
                        file_path = os.path.join(emotion_path, audio_file)
                        feature = self.extract_features(file_path)
                        
                        if feature is not None:
                            features.append(feature)
                            labels.append(emotion_dir)
        
        return np.array(features), np.array(labels)

    def prepare_data(self, data_dir, csv_file=None, test_size=0.3):
        X, y = self.process_dataset(data_dir, csv_file)
        
        if len(X) == 0:
            raise ValueError("No audio data found")
        
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        # Check if we have enough data for stratified split
        unique_classes, class_counts = np.unique(y_encoded, return_counts=True)
        min_class_count = min(class_counts)
        
        if min_class_count < 2:
            logger.warning("Not enough samples per class for stratified split, using random split")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=test_size, random_state=42
            )
        else:
            # Adjust test_size if needed to ensure at least 1 sample per class in test set
            min_test_size = len(unique_classes) / len(X)
            actual_test_size = max(test_size, min_test_size)
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=actual_test_size, random_state=42, stratify=y_encoded
            )
        
        logger.info(f"Data split: {len(X_train)} training, {len(X_test)} testing samples")
        logger.info(f"Classes: {le.classes_}")
        
        return X_train, X_test, y_train, y_test, le
