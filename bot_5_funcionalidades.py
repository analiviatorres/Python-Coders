from flask import Flask, request, jsonify
import requests
import socket

# Usando o flask para criar o servidor local do bot.
app = Flask(__name__) # a variável "app" é o padrão usado nesse tipo de código.

token = "" #token do bot do telegram.
api_url = f"https://api.telegram.org/bot{token}" #endereço da API do telegram.
url_webhook = "" #endereço que o aplicativo do ngrok disponibiliza após ser executado no computador(obs: esse endereço muda todas as vezes que programa é executado).

# Configuração do webhook que é executada após o inicio do aplicativo do flask, "app".
def telegram_webhook(): #função que vai executar o webhook
    url = f"{api_url}/setWebhook?url={url_webhook}/webhook" # url que interliga a API do telegram e o programa "Ngrok" e faz a rota de comuniação.
    response = requests.get(url) #fazendo solicitação "GET".
    return response.json() #retornando os dados em JSON e transformando-os em um objeto python.

# Lista que vai armazenar o nome recebido pelos usuários.
users_registered = []

# Lógica para processar mensagens recebidas
def process_message(dados):
    name_id = dados["message"]["from"]["first_name"] #A função "process_message" recebe um argumento chamado "dados", que é onde está localizado as informações recebidas pelo bot.
    chat_id = dados['message']['chat']['id'] #Aqui está sendo extraido o "id" do chat da mensagem recebida.
    text_received = dados['message']['text'] #aqui está sendo extraido a mensagem do usuário.

    #Aqui será criado um fluxo de interação pré-determinado entre o bot e o usuário.
    if text_received == "/start": # A palavra "/start" será o gatilho da interação.
        welcome_message = ("Bem-vindo ao bot Scooby-doo! 🤖\n"
                           "Digite '/info' para saber mais informações sobre mim! \n"
                           "Digite '/name' para saber qual é seu nome de usuário do Telegram! \n"
                           "Digite '/ip' para eu te mostrar o meu endereço IP! \n"
                           "Digite '/image' para eu te enviar uma foto minha :) \n"
                           "Digite '/sair' para encerrar o chat! \n")
        send_message(chat_id, welcome_message) #chamando a função "send_message" para enviar a mensagem de forma mais automática ao "chat_id".
    #Abaixo uma serie de condições para cada solicitação do usuário.
        #Enviando as informações sobre o BOT.
    elif text_received.lower() == "/info":
        response_message = "Olá, eu sou o BOT Scooby-doo! Possuo algumas habilidade legais, posso te mostrar meu endereço IP, descobrir seu nome de usuário e mais!  "
        send_message(chat_id, response_message)

        #Enviando o nome do usuário conforme configurado no telegram e o adicionando a uma lista.
    elif text_received.lower() == "/name":
        response_message = f"Seu nome de usuário é: {name_id}! e ele foi adicionado ao nosso banco de dados."
        send_message(chat_id, response_message)
        users_registered.append(name_id)

        #Enviando o endereço IP do BOT.
    elif text_received.lower() == "/ip":
        response_message = f"Meu endereço IP é: {get_ip()}"
        send_message(chat_id, response_message)

        #Enviando uma foto do BOT para o usuário.
    elif text_received.lower() == '/image':
        photo_path = get_image()
        response_message = "Aqui está a foto:"
        send_message(chat_id, response_message)
        send_photo(chat_id, photo_path)

        #Finalizando a interação.
    elif text_received.lower() == "/sair": 
        response_message = "Você escolheu SAIR. Até a próxima! 🤖" 
        send_message(chat_id, response_message)

        #lidando com outras mensagens do usuário.
    else:
        response_message = "Comando não reconhecido. Digite '/info' para saber mais sobre mim ou '/sair' para encerrar o chat."
        send_message(chat_id, response_message)

# Função que processa a lógica para envio da mensagem.
def send_message(chat_id, text): # a função possui dois parâmetros, "chat_id" que é o identificador do usuário e "text" que será e mensagem enviada.
    url = f"{api_url}/sendMessage" #usando f-string para construir o endereço da url juntamente com o endpoint, que é o "sendMessage".
    send_dados = {"chat_id": chat_id, "text": text} # "send_dados" é um dicionário que será enviado no corpo da solicitação.
    response = requests.post(url, json=send_dados) #criando a solicitação POST.
    return response.json()

# Função que envia uma foto para o usuário usando a API do Telegram.
def send_photo(chat_id, photo_path): #chat_id e photo_path, são parâmetros que representam o identificador do chat para o qual a foto será enviada e o caminho do arquivo da foto, respectivamente.
    url = f"{api_url}/sendPhoto" #endereço da API do Telegram usando o comando sendPhoto para enviar a imagem.
    files = {'photo': open(photo_path, 'rb')} #abrindo a imagem.
    params = {'chat_id': chat_id} #parâmtros da requisição.

    response = requests.post(url, params=params, files=files) #enviando a requisição.
     #verificando o status da requisição.
    if response.status_code == 200:
        return 'ok'

# Função que cria um socket e coleta o IP do host.
def get_ip():
    try:
        conect_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #criando um socket do tipo UDP.
        conect_socket.connect(("8.8.8.8", 80)) #Conectando o socket a um endereço IP externo, Isso é feito para garantir que o socket esteja associado a uma interface de rede.
        address_ip = conect_socket.getsockname()[0] #usando o método "getsockname" para pegar o IP associado ao host, ele usa uma tupla que extrai esse dado.
        return address_ip
        #Realizando tratamento de erros.
    except OSError as e:
        return f"Erro ao obter endereço IP: {e}"
    finally: #finalizando a conexão do socket.
        conect_socket.close()
# Função que vai retorna o caminho do arquivo, a foto do BOT.
def get_image():
    try:
        photo_path = "C:\\Users\\livia\\Desktop\\server\\image_scooby.jpg"
        return photo_path
    except OSError as e:
        return f"Erro: {e}"

# Rota do webhook
@app.route('/webhook', methods=['POST']) #aqui é usado um tipo de decorator que mapeia a função "webhook" criada logo a baixo.
#esse decorator é o que vai permitir a comunicação de forma "sincrona", pois é o que o telegram usará para enviar as atualizações.
def webhook(): #essa função, "webhook" será usada para quando for usado a solicitações POST.
    dados = request.get_json() #os dados extraidos da solicitação JSON, serão adicionados a variável "dados"
    process_message(dados) #Aqui é chamado a função "process_message"para as informações do "dados" serem processadas.
    return jsonify()

if __name__ == '__main__': #essa condição verifica se o script está sendo executado.
    telegram_webhook() #chamando a função que está configurada no webhook a cima.
    app.run(port=5000) # Inicia o servidor na porta 5000.
