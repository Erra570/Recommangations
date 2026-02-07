from pydantic import BaseModel
from typing import List, Literal

MediaType = Literal["anime", "manga"]

class RecommendationsIdsResponse(BaseModel):
    username: str
    mediaType: MediaType
    ids: List[int]
