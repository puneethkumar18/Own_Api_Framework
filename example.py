from main import SlowAPI

def golbalmiddleware(req):
    print("Main middleware function in start of applications")

slowapi = SlowAPI(middleware=[golbalmiddleware])

def routeMiddleware(req):
    print("this is the route specific middleware")

@slowapi.get('/users/{id}',[routeMiddleware])
def getUsers(req,res,id):
    res.send(id,"200 OK")

@slowapi.post('/users')
def getUsers(req,res):
    res.send(400,400).     


@slowapi.get('/users')
def getTemp(req,res):
    res.render('example',{"name":"puneeth","message":"Iam Puneeth kumar g"})


@slowapi.get('/users')
def users(req,res):
    res.send("puneeth",400)

@slowapi.route('/users',[routeMiddleware])
class User:
    # def get(req,res):
    #     res.send('puneeth',200)

    def post(req,res):
        pass



@slowapi.post('/users')
def getTemp(req,res):
    res.render('example',{"name":"puneeth", "message":"I am Puneeth kumar g"})