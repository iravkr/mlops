import sys
import os
import numpy as np
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processing.audio_processor import AudioProcessor


class TestAudioProcessor:
    def setup_method(self):
        self.processor = AudioProcessor()
    
    def test_extract_features_shape(self):
        # Create a dummy audio file for testing
        sample_rate = 22050
        duration = 3
        dummy_audio = np.random.randn(sample_rate * duration)
        
        # Save as temporary file
        import soundfile as sf
        temp_file = "test_audio.wav"
        sf.write(temp_file, dummy_audio, sample_rate)
        
        try:
            features = self.processor.extract_features(temp_file)
            assert features is not None
            assert len(features) == 15  # 13 MFCCs + 2 other features
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_invalid_file_path(self):
        features = self.processor.extract_features("nonexistent_file.wav")
        assert features is None
    
    def test_processor_initialization(self):
        assert self.processor.sample_rate == 22050
        assert self.processor.duration == 3
