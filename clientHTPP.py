import socket 
import time

class cliente_HTTP: #definindo a classe que representará o cliente HTTP
    def __init__(self, host, port=80): #o __init__ está sendo usado para chamar os objetos criados na classe
        self.host = host #atribuindo os parâmetros de host aos atributos de self.host
        self.port = port #atribuindo os parâmetros de port aos atributos de self.port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #aqui está sendo criado um atributo que armazenará as informações do socket

    def connect(self): #o método connect está fazendo a conexão com o serviodor remoto, utilizando os parâmetros passado a cima
        self.sock.connect((self.host, self.port))

    #a função send_request está fazendo a solicitação HTTP para o servidor, ela possui alguns parâmetros:
    def send_request(self, metodo, solicitacao, cabecalho=None, dados=None): #foi passado os argumentos "None" para caso nenhum valor seja passado os dicionários a seguir estejam vazios.
        #as duas linhas a seguir, "cabecalho" e "dados" se forem "None" será atribuido um dicionário e uma string vázia, para evitar erros caso não seja fornecido valores.
        cabecalho = cabecalho or {} #
        dados = dados or b""

        requisicao_line= f"{metodo} {solicitacao} HTTP/1.1\r\n" #criando a solicitação e passando os parâmetros
        cabecalho_host = f"Host:{self.host}\r\n" #usando f-string para passar os parâmetros do Host
        cabecalho_str = "\r\n".join(f'{k}: {v}' for k, v in cabecalho.items()) + "\r\n" #usando expressões geradora para passar os parâmetros do cabeçalho, os trecho "for k, v in cabecalho.item" servem para pegar as chaves e valores do cabeçalho
        requisicao = f"{requisicao_line}{cabecalho_host}{cabecalho_str}\r\n" #aqui concatetamos todos os valores para formar a solicitação completa
        
        #Abaixo foi criado uma condição que verifica se existem dados incluidos no corpo da solicitação, se hopuver, será adicionado ao "Content-Lenght"
        if dados:
            requisicao += "Content-Length: {len(dados)}\r\n\r\n"
            requisicao += dados.decode()

        #criado um bloco de exceção para evitar problemas com a conexão do servidor, caso seja fechada antes da hora.
        try:
            self.sock.send(requisicao.encode())
        except BrokenPipeError as ERROR:
                print(f"Erro ao enviar a requisição: {ERROR}")


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

#fazendo a solicitação com o método GET
cliente.send_request("GET", "/image/jpeg")
resposta_dado = cliente.resposta()

#fazendo a solicitação com o método POST
cliente.send_request("POST", "/post", dados=b"https://httpbin.org/post")
resposta_dado = cliente.resposta()
#print(resposta_dado.decode("utf-8"))

#fazendo a solicitação com o método PUT
cliente.send_request("PUT", "/put", dados=b"https://httpbin.org/put")
resposta_dado = cliente.resposta()
#print(resposta_dado)

#fazendo a solicitação com o método PATCH
cliente.send_request("PATCH", "/patch", dados=b"https://httpbin.org/patch")
resposta_dado = cliente.resposta()

#fazendo a solitação com o método DELETE
cliente.send_request("DELETE", "/delete", dados=b"https://httpbin.org/delete")
resposta_dado = cliente.resposta()
print(resposta_dado)

pos_cabecalho = resposta_dado.find(b"\r\n\r\n")
metadados = resposta_dado[:pos_cabecalho]
for metadado in metadados.split(b"\r\n"):
    print(metadado)


arquivo = open("dados.bin", "wb")
arquivo.write(resposta_dado)
arquivo.close()

cliente.close()

