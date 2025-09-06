import sys 
import os 
import certifi 
from dotenv import load_dotenv
import pymongo
from src.logging.logger import logging
from fastapi.middleware.cors import CORSMiddleware
from src.exception.exception import NetworkSecurityException
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd 
from src.utils.main_utils.utils import *
from src.constant.training_pipeline import *
from src.pipeline.training_pipeline import TrainingPipeline
from fastapi.templating import Jinja2Templates
from src.utils.ml_utils.model.estimator import NetworkModel


ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(mongo_db_url , tlsCAFile=ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origin = ["*"]
templates = Jinja2Templates(directory="./templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request:Request , file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor , model=final_model)
        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred
        df.to_csv("prediction_output/output.csv")
        table_html = df.to_html(classes = 'table table-striped')
        return templates.TemplateResponse("table.html" , {"request":request , "table_html":table_html})
    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port = 8080)