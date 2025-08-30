from src.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME
import os 
import sys
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def predict(self, X):
        try:
            logging.info("Predicting target variable")
            X_transform = self.preprocessor.transform(X)
            y_pred = self.model.predict(X_transform)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e, sys)