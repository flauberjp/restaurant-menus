from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations ##
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if (self.path.endswith("/restaurants")):
                items = session.query(Restaurant).all()
                restaurantList = ""
                for item in items:
                    restaurantList += item.name + "<BR>\
                        <a href='/restaurants/%s/edit'>Edit</a><BR>\
                        <a href='/restaurants/%s/delete'>Delete</a><BR>\
                        <BR>" % (item.id, item.id)
                                        
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = "<a href='/restaurants/new'>Make a New Restaurant Here</a>"
                output += "<html><body><h2>Restaurants:</h2><BR>"
                output += restaurantList
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if (self.path.endswith("/restaurants/new")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants'>Restaurants List</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='\
                       /restaurants/new'><h2>Make a New Restaurant</h2><input\
                       name='newRestaurantName' type='text'><input type='submit' value='Create'>\
                       </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if (self.path.startswith("/restaurants/") and
              self.path.endswith("edit")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurantId = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants'>Restaurants List</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='\
                       /restaurants/%s/edit'><h2>Rename Restaurant</h2><input\
                       name='newRestaurantName' type='text' value='%s'> \
                       <input type='submit' value='Update'>\
                       </form>" % (restaurantId, myRestaurantQuery.name)
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if (self.path.startswith("/restaurants/") and
              self.path.endswith("delete")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurantId = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants'>Restaurants List</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='\
                       /restaurants/%s/delete'><h2>Confirm delation?</h2>\
                       Restaurant to be deleted: %s \
                       <input type='submit' value='Delete'>\
                       </form>" % (restaurantId, myRestaurantQuery.name)
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if (self.path.endswith("/hello")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='\
                       hello'><h2>What would you like me to say?</h2><input\
                       name='message' type='text'><input type='submit' value='Submit'>\
                       </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if (self.path.endswith("/hola")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


                output = ""
                output += "<html><body>&#161Hello <a href='/hello' > Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='\
                       hello'><h2>What would you like me to say?</h2><input\
                       name='message' type='text'><input type='submit' value='Submit'>\
                       </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

        except:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if (self.path.endswith("/delete")):
                restaurantId = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()

                if (myRestaurantQuery != []):
                    session.delete(myRestaurantQuery)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if (self.path.endswith("/edit")):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if (ctype == 'multipart/form-data'):
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantId = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()

                    if (myRestaurantQuery != []):
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if (self.path.endswith("/restaurants/new")):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if (ctype == 'multipart/form-data'):
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant class
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                
               

        except:
            pass


    def do_PUT(self):
        try:
            print("PUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUTPUT")
                
               

        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()