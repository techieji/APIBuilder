import json
from bottle import Bottle, request
import requests
import pickle

class WebAPI:
    def __init__(self, app=None):
        if app == None:
            self.app = Bottle()
        else:
            self.app = app

    def add_api(self, label=''):
        def dec(fn):
            @self.app.post('/' + label)
            def f():
                j = json.loads(request.json)
                return json.dumps(fn(j))
            return f
        return dec

    def configure(self, **kwargs):
        self.kwargs = kwargs
        kws = {}
        if "host" in kwargs.keys():
            kws["host"] = kwargs["host"]
        elif "port" in kwargs.keys():
            kws["port"] = kwargs["port"]
        self.client = Client(**kws)

    def run(self, **kwargs):
        if kwargs:
            try:
                self.kwargs.update(kwargs)
            except:
                self.kwargs = kwargs
            print("\u001b[31mWarning: please use configure instead of directly passing arguments. \u001b[37m")
        self.app.run(**self.kwargs)

class Client:
    def __init__(self, host="localhost", port=8080, schema="http"):
        self.host = host
        self.port = port
        self.schema = schema

    def __str__(self): return f"Client(url={self.schema}://{self.host}:{self.port})"
    def __repr__(self): return self.__str__()
    def __reduce(self): return (self.__class__, (self.host, self.port))

    def send(self, req, label=""):
        j = json.dumps(req)
        res = requests.post(f"{self.schema}://{self.host}:{self.port}/{label}", json=j)
        return res.json()

def main():
    w = WebAPI()
    w.add_api()(lambda x: {1: 2})
    w.configure(port=8080, host="192.168.1.226", reloader=True)
    with open("client.bin", "bw") as f:
        pickle.dump(w.client, f)
    w.run()

if __name__ == "__main__":
    main()
