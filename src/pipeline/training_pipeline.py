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
from src.constant.training_pipeline import TRAINING_BUCKET_NAME
from src.cloud.s3_syncer import S3Sync

class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()
            self.s3_sync = S3Sync()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            self.data_ingestion_artifact = self.data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_validation = DataValidation(data_ingestion_artifact=self.data_ingestion_artifact ,data_validation_config=self.data_validation_config)
            self.data_validation_artifact = self.data_validation.initiate_data_validation()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_data_transformation(self):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            self.data_transformation = DataTransformation(data_validation_artifact=self.data_validation_artifact , data_transformation_config= self.data_transformation_config)
            self.data_transformation_artifact = self.data_transformation.initiate_data_transformation()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def start_model_trainer(self):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            self.model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config , data_transformation_artifact=self.data_transformation_artifact)
            self.model_trainer_artifact = self.model_trainer.initiate_model_trainer()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir , aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = "final_model" , aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def run_pipeline(self):
        try:
            self.start_data_ingestion()
            self.start_data_validation()
            self.start_data_transformation()
            self.start_model_trainer()
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
        except Exception as e:
            raise NetworkSecurityException(e, sys)