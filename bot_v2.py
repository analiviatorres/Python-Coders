from flask import Flask, request, jsonify
import requests
import time

#usando o flask para criar o webhook do bot do telegram.
app = Flask(__name__) # a variável "app" é o padrão usado nesse tipo de código.

token = "" #token do bot do telegram.
api_url = f"https://api.telegram.org/bot{token}" #endereçoi da API do telegram.
url_webhook = "" #endereço que o aplicativo do ngrok disponibiliza após ser executado no computador(obs: esse endereço muda todas as vezes que programa é executado.).

# Configuração do webhook que é executada após o inicio do aplicativo do flask, "app".
def telegram_webhook(): #função que vai executar o webhook
    url = f"{api_url}/setWebhook?url={url_webhook}/webhook" # url que interliga a API do telegram e o programa "Ngrok" e faz a rota de comuniação.
    response = requests.get(url) #fazendo solicitação "GET".
    return response.json() #retornando os dados em JSON e transformando-os em um objeto python.

users_registered = []
# Lógica para processar mensagens recebidas
def process_message(dados):
    name_id = dados["message"]["from"]["first_name"] #A função "process_message" recebe um argumento chamado "dados", que é onde está localizado as ifnormações recebidas pelo bot.
    chat_id = dados['message']['chat']['id'] #Aqui está sendo extraido o "id" do chat da mensagem recebida.
    text_received = dados['message']['text'] #aqui está sendo extraido a mensagem do usuário.

    #Aqui será criado um fluxo de interação pré-determinado entre o bot e o usuário.
    if text_received == "/start": # A palavra "/start" será o gatilho da interação.
        welcome_message = ("Bem-vindo ao bot Scooby-doo! 🤖\n"
                           "Digite '/info' para saber mais informações sobre mim! \n"
                           "Digite '/name' para saber qual é seu nome de usuário do Telegram! \n"
                           "Digite '/sair' para encerrar o chat! \n")
        send_message(chat_id, welcome_message) #chamando a função "send_message" para enviar a mensagem de forma mais automática ao "chat_id".
    elif text_received.lower() == "/name":
        response_message = f"Seu nome de usuário é: {name_id}! e ele foi adicionado ao nosso banco de dados."
        send_message(chat_id, response_message)
        users_registered[chat_id] = name_id
    elif text_received.lower() == "/info": #caso a condição anterior não seja atendida, será verificado se a resposta é "um".
        response_message = "Olá, me chamo Scooby-doo,sou um BOT investigador e possuo algumas habilidades! Como descobrir qual é o seu indereço IP, serviço de DNS e mais! "
        send_message(chat_id, response_message)
    elif text_received.lower() == "/sair": #caso a condição anterior não seja atendida, será verificado se a resposta é "dois".
        response_message = "Você escolheu SAIR. Até a próxima! 🤖" 
        send_message(chat_id, response_message)
    else:
        #lidando com outras mensagens do usuário.
        response_message = "Comando não reconhecido. Digite '/info' para saber mais sobre mim ou '/sair' para encerrar o chat."
        send_message(chat_id, response_message)

# Função que processa a lógica para envio da mensagem.
def send_message(chat_id, text): # a função possui dois parâmetros, "chat_id" que é o identificador do usuário e "text" que será e mensagem enviada.
    url = f"{api_url}/sendMessage" #usando f-string para construir o endereço da url juntamente com o endpoint, que é o "sendMessage".
    send_dados = {"chat_id": chat_id, "text": text} # "send_dados" é um dicionário que será enviado no corpo da solicitação.
    response = requests.post(url, json=send_dados) #criando a solicitação POST.
    return response.json()

# Rota do webhook
@app.route('/webhook', methods=['POST']) #aqui é usado um tipo de decorator que mapeia a função "webhook" criada logo a baixo.
#esse decorator é o que vai permitir a comunicação de forma "sincrona", pois é o que o telegram usará para enviar as atualizações.
def webhook(): #essa função, "webhook" será usada para quando for usado a solicitações POST.
    dados = request.get_json() #os dados extraidos da solicitação JSON, serão adicionados a variável "dados"
    process_message(dados) #Aqui é chamado a função "process_message"para as informações do "dados" serem processadas.
    return jsonify()

if __name__ == '__main__': #essa condição verifica se o script está sendo executado.
    telegram_webhook() #chamando a função que está configurada no webhook a cima.
    app.run(port=5000) # Inicia o servidor na porta 5000
