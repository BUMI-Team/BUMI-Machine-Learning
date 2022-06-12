from tokenize import String
from turtle import st
from pydantic import BaseModel
# from uuid import UUID, uuid4
from typing import Optional, List
# from enum import Enum

class Datas(BaseModel):
  user_request: List
  ids: List

class Model(BaseModel):
  input_details: List
  output_details: List

class Genre(BaseModel):
  genre: str

class dataBRecommender(BaseModel):
  user_id: str