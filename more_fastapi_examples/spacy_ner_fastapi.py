from copy import deepcopy
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from enum import Enum
import spacy
import uvicorn


def load_models():
    """
    load the models from disk
    and put them in a dictionary
    Returns:
        dict: loaded models
    """
    models = {
        "en_sm": spacy.load("en_core_web_sm"),
        "fr_sm": spacy.load("fr_core_news_sm"),
    }
    print("models loaded from disk")
    return models


class ModelLanguage(str, Enum):
    fr = "fr"
    en = "en"


class ModelSize(str, Enum):
    sm = "sm"
    md = "md"
    lg = "lg"


class UserRequestIn(BaseModel):
    """
    Uses 3 attributes as input to spacy model based on ModelLanguage and ModelSize classes
    that inherit from str and Enum. We use Enum to limit the possible values for each of the fields to
    1 choice.
    """

    text: str
    model_language: ModelLanguage = "en"
    model_size: ModelSize = "sm"


class EntityOut(BaseModel):
    start: int
    end: int
    type: str
    text: str


class EntitiesOut(BaseModel):
    """
    Schema uses 2 keys entities and anonymized_text
    """

    entities: List[EntityOut]
    anonymized_text: str


models = load_models()
app = FastAPI()


@app.post("/entities", response_model=EntitiesOut)
# force response to follow EntitiesOut class schema
def extract_entities(user_request: UserRequestIn):
    """
    Define handler with the user's request that follows UserRequestIn class schema
    """
    text = user_request.text
    language = user_request.model_language
    model_size = user_request.model_size

    model_key = language + "_" + model_size

    model = models[model_key]
    doc = model(text)

    entities = [
        {
            "start": ent.start_char,
            "end": ent.end_char,
            "type": ent.label_,
            "text": ent.text,
        }
        for ent in doc.ents
    ]

    anonymized_text = list(deepcopy(text))

    for entity in entities:
        start = entity["start"]
        end = entity["end"]
        anonymized_text[start:end] = "X" * (end - start)

    anonymized_text = "".join(anonymized_text)
    return {"entities": entities, "anonymized_text": anonymized_text}


if __name__ == "__main__":
    uvicorn.run("spacy_ner_fastapi:app", reload=True)

# Source: https://towardsdatascience.com/how-to-deploy-a-machine-learning-model-with-fastapi-docker-and-github-actions-13374cbd638a
# http://localhost:8000/docs
# uvicorn spacy_ner_fastapi:app --reload
