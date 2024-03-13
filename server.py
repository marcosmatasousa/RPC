from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

class Client:
    def __init__(self, name : str, cpf : str, age : int) -> None:
        self.name = name
        self.cpf = cpf
        self.age = age

class DB:
    def __init__(self) -> None:
        self.clients = []

    def cpf_exists(self, cpf : str):
        for client in self.clients:
            if client.cpf == cpf:
                return True
        return False
            
    def register_client(self, client : Client):
        if not self.cpf_exists(client.cpf):
            self.clients.append(client)
            return "Client {} registered.".format(client.name)
        return "Could not register client {}, CPF already exists".format(client.name)
    
    def get_client(self, cpf : str):
        for client in self.clients:
            if client.cpf == cpf:
                return client
        return None
    
    def get_average_age(self):
        sum = 0
        for client in self.clients:
            sum += client.age
        return sum / len(self.clients)
        
# Restringe as solicitações para um caminho específico
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Criação do servidor
with SimpleXMLRPCServer(('localhost', 8080),
                        requestHandler=RequestHandler) as server:
    
    data_base = DB()

    # Função remota que você deseja registrar
    def register_client(name : str, cpf : str, age : int):
        return data_base.register_client(Client(name, cpf, age))
    
    def get_client(cpf : str):
        return data_base.get_client(cpf)
    
    def get_average_age():
        return data_base.get_average_age()

    # Registrando a função no servidor
    server.register_function(register_client, 'register_client')
    server.register_function(get_client, 'get_client')
    server.register_function(get_average_age, "get_average_age")
    server.register_multicall_functions()

    print("Servidor RPC ativo na porta 8080...")
    # Aguarda por solicitações infinitamente
    server.serve_forever()