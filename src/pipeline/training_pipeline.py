import os 
import sys 
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from src.entity.artifact_entity import (
    DataIngestionArtifact ,
    DataValidationArtifact ,
    DataTransformationArtifact,
    ModelTrainerArtifact
)


class TrainingPipeline:
    def __init__(self):
        try:
            self.trainig_pipeline_config = TrainingPipelineConfig()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.trainig_pipeline_config)
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.trainig_pipeline_config)
            self.data_validation = DataValidation(data_ingestion_artifact=self.data_ingestion_artifact ,data_validation_config=self.data_validation_config)
            self.data_validation_artifact = self.data_validation.initiate_data_validation()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_transformation(self):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.trainig_pipeline_config)
            self.data_transformation = DataTransformation(data_validation_artifact=self.data_validation_artifact , data_transformation_config= self.data_transformation_config)
            self.data_transformation_artifact = self.data_transformation.initiate_data_transformation()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_trainer(self):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.trainig_pipeline_config)
            self.model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config , data_transformation_artifact=self.data_transformation_artifact)
            self.model_trainer_artifact = self.model_trainer.initiate_model_trainer()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def run_pipeline(self):
        try:
            self.start_data_ingestion()
            self.start_data_validation()
            self.start_data_transformation()
            self.start_model_trainer()
        except Exception as e:
            raise NetworkSecurityException(e, sys)