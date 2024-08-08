import inspect
from typing import Any
from parse import parse
import types
from request import Request
from response import Response

SUPPORTED_REQUEST_METHODS = ['POST','GET','DELETE']

class SlowAPI:


    def __init__(self,middleware) -> None:
        self.routes = dict()
        self.middleware = middleware
        self.middleware_for_routes = dict()
      

    def __call__(self, environ,start_response) -> Any:
        request = Request(environ)
        response = Response()
        
        for middleware in self.middleware:
            if isinstance(middleware,types.FunctionType):
                middleware(request)
            else:
                raise ValueError("Middleware can not be a other than functions")
        print(self.routes)
        for path,handler_dic in self.routes.items():
            res = parse(path,request.path_info)
            for request_method, handler_function in handler_dic.items():
                route_middlewares = self.middleware_for_routes[path][request_method]
                for middleware in route_middlewares:
                    if isinstance(middleware,types.FunctionType):
                        middleware(request)
                    else:
                        raise "route -> middle can only be functions"
                if request_method == request.request_method and res:
                    handler_function(request,response,**res.named)
                    return response.as_wsgi(start_response)
        return response.as_wsgi(start_response)

    def get(self,path:None,middlewares=[]):
        def wrapper(handler):
            path_name = path or handler.__name__
            return self.route_common(path_name,'GET',handler,middlewares)
        return wrapper
    

    def route_common(self,path,method_name,handler_function,middlewares=[]):
         # {
            #     '/users':{
            #         'GET': handler,
             #           'POST':handler2
            #     }
            # }
        if path not in self.routes:
            self.routes[path]= {}
        self.routes[path][method_name] = handler_function
        # middleware
        # {
        #     '/users':{
        #         'GET':[middleware1,middleware2]
        #     }
        # }
        if path not in self.middleware_for_routes:
            self.middleware_for_routes[path] = {}
        
        self.middleware_for_routes[path][method_name] = middlewares
        return handler_function
    
    def delete(self,path:None,middlewares=[]):
        def wrapper(handler):
            path_name = path or handler.__name__
            return self.route_common(path_name,'DELETE',handler,middlewares)
        return wrapper
    
    def post(self,path:None,middlewares=[]):
        def wrapper(handler):
            path_name = path or handler.__name__
            return self.route_common(path_name,'POST',handler,middlewares)
        return wrapper
    


    def route(self,path:None,middlewares = []):
        def wrapper(handler):
            path_name = path or f"{handler.__name__}"
            if isinstance(handler,type):
                class_members =  inspect.getmembers(handler,lambda x: inspect.isfunction(x) and not (x.__name__.startswith("__") and x.__name__.endswith("__")) and x.__name__.upper() in SUPPORTED_REQUEST_METHODS ,)
                for (fn_name,fn_handler) in class_members:
                   
                    self.route_common(path_name ,fn_name.upper(),fn_handler,middlewares)
            else:
                raise ValueError("@route can br used for classess")
            
        return wrapper
    

    