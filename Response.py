import re
from this import s


class Response:
    def __init__(self, status_code="404 Missing Not Found", text="Route not found!") -> None:
        self.status_code=status_code
        self.text=text
        self.headers=[]

    def as_wsgi(self,start_response):
        start_response(self.status_code,self.headers)
        return [self.text.encode()]

    def send(self,text="",status_code="200 OK"):
        if isinstance(text,str):
            self.text=text
        else :
            self.text=str(text)
        
        if isinstance(status_code,int):
            self.status_code=str(status_code)
        elif isinstance(status_code,str):
            self.status_code=status_code
        else :
            raise ValueError("Status code have to be either int or str")

    def render(self,template_name,context={}):
        path=f"{template_name}"

        with open(path) as fp:
            template=fp.read()

            for key,value in context.items():
                template=re.sub(r'{{\s*' + re.escape(key) + r'\s*}}',str(value),template)

        self.headers.append(('Content-Type',"text/html"))
        self.text=template
        self.status_code="200 OK"
