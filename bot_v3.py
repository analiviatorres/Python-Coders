from flask import Flask, request, jsonify
import requests
import socket

#usando o flask para criar o webhook do bot do telegram.
app = Flask(__name__) # a variável "app" é o padrão usado nesse tipo de código.

token = "6461998796:AAFLpQNPx4rFTmOFs-PdJk2O_GqkQzxnWAY" #token do bot do telegram.
api_url = f"https://api.telegram.org/bot{token}" #endereçoi da API do telegram.
url_webhook = "https://999f-187-19-156-117.ngrok-free.app" #endereço que o aplicativo do ngrok disponibiliza após ser executado no computador(obs: esse endereço muda todas as vezes que programa é executado.).


# Configuração do webhook que é executada após o inicio do aplicativo do flask, "app".
def telegram_webhook(): #função que vai executar o webhook
    url = f"{api_url}/setWebhook?url={url_webhook}/webhook" # url que interliga a API do telegram e o programa "Ngrok" e faz a rota de comuniação.
    response = requests.get(url) #fazendo solicitação "GET".
    return response.json() #retornando os dados em JSON e transformando-os em um objeto python.

users_registered = []

# Lógica para processar mensagens recebidas
def register_user(dados): #A função "register_user" recebe um argumento chamado "dados", que é onde está localizado as informações recebidas pelo bot.
    chat_id = dados['message']['chat']['id'] #Aqui está sendo extraido o "id" do chat da mensagem recebida.
    text_received = dados['message']['text'] #aqui está sendo extraido a mensagem do usuário.
    print(text_received)
    if text_received.startswith("/name "):
        # Verifica se há pelo menos dois elementos após a divisão
        name_parts = text_received.split("/name ")
        if len(name_parts) > 1:
            user_name = name_parts[1]
            users_registered.append({chat_id: user_name})
            response_message = f"Olá, {user_name}! Você foi Registrado com Sucesso!"
            send_message(chat_id, response_message)
        else:
            response_message = "Por favor, use o comando '/name' seguido do seu nome para se registrar."
            send_message(chat_id, response_message)
    
    elif text_received == "/start": 
        users_registered = any(chat_id in user.keys() for user in users_registered)
        if users_registered:
            welcome_message = ("Bem-vindo ao bot Scooby-doo! 🤖\n"
                           "Digite '/info' para saber mais informações sobre mim! \n"
                           "Digite '/ip' para saber seu IP! \n"
                           "Digite '/sair' para encerrar o chat! \n")
            send_message(chat_id, welcome_message) #chamando a função "send_message" para enviar a mensagem de forma mais automática ao "chat_id".
        else:
            response_message = "Por favor, use o comando '/name' seguido do seu nome para se registrar. "
            send_message(chat_id, response_message)
    elif text_received.lower() == "/info": #caso a condição anterior não seja atendida, será verificado se a resposta é "um".
        response_message = "Olá, me chamo Scooby-doo,sou um BOT que investigativo e possuo algumas habilidades! Como descobrir qual é o seu indereço IP, serviço de DNS e mais! "
        send_message(chat_id, response_message)
    elif text_received.lower() == "/ip":
        ip_address = obter_ip()
        response_message = f"Seu endereço IP é: {ip_address}"
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

def obter_ip():
    try:
        host_name = socket.gethostname()
        ip_address = socket.gethostbyname(host_name)
        return ip_address
    except Exception as e:
        return f"Erro ao tentar obter endereço IP: {e}"
    

# Rota do webhook
@app.route('/webhook', methods=['POST']) #aqui é usado um tipo de decorator que mapeia a função "webhook" criada logo a baixo.
#esse decorator é o que vai permitir a comunicação de forma "sincrona", pois é o que o telegram usará para enviar as atualizações.
def webhook(): #essa função, "webhook" será usada para quando for usado a solicitações POST.
    dados = request.get_json() #os dados extraidos da solicitação JSON, serão adicionados a variável "dados"
    register_user(dados) #Aqui é chamado a função "process_message"para as informações do "dados" serem processadas.
    return jsonify()

if __name__ == '__main__': #essa condição verifica se o script está sendo executado.
    telegram_webhook() #chamando a função que está configurada no webhook a cima.
    app.run(port=5000) # Inicia o servidor na porta 5000
