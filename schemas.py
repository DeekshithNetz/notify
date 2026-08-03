from pydantic import BaseModel
from datetime import datetime


class GoogleLogin(BaseModel):
    google_id: str
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserData(BaseModel):
    id: int
    name: str
    email: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserData


class UpdateFCMToken(BaseModel):
    fcm_token: str


class NotificationRequest(BaseModel):
    title: str
    message: str