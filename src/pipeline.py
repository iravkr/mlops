from prefect import flow, task
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from training.train import ModelTrainer
from data_processing.audio_processor import AudioProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@task
def process_data():
    logger.info("Processing audio data...")
    processor = AudioProcessor()
    data_dir = "data/audio_files"
    
    if not os.path.exists(data_dir):
        logger.error(f"Data directory {data_dir} not found")
        return None
    
    return processor.prepare_data(data_dir)


@task
def train_model(data):
    if data is None:
        logger.error("No data provided for training")
        return None
        
    X_train, X_test, y_train, y_test, le = data
    logger.info("Training model...")
    
    trainer = ModelTrainer()
    model, accuracy = trainer.train_model(X_train, y_train, X_test, y_test)
    trainer.save_model(model, le)
    
    return model, accuracy


@task
def monitor_model():
    logger.info("Running model monitoring...")
    from monitoring.monitor import simulate_monitoring
    drift_detected, drift_score = simulate_monitoring()
    
    if drift_detected:
        logger.warning("Model retraining recommended due to data drift")
    
    return drift_detected


@flow(name="ml_pipeline")
def ml_pipeline():
    logger.info("Starting ML pipeline...")
    
    data = process_data()
    model_result = train_model(data)
    drift_detected = monitor_model()
    
    if model_result:
        model, accuracy = model_result
        logger.info(f"Pipeline completed. Model accuracy: {accuracy:.4f}")
    else:
        logger.error("Pipeline failed during training")
    
    return {"drift_detected": drift_detected, "model_trained": model_result is not None}


if __name__ == "__main__":
    result = ml_pipeline()
    logger.info(f"Pipeline result: {result}")
