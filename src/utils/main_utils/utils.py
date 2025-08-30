import yaml 
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
import os 
import sys 
import numpy as np 
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path , 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path:str , content:dict  , replace:bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok = True)
        with open(file_path , 'w') as yaml_file:
            yaml.dump(content , yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array(file_path:str , array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok = True)
        with open(file_path , 'wb') as file_obj:
            np.save(file_obj , array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_object(file_path:str , obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok = True)
        with open(file_path , 'wb') as file_obj:
            pickle.dump(obj , file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path , 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array(file_path:str) -> np.array:
    try:
        with open(file_path , 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        
        for i in range(len(list(models))):
            logging.info(f"Evaluating model: {list(models.keys())[i]}")
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]
            
            gs = GridSearchCV(model, param, cv=3)
            gs.fit(X_train, y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            report[list(models.keys())[i]] = test_model_score
            
        return report
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)