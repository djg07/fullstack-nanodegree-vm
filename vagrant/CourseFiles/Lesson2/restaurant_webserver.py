from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import sys
import cgi

class webServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		
		if self.path.endswith("/restaurant"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()


			message = "<html><body>"
			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				message += "<h1>" + restaurant.name + "</h1>"
				message += "<h2><a href='/" + str(restaurant.id) + "/edit'>Edit</a></h2>"
				message += "<h2><a href='/" + str(restaurant.id) + "/delete'>Delete</a></h2>"

			message += "<h1><a href='/new'> Make a New Restaurant Here! </a></h1>"
			message += "</body></html>"
			self.wfile.write(message)

			return

		if self.path.endswith("/new"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			message = "<html><body>"
			message += "<h1> Make a New Restaurant </h1>"
			message += "<form method='POST' enctype='multipart/form-data' action='addRestaurant'>"
			message += "<h2>Restaurant Name: </h2> <input name='message' type='text'>"
			message += "<input type='submit' value='Submit'></form>"
			message += "</body></html>"

			self.wfile.write(message)
			
			return

		if self.path.endswith("/edit"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			restaurantID = self.path.split("/")[1]
			message = "<html><body>"

			for restaurant in session.query(Restaurant.name).filter(Restaurant.id==restaurantID):
				message += "<h2>" + restaurant.name + "</h2>"
				message += "<form method='POST' enctype='multipart/form-data' action='edit'>"
				message += "<h2>Restaurant Name: </h2> <input name='message' type='text'>"
				message += "<input type='submit' value='Submit'></form>"
			
			message += "</body></html>"

			self.wfile.write(message)

		if self.path.endswith("/delete"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			restaurantID = self.path.split("/")[1]			
			message = "<html><body>"
			for restaurant in session.query(Restaurant.name).filter(Restaurant.id==restaurantID):
				message += "<h2>" + restaurant.name + "</h2>"
				message += "<form method='POST' enctype='multipart/form-data' action='delete'>"
				message += "<h2>Are you sure you would like to delete? </h2>"
				message += "<input type='submit' value='Delete'></form>"

			message += "</body></html>"
			self.wfile.write(message)

		# except IOError:
		# 	self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()

		if self.path.endswith("/addRestaurant"):
			
			self.send_response(301)
			self.end_headers()
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')

			newRestaurantName = messagecontent[0]
			newRestaurantORM = Restaurant(name = newRestaurantName)
			session.add(newRestaurantORM)
			session.commit()

			self.wfile.write("<h2>Success!</h2>")

		if self.path.endswith("/edit"):
			
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')

			restaurantID = self.path.split("/")[1]
			updatedName = messagecontent[0]

			restaurantORM = session.query(Restaurant).filter_by(id=restaurantID)
			for restaurant in restaurantORM:
				restaurant.name = updatedName
				session.add(restaurant)
				session.commit()
				
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

			self.wfile.write("<h2>Success!</h2>")

		if self.path.endswith("/delete"):			

			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			
			if ctype == 'multipart/form-data':
				fields=cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')

			restaurantID = self.path.split("/")[1]			
			restaurantORM = session.query(Restaurant).filter_by(id=restaurantID)
			
			for restaurant in restaurantORM:
				session.delete(restaurant)
				session.commit()
				
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')

				self.end_headers()

			self.wfile.write("<h2>Success!</h2>")

		# except:
		# 	pass

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), webServerHandler)
		print "Web Server running on port %s"  % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()

if __name__ == '__main__':
	main()