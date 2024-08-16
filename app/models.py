from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

from datetime import datetime

from utils import get_current_utc_time




class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    telegram_id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str]
    created_at: datetime = Field(default_factory=get_current_utc_time)
    last_interaction: datetime = Field(default_factory=get_current_utc_time)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    content: str
    timestamp: datetime = Field(default_factory=get_current_utc_time)
    is_from_user: bool
    
    
class Conversation(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: int
    messages: List[Message] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=get_current_utc_time)
    end_time: Optional[datetime] = None
    was_escalated: bool = False

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    @classmethod
    def from_mongo(cls, data):
        if not data:
            return None
        if '_id' in data:
            data['id'] = data['_id']
        return cls(**data)