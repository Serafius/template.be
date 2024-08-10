from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from random import randint
from datetime import datetime


# User MongoDB Model
class PersonalInfo(BaseModel):
    name: str = "user" + str(randint(100000, 999999))
    email: str
    pictureUrl: str = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
    about: str
    credits: int = 0


class CustomerId(BaseModel):
    id: str


class Credentials(BaseModel):
    ids: List[Dict[str, str]]
    loginMethod: str = "email"
    lastLogin: Optional[str]
    oldPlans: List[str]


class Plan(BaseModel):
    id: str
    name: str
    credits: int
    recurring: str
    createdAt: str
    expirationDate: str
    isCanceled: bool
    isExpired: bool
    oldId: str


class Auth(BaseModel):
    password: Optional[str]
    token: Optional[str]


class User(BaseModel):
    personalInfo: PersonalInfo
    credentials: Credentials
    plan: Plan
    auth: Auth
    customerIds: List[CustomerId]
    isDeleted: bool
    isVerified: bool
    createdDate: datetime
    updatedDate: datetime


# User DTO Models


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    pictureUrl: str
    loginMethod: str

class UserUpdate(BaseModel):
    personalInfo: Optional[PersonalInfo]
    credentials: Optional[Credentials]
    plan: Optional[Plan]
    auth: Optional[Auth]
    isDeleted: Optional[bool]
    isVerified: Optional[bool]


class UserCheck(BaseModel):
    name: str
    email: str
    id: str
    pictureUrl: str
    loginMethod: str


class UserObject(BaseModel):
    id: str
    personalInfo: str
