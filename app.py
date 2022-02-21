from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import psycopg2

conn = psycopg2.connect("dbname=pyramid user=postgres password=123456 host=localhost port=5432")

cr = conn.cursor()

sql = "CREATE TABLE IF NOT EXISTS pyuser( id SERIAL PRIMARY KEY, name VARCHAR(220) NOT NULL, email VARCHAR(220) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"

dt = cr.execute(sql)

if dt == True:
   print("Table created.")

@view_config(
    route_name='home',
    request_method='GET',
    renderer='templates/home.jinja2'
)

@view_config(
    route_name='home',
    request_method='POST',
    renderer='templates/home.jinja2'
)

def home(request):
     if request.method =='POST':
        name = request.POST.get('fname')
        email = request.POST.get('email')
        cr.execute("INSERT INTO pyuser(name, email) VALUES(%s, %s)", [name, email])
        conn.commit()
        print(request.POST.get('fname'))

     return {"greet": 'Welcome', "name": 'Johan'} 


@view_config(
    route_name='about',
    request_method='GET',
    renderer='templates/about.jinja2'
)

def about(request):
     cr.execute("SELECT * FROM pyuser")
     users = cr.fetchall()
     
     return {"heading": 'About page', 'udata': users}     
   
     

if __name__ == '__main__':
    with Configurator() as config:
        config.include('pyramid_jinja2')
        #routers ===
        config.add_route('home', '/')
        config.add_route('about', '/about')
        config.scan()
       
        
        app = config.make_wsgi_app()
    print("Server is running on port 8000")    
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
