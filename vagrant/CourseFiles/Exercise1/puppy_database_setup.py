import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()



class Shelter(Base):
	__tablename__ = 'shelter'
	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	address = Column(String(250))
	city = Column(String(50))
	state = Column(String(50))
	email = Column(String(100))
	
class Puppy(Base):
	__tablename__ = 'puppy'
	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	date_of_birth = Column(DateTime, default=datetime.datetime.utcnow)
	breed = Column(String(100))
	gender = Column(String(25)) #change this to FK later?
	weight = Column(Float(2))
	shelter_id = Column(Integer,ForeignKey(Shelter.id))

engine = create_engine('sqlite:///puppyshelters.db')
Base.metadata.create_all(engine)
