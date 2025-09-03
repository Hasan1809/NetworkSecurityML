import sys 
import os 
from src.exception.exception import NetworkSecurityException
import numpy as np 
import pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from src.constant.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS
from src.entity.artifact_entity import DataTransformationArtifact , DataValidationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.logging.logger import logging
from src.utils.main_utils.utils import read_yaml_file , save_numpy_array , save_object


class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    
    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info("Creating data transformer object")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            pipeline = Pipeline(steps=[
                ('Imputer' , imputer)
            ])
            return pipeline
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating data transformation")
        try:
            
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            logging.info("Read train and test data as pandas dataframe")
            
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1,0)
            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1,0)
            
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature , np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature , np.array(target_feature_test_df)]
            
            save_numpy_array(file_path=self.data_transformation_config.transformed_train_file_path , array=train_arr)
            save_numpy_array(file_path=self.data_transformation_config.transformed_test_file_path , array=test_arr)
            logging.info("Saved transformed train and test array")
            
            save_object(file_path=self.data_transformation_config.transformed_object_file_path , obj=preprocessor_object)
            logging.info("Saved preprocessor object")
            
            save_object(file_path= "final_model/preprocessor.pkl" , obj=preprocessor_object)
            
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path= self.data_transformation_config.transformed_object_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_train_file_path= self.data_transformation_config.transformed_train_file_path
            )
            
            return data_transformation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)