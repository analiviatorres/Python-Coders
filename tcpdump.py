capture = open("/home/livia/capture.cap", "rb") #lendo o arquivo em modo binário, (rb).
dado = capture.read(16) #lendo os próximos 16 bytes e armazenando em "dado"

while dado!= b"": #loop que será repetido enquanto dado não for vázio
    versao = (dado[0] >> 4) & 0xF #verificando a versão do pacote, o 0xF mantém os 4 bits mais significativos e redefine os 4 bits menos significativo
    ihl = dado[0] & 0xF #lendo o tamanho do cabeçalho 
    tos = dado[1] #verificando o tipo de serviço
    comprimento = int.from_bytes(dado[2:4], byteorder="big") #lendo o tamanho total do pacote, TotalLength
    identificador = int.from_bytes(dado[4:6], byteorder="big") #lendo os fragmentos do datagrama do IP original
    flags = (dado[6] >> 5) & 0x7 #o operador AND máscara os 3 bits mais significado e descarta os outros bits, o 0x7 mantém os 3 bits mais significativo e redefine os outros bits para zero.
    offset = ((dado[6] & 0x1F) << 8 ) + dado[7] #coletando os dados do fragmento atual do pacote, "dado[6] & 0x1F" mascara os 6 bits mais significativos"
    ttl = dado[8] #coletando o tempo de vida do pacote
    protocolo = dado[9]
    checksum = int.from_bytes(dado[10:12], byteorder="big") #lendo as informações do checksum do pacote
    src_ip = ".".join(map(str, dado[12:16])) #o map aplica a todos os itens de "dado" a função string, o join é usado para separar os elementos com o "." e ficar mais fácil a compreensão
    dst_ip = ".".join(map(str, dado[16:20]))

    print(f"A versão do pacote é:{versao}, o tamanho é: {ihl}, O tipo de serviço: {tos},  o tamanho total: {comprimento}, a identificação: {identificador}, as flags: {flags}, o fragmento offset: {offset}, o tempo de vida: {ttl}, o protocolo é: {protocolo}, o checksum{checksum}, IP de origem{src_ip} e o IP de destino: {dst_ip} ")
    dado = capture.read(16)

#-lendo em qual momento inicia e termina a captura do pacote---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def timestamp(capture):
    timestamp_bytes = capture.read(4) #lendo o timestamp do pacote em segundos
    if not timestamp_bytes:
        return None
        
    timestamp = int.from_bytes(timestamp_bytes, byteorder="big")
    return timestamp

def main():
    packetList = []  #lista para armazenar informações de cada pacote

    capture = open("/home/livia/capture.cap", "rb")  #abrindo o arquivo de captura

    while True: #iniciando a leitura dos pacotes com o loop
        inicioTamp = timestamp(capture) #lendo o timestamp do inicio do pacote e atribuindo a "inicioTamp"

        if inicioTamp is None: #caso não haja mais timesTamp a serem lidos, sairemos do loop com o break
            break

        deltaTime = capture.read(4)  #lendo o campo "Delta Time" que está nós próximos 4 bytes do pacote

        if not deltaTime: #caso o delta time seja vazio, paramos com o break
            break

        deltaBytes = int.from_bytes(deltaTime, byteorder="big")  # Converte o campo "Delta Time" de bytes para inteiros

        endTime = inicioTamp + deltaBytes #somando o inicio e o fim da captura do pacote

        packet_info = { #iniciando um dicionário que contém as chaves, inicioTamp, delta_time e endTime e relacionando as respectivas variáveis
                "inicioTamp": inicioTamp,
                "delta_time": deltaBytes,
                "endTime": endTime
            }

        packetList.append(packet_info) #adicionando as informações do pacote a lista packetList.

    for i, packet in enumerate(packetList): #percorrente a lista e atribuindo-a ao dicionário packet, o enumerate obtém o índice de cada dicionário.
        print(f"Pacote {i + 1}:") #aqui vamos imprimir o respectivo número do pacote
        print(f"Início da captura: {packet['inicioTamp']}") #imprimindo o tempo do inicio do pacote
        print(f"Término da captura: {packet['endTime']}")
        print("\n")

    capture.close()  # Fecha o arquivo de captura

if __name__ == "__main__": #para que o código seja executado como script e não um módulo, usei essa construção IF
    #o trecho main, está sendo usado como uma função que contém o código principal. 
    main()