nome_origem = input("Digite uma palavra para criptografar: ")
passe = input("Digite agora uma palavra passe: ")
destino_criptografado = []
destino_descriptografado = []

if not passe:
    print("A palavra-passe não pode estar vazia! ")
else:
    for i, char in enumerate(nome_origem):
        n_origem = ord(char)
        n_passe = ord(passe[i % len(passe)])
        resultado_criptografado = chr(n_origem ^ n_passe)
        resultado_descriptografado = chr(ord(resultado_criptografado) ^ n_passe)

    destino_criptografado.append(resultado_criptografado)

    destino_descriptografado.append(resultado_descriptografado)
    print(resultado_criptografado)

    resultado_completo_criptografado = ''.join(destino_criptografado)
    resultado_completo_descriptografado = ''.join(destino_descriptografado)


    print(f'Resultado criptografado: {resultado_completo_criptografado}')
    print(f'Resultado descriptografado: {resultado_completo_descriptografado}')
