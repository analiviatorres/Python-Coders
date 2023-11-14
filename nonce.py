import time
def findNonce(dataToHash, bitsToBeZero): #o dataToHash será usado para calcular o hash e o bitsToBeZero será os bits iniciais

    #bitsToBeZero = input("Digite uma quantidade de bits em zero")
    nonce = 4 #iniciando o nonce com determinado valor
    tempoInicial = tempoAtual() #essa variável tempoInicial será usada mais a frente para calcular o tempo de execução do loop

    bitsToBeZero = int(bitsToBeZero)

    while True: #inicio do loop
        dados = nonce.to_bytes(4, 'big') + dataToHash.encode('utf-8')#aqui iremos converter o valor inicial do nonce em 4 bytes e concatenar com os dados originais do dataToHash, formando um novo conjunto de dados
        hash_resultante = calcularHash(dados)
        numZeros_iniciais = contarZeros(hash_resultante)

        if numZeros_iniciais >= bitsToBeZero:
            tempoFinal = tempoAtual()
            tempoDecorrido = tempoFinal - tempoInicial
            return nonce, tempoDecorrido
        nonce += 1
        

#o código abaixo vai calcular os dados do hash
def calcularHash(dados):
    def rotr(x, n, b):
        return ((x >> n) | (x << (b - n))) & 0xFFFFFFFF

    def ch(x, y, z):
        return (x & y) ^ (~x & z)

    def maj(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    def sigma0(x):
        return rotr(x, 2, 32) ^ rotr(x, 13, 32) ^ rotr(x, 22, 32)

    def sigma1(x):
        return rotr(x, 6, 32) ^ rotr(x, 11, 32) ^ rotr(x, 25, 32)

    def gamma0(x):
        return rotr(x, 7, 32) ^ rotr(x, 18, 32) ^ (x >> 3)

    def gamma1(x):
        return rotr(x, 17, 32) ^ rotr(x, 19, 32) ^ (x >> 10)

    # Inicialize os valores iniciais do hash (H)
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    # Defina constantes K
    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    # Preparar mensagem (dados para hash)
    mensagem = bytearray(dados)
    resultado = (h0 << 128) | (h1 << 96) | (h2 << 64) | (h3 << 32) | h4

    return resultado.to_bytes(32, 'big')  # Retorne o hash como um conjunto de bytes




def contarZeros(hash_resultante):
    num_zeros = 0 #a variável num_zeros está sendo usada para manter a contagem de número dos bits em zero
    for byte in hash_resultante: #loop que vai itera cada byte condtido em hash_resultante
        for i in range(8):
            if (byte >> (7 - i)) & 1 == 0: #verificando o bit atual no byte utilizando a função bitwise
                num_zeros += 1 #caso o bit atual seja zero será incrementado 1
            else:
                return num_zeros
    return num_zeros #caso o loop termine em um bit não-zero, a função vai retornar o valor total de num_zeros.


#a função tempoAtual está sendo usada para retornar o valor atual do tempo em segundos, que é obtido em time.perf_counter()
def tempoAtual():
    return time.perf_counter()

bitsToBeZero = int(input("Digite a quantidade de bits iniciais em zero: "))
dataToHash = input("Digite o texto a validar: ")
nonceEncontrado, tempoGasto = findNonce(dataToHash, bitsToBeZero)
print(f"Nonce encontrado: {nonceEncontrado}")
print(f"Tempo levado: {tempoGasto} segundos")
print(contarZeros)


