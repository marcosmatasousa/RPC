from xmlrpc.client import ServerProxy
import json

# Conecta ao servidor RPC
server = ServerProxy('http://localhost:8080/RPC2')

with open('names.txt', 'r') as file:
    for line in file:
        data = line.split(" ")
        result = server.register_client(data[0], data[1], int(data[2]))
        print(result)
        
average_age = server.get_average_age()
print("Average age is {}".format(int(average_age)))