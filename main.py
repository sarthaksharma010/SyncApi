from cgitb import handler
from email import header
import inspect
from operator import imod
import re
from tarfile import SUPPORTED_TYPES
from tkinter.messagebox import NO
from urllib import request
from parse import parse
import types
from tkinter import S, W
from typing import Any
from Response import Response
from request import Request 

SUPPORTED_REQ_METHODS={'GET','POST','DELETE','PUT'}



class SlowAPI:
    def __init__(self,middlewares=[]) -> None:
        self.routes=dict()
        self.middlewares=middlewares
        self.middlewares_for_routes=dict()

    def __call__(self, environ ,start_response) -> Any:
        response=Response()
        request=Request(environ)

        for middleware in self.middlewares:
            if isinstance(middleware,types.FunctionType):
                middleware(request)
            else:
                raise  ValueError("You can only pass functions as Middleware!")

        for path,handler_dict in self.routes.items():
            res=parse(path,request.path_info)
            # print(res)
            for request_method,handler in handler_dict.items():
                if request.request_method==request_method and res:
                    route_mw_list=self.middlewares_for_routes[path][request_method]

                    for middleware in route_mw_list:
                        if(isinstance(middleware,types.FunctionType)):
                            middleware(request)
                        else:
                            raise ValueError("You can only pass functions as Middleware!")
                
                    handler(request,response,**res.named)
                    return response.as_wsgi(start_response)

        return response.as_wsgi(start_response)


    def route_common(self,path,handler,method_name,middlewares):
        # {
        #     users:{
        #         Method : handler
        #         Method2 :handler2
        #     }
        # }

        path_name = path or f"/{handler.__name__}"
            #  if the path is not given we use function as a route

        if path_name not in self.routes:
           self.routes[path_name]={}
                
        self.routes[path_name][method_name]=handler
            # print(self.routes)

            # //For Middleware
            # {
            #     'path/id':{
            #         "Get"={mv1,mv2}
            #         "method"={mv1,mv2}
            #     }
            # }

        if path_name not in self.middlewares_for_routes:
            self.middlewares_for_routes[path_name]={}
        
        self.middlewares_for_routes[path_name][method_name]=middlewares
        return handler


    def get(self,path=None,middlewares=[]):
        def wrapper(handler):
            return self.route_common(path,handler,"GET",middlewares)
        return wrapper

    def post(self,path=None,middlewares=[]):
        def wrapper(handler):
            return self.route_common(path,handler,"POST",middlewares)
        return wrapper  

    def delete(self,path=None,middlewares=[]):
        def wrapper(handler):
            return self.route_common(path,handler,"DELETE",middlewares)
        return wrapper  

    def put(self,path=None,middlewares=[]):
        def wrapper(handler):
            return self.route_common(path,handler,"PUT",middlewares)
        return wrapper  
    

    # class Based ROuting decorator(route)

    def route(self,path=None,middlewares=[]):
        def wrapper(handler):

            if isinstance(handler,type):
                class_members=inspect.getmembers(handler,lambda x: inspect.isfunction(x) and not (x.__name__.startswith("__") and x.__name__.endswith("__")) and x.__name__.upper() in SUPPORTED_REQ_METHODS)  
                for fn_name , fn_handler in class_members:
                    self.route_common(path or f"/{handler.__name__}",fn_handler,fn_name.upper(),middlewares)
                    # print(path,fn_name.upper())
                    
            else:
                raise ValueError("@route can only be used for classes")

        return wrapper
        





    