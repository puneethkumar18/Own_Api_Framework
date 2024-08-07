from typing import Any

from response import Response


class SlowAPI:


    def __init__(self) -> None:
        self.routes = dict()

    def __call__(self, environ,start_response) -> Any:
        for key, val in environ.items():
            print(key,"->",val)
        response = Response()
        for path,handler in self.routes.items():
            for request_method, handler_function in handler.items():
                if request_method == environ['REQUEST_METHOD'] and path == environ['PATH_INFO']:
                    handler_function(environ,response)
                    response.as_wsgi(start_response)
                    return [response.text.encode()]

    def get(self,path:None):
        def wrapper(handler):
            path_name = path or handler.__name__
            self.route_common(path_name,'GET',handler)
        return wrapper
    

    def route_common(self,path,method_name,handler_function):
         # {
            #     '/users':{
            #         'GET': handler,
             #           'POST':handler2
            #     }
            # }
        if path not in self.routes:
            self.routes[path]= {}
        self.routes[path][method_name] = handler_function
    
    def delete(self,path:None):
        def wrapper(handler):
            path_name = path or handler.__name__
            self.route_common(path_name,'DELETE',handler)
        return wrapper
    
    def post(self,path:None):
        def wrapper(handler):
            path_name = path or handler.__name__
            self.route_common(path_name,'POST',handler)
        return wrapper