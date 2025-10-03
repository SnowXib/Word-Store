from pydantic import BaseModel
from typing import List

class WordItem(BaseModel):
    word: str


class Settings(BaseModel):
    api_key: str
    model: str
    base_url: str
    language: str


class TestItem(BaseModel):
    target: str
    user_try: str


class Testing(BaseModel):
    testing_array: List[TestItem]