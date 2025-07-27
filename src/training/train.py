import os
import sys
import pickle
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import logging

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.audio_processor import AudioProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    def __init__(self, experiment_name="audio_sentiment"):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)

    def train_model(self, X_train, y_train, X_test, y_test):
        with mlflow.start_run():
            model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 10)
            mlflow.log_metric("accuracy", accuracy)
            
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name="sentiment_classifier"
            )
            
            logger.info(f"Model accuracy: {accuracy:.4f}")
            logger.info(f"Classification report:\n{classification_report(y_test, y_pred)}")
            
            return model, accuracy

    def save_model(self, model, label_encoder, model_path="models"):
        os.makedirs(model_path, exist_ok=True)
        
        with open(f"{model_path}/model.pkl", "wb") as f:
            pickle.dump(model, f)
            
        with open(f"{model_path}/label_encoder.pkl", "wb") as f:
            pickle.dump(label_encoder, f)
            
        logger.info(f"Model saved to {model_path}")


def main():
    # Get the project root directory (two levels up from this file)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    train_data_dir = os.path.join(project_root, "data", "TRAIN")
    train_csv_file = os.path.join(project_root, "data", "TRAIN.csv")
    
    if not os.path.exists(train_data_dir):
        logger.error(f"Training data directory {train_data_dir} not found")
        return
        
    if not os.path.exists(train_csv_file):
        logger.error(f"Training CSV file {train_csv_file} not found")
        return
    
    processor = AudioProcessor()
    X_train, X_test, y_train, y_test, le = processor.prepare_data(train_data_dir, train_csv_file)
    
    trainer = ModelTrainer()
    model, accuracy = trainer.train_model(X_train, y_train, X_test, y_test)
    
    # Save model in project root models directory
    model_path = os.path.join(project_root, "models")
    trainer.save_model(model, le, model_path)


if __name__ == "__main__":
    main()
