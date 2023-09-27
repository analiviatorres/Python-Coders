nome_origem = (input("Digite uma palavra para criptografar: "))
passe = (input("Digite agora uma palavra passe: "))
destino = []

if not passe:
    print("A palavra passe não pode estar vazia! ")
else: 

    for decripto, cripto in enumerate(nome_origem): #o enumerate obtem os indices das variáveis cripto e decripto
        n_origem = ord(cripto) #ord converte os caracteres da variável cripto para ascii e os armazena em n_origem
        n_passe = ord(passe[decripto % len(passe)]) # vamos calcular e verificar se a palavra recebida em passe é menor que a recebida em nome_origem
        resultado = chr(n_origem ^ n_passe) # o chr retorna o resultado XOR em ASCII
        destino.append(resultado)

        resultado_descriptografado = chr(ord(resultado) ^ n_passe)
        resultado_completo_descriptografado = ''.join(resultado_descriptografado)

print(f'O resultado das duas palavras combinadas é: {destino}')
print((f'Resultado descriptografado: {resultado_completo_descriptografado}'))

