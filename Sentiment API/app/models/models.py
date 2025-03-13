from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from datetime import datetime

class news(BaseModel):
    id: Optional[str] = Field(default_factory=str, alias="_id")
    url: str
    disruptionType: str
    imageUrl: Optional[HttpUrl] = None
    isdeleted: bool
    lat: Optional[float] = None
    lng: Optional[float] = None
    location: str
    publishedDate: datetime
    radius: Optional[float] = None
    raw_text: str
    severity: str
    text: str
    title: str
    actual_text: str
    sentiment: Optional[float] = None
    ner: Optional[Dict[str, List[str]]] = None

class update_sentiment_response(BaseModel):
    update: bool
    id: Optional[str] = Field(default_factory=str, alias="_id")
    sentiment: Optional[float] = None

class SentimentUpdateRequest(BaseModel):
    id: str

class TimeSeriesData(BaseModel):
    data: Dict[datetime, float] = Field(..., description="Mapping of datetime strings to integer values")


class TimeSeriesData_Dict(BaseModel):
    data: Dict[str, Dict[str, List[str]]]= Field(default_factory=dict)


# class Sentiment_ItemWithId(Sentiment_Item):
#     id: str