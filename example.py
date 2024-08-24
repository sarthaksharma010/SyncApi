from urllib import request
from main import SlowAPI
from Response import Response

def global_middleware(request):
    print("This was executed before any route")

def local_middleware(request):
    print("This is local middleware")


slowapi=SlowAPI(middlewares=[global_middleware])

@slowapi.get('/users/{id}',middlewares=[local_middleware])
def get_users(req, res ,id):
    res.send(id,200)

@slowapi.post('/users')
def post_users(req,res):
    res.send("Hey there")

@slowapi.put('/users')
def put_users(req,res):
    res.send("Hey Sarthak")


# //Class Based Routing 

@slowapi.route("/users")
class User:
    def __init__(self) -> None:
        pass

    def get(req,res):
        print(req.queries)
        res.send("HEllo Sarthak") 

    def post(req,res):
        res.render("venv/example.html",{"name":"Sarthak","message":"Hello Sarthak"})

    def put(req,res):
        pass

    def delete(req,res):
        pass
