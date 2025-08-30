from src.components.data_ingestion import DataIngestion
from src.logging.logger import logging
from src.exception.exception import NetworkSecurityException
import sys
from src.entity.config_entity import *
from src.components.data_validation import DataValidation
from src.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact , DataTransformationArtifact
from src.components.data_transformation import DataTransformation

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Starting data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Data ingestion completed")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    try:
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact ,data_validation_config)
        logging.info("Starting data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
    
    try:
        data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact , data_transformation_config= data_transformation_config)
        logging.info("Starting data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(data_transformation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)