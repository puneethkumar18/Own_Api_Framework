import re


class Response:
    def __init__(self,status_code='404 missing error',text='Route not found!',) -> None:
        self.status_code = status_code
        self.headers = []
        self.text = text
        self.middleware = []

    def as_wsgi(self, start_response):
        start_response(self.status_code,headers=self.headers)
        return [self.text.encode()]
    
    def send(self,text="",status_code="200 OK"):
        if isinstance(status_code,int):
            self.status_code = str(status_code)
        elif isinstance(status_code, str):
            self.status_code = status_code
        else:
            raise ValueError("Status code must be either int or string")
            
        if isinstance(text,str):
            self.text = text
        
        else:
            self.text = str(text)

    def render(self,template_name,context={}):
        file_path = f"{template_name}.html"

        with open(file_path) as file_pointer:
            template  =  file_pointer.read()

            for key ,val in context.items():
                print(key,val)
                template = re.sub(r'{{\s*' + re.escape(key) + r'\s*}}',str(val),template)
        self.headers.append(('Content-Type',"text/html"))
        self.text = template
        self.status_code = "200 OK"
        
    