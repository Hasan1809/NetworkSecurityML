from src.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.constant.training_pipeline import SCHEMA_FILE_PATH
from src.utils.main_utils.utils import read_yaml_file , write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd 
import os 
import sys


class DataValidation:
    def __init__(self , data_ingestion_artifact: DataIngestionArtifact , data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact 
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_number_of_columns(self , dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config['columns'])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Data frame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_column_names(self, dataframe: pd.DataFrame) -> bool:
        try:
            dataframe_columns = set(dataframe.columns)

            # Extract just the keys (column names) from schema['columns']
            schema_columns = set(col for col_dict in self.schema_config['columns'] for col in col_dict.keys())

            missing_columns = [col for col in schema_columns if col not in dataframe_columns]

            if missing_columns:
                logging.info(f"Missing columns: {missing_columns}")
                return False

            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def detect_data_drift(self, base_dataframe: pd.DataFrame , current_dataframe: pd.DataFrame , threshold = 0.05) -> dict:
        try:
            status = True
            c = 0
            drift_report = {}
            for column in base_dataframe.columns:
                d_statistic , p_value = ks_2samp(base_dataframe[column] , current_dataframe[column])
                if p_value >= threshold:
                    is_found = False
                else:
                    is_found = True
                    c += 1
                drift_report.update({column:{
                    "p_value": float(p_value),
                    "d_statistic": float(d_statistic),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path , exist_ok = True)
            write_yaml_file(file_path=drift_report_file_path , content=drift_report)
            if c/len(base_dataframe.columns) > 0.1:
                status = False 
            
            return status 
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            error = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            train_dataframe = pd.read_csv(train_file_path)
            test_dataframe = pd.read_csv(test_file_path)
            
            status = self.validate_number_of_columns(train_dataframe)
            if not status:
                error += f"Train data does not have all the required columns\n"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error += f"Test data does not have all the required columns\n"
            status = self.validate_column_names(train_dataframe)
            if not status:
                error += f"Train data does not have all the required column names\n"
            status = self.validate_column_names(test_dataframe)
            if not status:
                error += f"Test data does not have all the required column names\n"
                
            status = self.detect_data_drift(base_dataframe=train_dataframe , current_dataframe=test_dataframe)
            
            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                
                train_dataframe.to_csv(self.data_validation_config.valid_train_file_path , index = False , header = True)
                test_dataframe.to_csv(self.data_validation_config.valid_test_file_path , index = False , header = True)
            else:
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                
                train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path , index = False , header = True)
                test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path , index = False , header = True)
                error += f"Data drift found in the dataset\n"
            
            if len(error) > 0:
                logging.info(f"Data Validation failed with error: {error}")
            
            data_validation_artifact = DataValidationArtifact(
                validation_status = len(error) == 0,
                valid_train_file_path = self.data_validation_config.valid_train_file_path,
                valid_test_file_path = self.data_validation_config.valid_test_file_path,
                invalid_train_file_path = self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path = self.data_validation_config.invalid_test_file_path,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)        