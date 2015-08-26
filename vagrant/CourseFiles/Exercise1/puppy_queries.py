import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import asc, desc
from puppy_database_setup import Base, Puppy, Shelter
import datetime

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

###		BASIC QUERYING		####
#			EQUALS				##
#for item in session.query(Restaurant.name).filter(Restaurant.name=="Pizza Palace"):
#	print item



#	1. Query all of the puppies 
#   and return the results in ascending alphabetical order

# puppies = session.query(Puppy).order_by(Puppy.name)
# for puppy in puppies:
# 	print "ID: %s" % puppy.id
# 	print "Name: %s" % puppy.name
# 	print "Gender: %s" % puppy.gender
# 	print "Birthday: %s" % puppy.dateOfBirth
# 	print "Picture: %s" % puppy.picture
# 	print "ShelterID: %s" % puppy.shelter_id
# 	print "Shelter Object: %s" % puppy.shelter
# 	print "Weight: %s" % puppy.weight
# 	print "-----------------------------"

# 	2. Query all of the puppies that are less 
# 	than 6 months old organized by the youngest first
# sixMonthsAgo = datetime.date(2015,02,24)
# puppies = session.query(Puppy).filter(Puppy.dateOfBirth > sixMonthsAgo)
# print puppies.count()
# for puppy in puppies:
# 	print puppy.dateOfBirth

#	3. Query all puppies by ascending weight
# puppies = session.query(Puppy).order_by(asc(Puppy.weight))
# for puppy in puppies:
# 	print puppy.weight

#	4. Query all puppies grouped by the shelter 
#	in which they are staying

puppies = session.query(Puppy).order_by(Puppy.shelter_id)
#.group_by(Puppy.shelter_id).all()
for puppy in puppies:
	print puppy.name
	print puppy.shelter_id
# print puppies