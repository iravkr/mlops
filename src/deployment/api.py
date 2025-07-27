import pickle
import numpy as np
from fastapi import FastAPI, UploadFile, File
import librosa
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Audio Sentiment API")

model = None
label_encoder = None


def load_model():
    global model, label_encoder
    try:
        with open("models/model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("models/label_encoder.pkl", "rb") as f:
            label_encoder = pickle.load(f)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Error loading model: {e}")


@app.on_event("startup")
async def startup_event():
    load_model()


@app.post("/predict")
async def predict_sentiment(file: UploadFile = File(...)):
    if model is None or label_encoder is None:
        return {"error": "Model not loaded"}
    
    try:
        audio_data = await file.read()
        
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data)
        
        audio, _ = librosa.load("temp_audio.wav", sr=22050, duration=3)
        
        mfccs = librosa.feature.mfcc(y=audio, sr=22050, n_mfcc=13)
        mfccs_mean = np.mean(mfccs.T, axis=0)
        
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=22050)
        spectral_centroid_mean = np.mean(spectral_centroid)
        
        zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)
        zcr_mean = np.mean(zero_crossing_rate)
        
        features = np.concatenate([mfccs_mean, [spectral_centroid_mean, zcr_mean]])
        features = features.reshape(1, -1)
        
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].max()
        
        sentiment = label_encoder.inverse_transform([prediction])[0]
        
        import os
        os.remove("temp_audio.wav")
        
        return {
            "sentiment": sentiment,
            "confidence": float(probability)
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return {"error": str(e)}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
