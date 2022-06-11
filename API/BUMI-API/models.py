from pydantic import BaseModel
# from uuid import UUID, uuid4
from typing import Optional, List
# from enum import Enum

#Format data untuk video recommendation
class Datas(BaseModel):
    user_request: List
    ids: List
    genres: List
    ratings: List

class Model(BaseModel):
    input_details: List
    output_details: List

#Format data untuk bisnis recommendation(Collaborative filtering)
class dataBRecommender(BaseModel):
    user_id: int
