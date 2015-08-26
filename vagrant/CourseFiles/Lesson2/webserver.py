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

		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>Hello!</body></html>"
				message += "<form method='POST' enctype='multipart/form-data'"
				message += " action='/changeName'><h2>What would you like me to say?</h2>"
				message += "<input name='message' type='text'><input type='submit'" 
				message += " value='Submit'></form>"
				self.wfile.write(message)
				print message
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body> &#161 Hola ! </body></html>"
				message += "<form method='POST' enctype='multipart/form-data'" 
				message += " action='/changeName'><h2>What would you like me to say?</h2>" 
				message += "<input name='message' type='text'><input type='submit'"  
			  	message += " value='Submit'></form>"
				self.wfile.write(message)
				print message
				return

		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)
	def do_POST(self):
		try:
			if self.path.endswith("/changeName"):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output +=  "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				output += '''<form method='POST' enctype='multipart/form-data' action='/changeName'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
				output += "</html></body>"

				self.wfile.write(output)
				print output
		except:
			pass

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