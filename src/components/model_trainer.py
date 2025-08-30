import os 
import sys 
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact , ModelTrainerArtifact , ClassificationMetricArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.utils.ml_utils.model.estimator import NetworkModel
from src.utils.main_utils.utils import *
from src.utils.ml_utils.metric.classification_metric import get_classification_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig , data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info("Model trainer log started")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_model(self, X_train, y_train , X_test, y_test):
        try:
            models = {
                "DecisionTree": DecisionTreeClassifier(),
                "RandomForest": RandomForestClassifier(verbose= 1),
                "GradientBoosting": GradientBoostingClassifier(verbose = 1),
                "LogisticRegression": LogisticRegression(),
                "AdaBoost": AdaBoostClassifier(),
            }
            
            params={
            "DecisionTree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2'],
            },
            "RandomForest":{
                'criterion':['gini', 'entropy', 'log_loss'],
                'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "GradientBoosting":{
                'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                'criterion':['squared_error', 'friedman_mse'],
                'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "LogisticRegression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
            }
            
            model_report:dict = evaluate_models(X_train, y_train, X_test, y_test , models, params)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]            
            best_model = models[best_model_name]
            logging.info(f"Best model found , Model name : {best_model_name} , r2 score : {best_model_score}")
            
            y_train_pred = best_model.predict(X_train)
            classification_train_metric = get_classification_score(y_train , y_train_pred)
            
            y_test_pred = best_model.predict(X_test)
            classification_test_metric = get_classification_score(y_test , y_test_pred)
            
            preprocessor = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok= True)
            
            network_model = NetworkModel(preprocessor = preprocessor , model = best_model)
            save_object(file_path = self.model_trainer_config.trained_model_file_path , obj = network_model)
            logging.info("Trained model object saved")
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                train_metric_artifact = classification_train_metric,
                test_metric_artifact = classification_test_metric
            )
            
            logging.info("Model trainer artifact created")
            
            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array(file_path=self.data_transformation_artifact.transformed_test_file_path)
            
            logging.info("Loaded train and test arrays")
            
            X_train, y_train = train_arr[:,:-1] , train_arr[:,-1]
            X_test, y_test = test_arr[:,:-1] , test_arr[:,-1]
            
            return self.train_model(X_train, y_train, X_test, y_test)
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)