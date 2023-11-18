#importando as bibliotecas
import socket 
import ssl 
import time

class cliente_HTTP: #definindo a classe que representará o cliente HTTP
    def __init__(self, host, port=443): #o __init__ está sendo usado para chamar os objetos criados na classe
        self.host = host #atribuindo os parâmetros de host aos atributos de self.host
        self.port = port #atribuindo os parâmetros de port aos atributos de self.port
        self.sock = None
        self.context = ssl.create_default_context()
        
    
    def conectar(self): #o método conectar está fazendo a conexão com o servidor remoto, utilizando os parâmetros passado a cima
        self.sock = socket.create_connection((self.host, self.port))
        self.sock = self.context.wrap_socket(self.sock, server_hostname=self.host)


    #a enviar_solicitacao está fazendo a solicitação HTTP para o servidor, ela possui alguns parâmetros:
    def enviar_solicitacao(self, metodo, solicitacao, cabecalho=None, dados=None): #foi passado os argumentos "None" para caso nenhum valor seja passado os dicionários a seguir estejam vazios.
        #as duas linhas a seguir, "cabecalho" e "dados" se forem "None" será atribuido um dicionário e uma string vázia, para evitar erros caso não seja fornecido valores.
        cabecalho = cabecalho or {} #
        dados = dados or b""

        requisicao_line= f"{metodo} {solicitacao} HTTP/1.1\r\n" #criando a solicitação e passando os parâmetros
        cabecalho_host = f"Host:{self.host}\r\n" #usando f-string para passar os parâmetros do Host
        cabecalho_str = "\r\n".join(f'{k}: {v}' for k, v in cabecalho.items()) + "\r\n" #usando expressões geradora para passar os parâmetros do cabeçalho, os trecho "for k, v in cabecalho.item" servem para pegar as chaves e valores do cabeçalho
        requisicao = f"{requisicao_line}{cabecalho_host}{cabecalho_str}\r\n" #aqui concatetamos todos os valores para formar a solicitação completa
        
        #Abaixo foi criado uma condição que verifica se existem dados incluidos no corpo da solicitação, se houver, será adicionado ao "len_dados".
        if dados:
            requisicao += "len_dados: {len(dados)}\r\n\r\n"
            requisicao += dados.decode()

        #criado um bloco de exceção para evitar problemas com a conexão do servidor, caso seja fechada antes da hora.
        try:
            self.sock.send(requisicao.encode())
            time.sleep(3)
        except ssl.SSLEOFError: #criado esse exceção para reconectar ao servidor após alguma falha.
                print("Reconectando...")
                self.conectar()
                self.sock.send(requisicao.encode())
        except BrokenPipeError as e: #criando outra exceção para evitar a falta de conexão entre o socket.
                print(f"Erro ao enviar a requisição: {e}")


    def resposta(self, tamanho=4096): #função responsável por receber a resposta do servidor.
        data = b"" #iniciando uma variável com uma sequência de bytes vázia, no qual será usada para adicionar os dados recebidos.
        while True:
            bloco_dados = self.sock.recv(tamanho) #recebe um bloco de dados do servidor de acordo com o tamanho especificado.
            if not bloco_dados: #verificando se o bloco de dados está vázio, se estiver, o loop é interrompido.
                break
            data += bloco_dados #adiciona os blocos recebidos a variável data.
        return data
    
    def close(self): #fechando a conexão com o socket.
        self.sock.close()

cliente = cliente_HTTP("httpbin.org") #criando a classe "cliente" que faz a conexão com o Host usando o método "conectar".
cliente.conectar()

#uma tupla contendo as requisições e abrindo um arquivo chamado "dados.bin"
solicitar_e_mostrar_resposta = [
    ("GET", "/image/jpeg"), #solicitação do tipo GET.
    ("POST", "/post", b"https://httpbin.org/post"), #solicitação do tipo POST.
    ("PUT", "/put", b"https://httpbin.org/put"), #solicitação do tipo PUT.
    ("PATCH", "/patch", b"https://httpbin.org/patch"), #solicitação do tipo PATCH.
    ("DELETE", "/delete", b"https://httpbin.org/delete") #solicitação DELETE.
]
arquivo = open("dados.bin", "wb") #abrindo o arquivo "dados.bin".

for metodo, solicitacao, *dados in solicitar_e_mostrar_resposta: #interando os elementos da tupla a cima sobre cada método de requisição, solicitação e os dados.
    cliente.enviar_solicitacao(metodo, solicitacao, dados=dados[0] if dados else None) #chamamos o método "enviar_solicitacao" na classe "cliente_HTTP" para enviar as solicitações ao servidor.
    resposta_dado = cliente.resposta() #adicionando as respostas do servidor na variável "resposta_dado".

    print(f"Resposta para {metodo} {solicitacao}:\n{'='*50}") #imprimindo a resposta de acordo com a solicitação que foi feita.
    
    arquivo.write(resposta_dado)#escrevendo a resposta do servidor no arquivo "dados.bin".
    print(f"Exibindo primeiros 100 bytes da resposta: {resposta_dado[:100]}") #exibindo apenas os 100 primeiros bytes do cabeçalho pois sem esse parâmetro a resposta fica sobrecarregada e gera erros.


arquivo.close() #fechando o arquivo "dados.bin".
cliente.close() #fechando a conexão com o servidor.

