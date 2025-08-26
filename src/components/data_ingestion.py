from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig
import os 
import sys 
import numpy as np 
import pandas as pd
import pymongo 
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
from src.entity.artifact_entity import DataIngestionArtifact

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self , data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def get_db_collection(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis = 1)
            
            df.replace({"na" : np.nan} , inplace = True)
            return df 
        
        except Exception as e:
            raise NetworkSecurityException(e , sys)
    
    
    def export_data_into_feature_store(self , dataframe:pd.DataFrame):
        try:
            store_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(store_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(store_path , index=False , header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    
    def split_data_as_train_test(self , dataframe:pd.DataFrame):
        try:
            train_set , test_set = train_test_split(dataframe , test_size = self.data_ingestion_config.train_test_split_ratio , random_state=42)
            logging.info(f"Performed train test split with test size {self.data_ingestion_config.train_test_split_ratio}")
            
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
            
            dir_path = os.path.dirname(train_file_path)
            os.makedirs(dir_path , exist_ok=True)
            
            train_set.to_csv(train_file_path , index = False , header = True)
            test_set.to_csv(test_file_path , index = False , header = True)
            
            logging.info(f"Exported training and testing data into file path : [{train_file_path}] , [{test_file_path}]")
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    
    def initiate_data_ingestion(self):
        try:
            df = self.get_db_collection()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)
            
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path = self.data_ingestion_config.training_file_path,
                test_file_path = self.data_ingestion_config.testing_file_path
            )
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)