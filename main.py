from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from fastapi.middleware.cors import CORSMiddleware
import spacy
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


nlp = spacy.blank("en")
ruler = nlp.add_pipe("entity_ruler")

with open("bank_patterns.json", "r", encoding="utf-8") as f:
    patterns = json.load(f)

ruler.add_patterns(patterns)

class Patterns(BaseModel):
    l1: List[Dict[str, Any]]

class Sentence(BaseModel):
    sentence: str

@app.post("/train/")
def train_data(patterns: Patterns):
    ruler.add_patterns(patterns.l1)
    return {"message": f"{len(patterns.l1)} patterns added"}

@app.post("/test/")
def test_model(sentence: Sentence):
    doc = nlp(sentence.sentence)
    return [(ent.text, ent.label_) for ent in doc.ents]


'''
{
  "l1": [
    {
      "label": "BANK",
      "pattern": "UAB"
    },

    {
      "label": "BANK",
      "pattern": "IDBI"
    },

    {
      "label": "BANK",
      "pattern": "AXIS"
    }

  ]
}
'''