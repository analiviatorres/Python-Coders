import socket 
import time

class cliente_HTTP: #definindo a classe que representará o cliente HTTP
    def __init__(self, host, port=80): #o __init__ está sendo usado para chamar os objetos criados na classe
        self.host = host #atribuindo os parâmetros de host aos atributos de self.host
        self.port = port #atribuindo os parâmetros de port aos atributos de self.port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #aqui está sendo criado um atributo que armazenará as informações do socket

    def connect(self):
        self.sock.connect((self.host, self.port))

    def send_request(self, metodo, solicitacao, cabecalho=None):
        cabecalho = cabecalho or {}
        requisicao_line= f"{metodo} {solicitacao} HTTP/1.1\r\n"
        cabecalho_host = f"Host:{self.host}\r\n"
        cabecalho_str = "\r\n".join(f'{k}: {v}' for k, v in cabecalho.items()) + "\r\n"  
        requisicao = f"{requisicao_line}{cabecalho_host}{cabecalho_str}\r\n"
        self.sock.send(requisicao.encode())
        time.sleep(3)

    def resposta(self, tamanho=4096):
        data = b""
        while True:
            chunk = self.sock.recv(tamanho)
            if not chunk:
                break
            data += chunk
        return data
    
    def close(self):
        self.sock.close()

cliente = cliente_HTTP("httpbin.org")
cliente.connect()

cliente.send_request("GET", "/image/jpeg")
resposta_dado = cliente.resposta()

pos_cabecalho = resposta_dado.find(b"\r\n\r\n")
metadados = resposta_dado[:pos_cabecalho]
for metadado in metadados.split(b"\r\n"):
    print(metadado)


arquivo = open("dados.bin", "wb")
arquivo.write(resposta_dado)
arquivo.close()

cliente.close()

