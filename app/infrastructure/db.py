from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime, ForeignKey
from app.core.database import Base
from app.domain.entities import PetStatus, AdoptionStatus
import datetime

class ShelterDB(Base):
    __tablename__ = "shelters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    contact_phone = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class PetDB(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    age = Column(Integer, nullable=False, default=0)
    status = Column(SQLEnum(PetStatus), default=PetStatus.AVAILABLE)
    shelter_id = Column(Integer, nullable=False)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    password = Column(String, nullable=False)

class AdoptionDB(Base):
    __tablename__ = "adoptions"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(SQLEnum(AdoptionStatus), default=AdoptionStatus.PENDING)
    application_date = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String)
