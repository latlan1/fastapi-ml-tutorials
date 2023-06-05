from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
import tensorflow
from tensorflow.keras.models import load_model
import numpy as np
import json
import pandas as pd

model = load_model("model.h5", custom_objects=None, compile=False)

app = FastAPI()


class Feature(BaseModel):
    price_open: float
    price_low: float
    price_close: float
    volume_traded: float
    trades_count: float
    price_open_1: float
    price_high_1: float
    price_low_1: float
    price_close_1: float
    volume_traded_1: float
    trades_count_1: int
    price_open_2: float
    price_high_2: float
    price_low_2: float
    price_close_2: float
    volume_traded_2: float
    trades_count_2: int
    price_open_3: float
    price_high_3: float
    price_low_3: float
    price_close_3: float
    volume_traded_3: float
    trades_count_3: int
    price_open_4: float
    price_high_4: float
    price_low_4: float
    price_close_4: float
    volume_traded_4: float
    trades_count_4: int
    price_open_5: float
    price_high_5: float
    price_low_5: float
    price_close_5: float
    volume_traded_5: float
    trades_count_5: int
    price_open_6: float
    price_high_6: float
    price_low_6: float
    price_close_6: float
    volume_traded_6: int
    trades_count_6: int
    price_open_7: float
    price_high_7: float
    price_low_7: float
    price_close_7: float
    volume_traded_7: float
    trades_count_7: int
    price_open_8: float
    price_high_8: float
    price_low_8: float
    price_close_8: float
    volume_traded_8: float
    trades_count_8: int
    price_open_9: float
    price_high_9: float
    price_low_9: float
    price_close_9: float
    volume_traded_9: float
    trades_count_9: int


class Dataset(BaseModel):
    bitcoin_last_minute: List[Feature]


class Prediction(BaseModel):
    bitcoin_prediction: float


@app.get("/")
def read_root():
    return {"Status of API": "UP!"}


@app.post("/predict", response_model=Prediction)
def predict(user_request: Dataset):
    data = user_request.bitcoin_last_minute
    df = pd.DataFrame([i.dict() for i in data])
    # print(type(df), df)
    res = model.predict(df)
    return {"bitcoin_prediction": res}


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
