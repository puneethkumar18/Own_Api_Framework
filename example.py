from main import SlowAPI

slowapi = SlowAPI()


@slowapi.get('/users')
def getUsers(req,res):
    res.send(['I am Puneeth Kumar','FRAMEWORK'],"200 OK")

@slowapi.get('/users')
def getUsers(req,res):
    res.send(400,400)