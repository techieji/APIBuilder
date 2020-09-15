from WebAPI import *
import pickle

with open("client.bin", "br") as f:
    c = pickle.load(f)

print(c)
res = c.send({})
print(res)
