from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime

class PetStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ADOPTED = "ADOPTED"
    PENDING = "PENDING"

class AdoptionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Shelter(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., max_length=100)
    location: str
    contact_phone: str
    email: str
    password: str

    class Config:
        from_attributes = True

class Pet(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., max_length=100)
    species: str
    age: int = 0
    status: PetStatus = PetStatus.AVAILABLE
    shelter_id: int

    class Config:
        from_attributes = True

class User(BaseModel):
    id: Optional[int] = None
    email: str
    name: str
    password: str
    
    class Config:
        from_attributes = True

class Adoption(BaseModel):
    id: Optional[int] = None
    pet_id: int
    user_id: int
    status: AdoptionStatus = AdoptionStatus.PENDING
    application_date: Optional[datetime] = None
    message: Optional[str] = ""

    class Config:
        from_attributes = True
