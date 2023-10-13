nome_origem = (input("Digite uma palavra para criptografar: ")) #recebe a palavra ou frase do usuário
passe = input("Digite agora uma palavra passe: ") #recebe a palavra-chave
destino = [] #a palavra criptografada será inserida nessa lista ao final

if not passe:
    print("A palavra passe não pode estar vazia! ") #verifica se a palavra passe está vazia.
else: 

    for decripto, cripto in enumerate(nome_origem): #o enumerate obtem os indices das variáveis cripto e decripto
        n_origem = ord(cripto) #ord converte os caracteres da variável cripto para ascii e os armazena em n_origem
        n_passe = ord(passe[decripto % len(passe)]) # o "%" calcula o índice da palavra-passe, assim, garantindo que ela seja repetida quantas vezes necesária para criptografar todos os caracteres. 
        # "len(passe)" retorna o comprimento da palavra-passe, garantindo que a palavra passe não seja menor que a palavra de origem.
        resultado = chr(n_origem ^ n_passe) # o chr retorna o resultado XOR em ASCII das duas palavras
        destino.append(resultado) #incrementantando o resultado dentro da lista destino.

print(f"O resultado das duas palavras combinadas é: {destino}")