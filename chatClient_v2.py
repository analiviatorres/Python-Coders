import requests
#Função responsável por enviar mensagem ao servidor.
def enviar_mensagem(mensagem):
    url = 'http://127.0.0.1:5000/enviar_mensagem' #URL do servidor juntamente com a rota.
    dados = {'mensagem': mensagem} #um dicionário que vai conter a mensagem enviada.

    response = requests.post(url, json=dados) #Fazendo a solicitação POST para o servidor.

    #Condição que verifica se a solicitação POST foi bem sucedida.
    if response.status_code == 200:
        resposta = response.json()
        print(f'Resposta do servidor: {resposta["resposta"]}')
    else:
        print(f'Erro ao enviar mensagem. Código de status: {response.status_code}')

#Função responsável por receber e imprimir a resposta vinda do servidor.
def receber_resposta():
    url = 'http://127.0.0.1:5000/receber_resposta' #URl do servidor, juntamente com a rota responsável por obter a resposta do servidor.
    
    #Fazendo uma solicitação GET para obter a resposta do servidor
    response = requests.get(url)

    #Condição que verifica a resposta do servidor.
    if response.status_code == 200:
        resposta = response.json()
        print(f'Mensagem do servidor: {resposta["mensagem"]}')
    else:
        print(f'Erro ao receber resposta do servidor. Código de status: {response.status_code}')

#Loop principal, que verifica as mensagens enviadas pelo cliente.
if __name__ == '__main__':
    while True:
        mensagem_para_enviar = input('Digite a mensagem a ser enviada para o servidor (ou "!q" para sair): ')
        enviar_mensagem(mensagem_para_enviar)
        
        #Se a mensagem começar com "!q" o chat será encerrado.
        if mensagem_para_enviar.startswith('!q'):
            print('Chat encerrado.')
            break

        receber_resposta()
