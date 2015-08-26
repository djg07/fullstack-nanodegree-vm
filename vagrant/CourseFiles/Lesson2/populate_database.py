import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



####		ADDING A RECORD		####
# myFirstRestaurant = Restaurant(name = "Pizza Palace")
# session.add(myFirstRestaurant)
# session.commit()

# cheesepizza = MenuItem(name="Cheese Pizza", description="Made with all natural" + 
# 	"ingredients and fresh mozzarella", course="Entree", price="$8.99", 
# 	restaurant=myFirstRestaurant)

# session.add(cheesepizza)
# session.commit()

# items = session.query(Restaurant).order_by(Restaurant.name)


###		BASIC QUERYING		####
#			EQUALS				##
for item in session.query(Restaurant.name).filter(Restaurant.name=="Pizza Palace"):
	print item

# ##			LIKE 				##
# for item in session.query(Restaurant.name).filter(Restaurant.name.like("%pizza%")):
# 	print item

# ##			COUNT 				##
# items = session.query(Restaurant.name).filter(Restaurant.name.like('%Pizza%')).count() 
# print items

####		UPDATING			####
# veggieBurgers = session.query(MenuItem).filter_by(name="Veggie Burger")
# for veggieBurger in veggieBurgers:
# 	print veggieBurger.id
# 	print veggieBurger.price
# 	print veggieBurger.restaurant.name
# 	print "\n"
# 	if (veggieBurger.price != "$2.99"):
# 		veggieBurger.price = "$2.99"
	
# 	session.add(veggieBurger)
# 	session.commit()

####		DELETING			####
# pizzaPalaces = session.query(Restaurant).filter_by(name="Pizza Palace")
# for x in pizzaPalaces:
# 	session.delete(x)
# 	session.commit()



