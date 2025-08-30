from src.entity.artifact_entity import ClassificationMetricArtifact
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
from sklearn.metrics import f1_score , recall_score , precision_score
import sys

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        
        classification_metric_artifact = ClassificationMetricArtifact(
            f1_score=f1,
            precision_score=precision,
            recall_score=recall
        )
        return classification_metric_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)