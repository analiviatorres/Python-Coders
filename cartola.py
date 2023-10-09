def dados_cartola(ano):
    try:
        # Abre o arquivo correspondente ao ano
        with open(f'/home/livia/Downloads/dados_cartola_fc/cartola_fc_{ano}.txt', 'r', encoding='utf-8') as arquivo:
            dados = arquivo.read()
        return dados
    except FileNotFoundError:
        return f"Arquivo de dados para o ano {ano} não encontrado."
    
ano_desejado = input("Digite o ano para acessar os dados (2021 ou 2022): ")

if ano_desejado in ['2021', '2022']:
    dados = dados_cartola(ano_desejado)
    if dados:
        print(f"Dados do Cartola para o ano {ano_desejado}:\n")
        #print(dados)
else:
    print("Ano inválido, digite 2021 ou 2022.")

esquema1 = ["3 zagueiro", "0 laterais", "4 meias", "3 atacantes"] #esquema 3-4-3
esquema2 = ["3 zagueiros", "0 laterais", "5 meias", "2 atacantes"] #esquema 3-5-2 
esquema3 = ["2 zagueiros", "2 laterais", "3 meias", "3 atacantes"] #esquema 4-3-3
esquema4 = ["2 zagueiros", "2 laterais", "4 meias", "2 atacantes"] #esquema 4-2-2 
esquema5 = ["2 zagueiro", "2 laterais", "5 meias", "1 atacantes"] #esquema 4-5-1
esquema6 = ["3 zagueiros", "2 laterais", "3 meias", "2 atacantes"] #esquema 5-3-2 
esquema7 = ["3 zagueiros", "2 laterais", "4 meias", "1 atacante"] #esquema 5-4-1
#print(f"Escolha agora um dos esquemas listados a seguir:\n Esquema 1:{esquema1}\n Esquema 2:{esquema2}\n Esquema 3:{esquema3}\n  Esquema 4:{esquema4}\n  Esquema 5:{esquema5}\n  Esquema 6:{esquema6}\n  Esquema 7:{esquema7}")

#def jogadores(esquemas):
    #selec_jogadores = [
        #{"posicoes": {"1": {"id": 1, "nome": "Goleiro", "abreviacao": "gol"}}},
        #{"posicoes": {"2": {"id": 2, "nome": "Lateral", "abreviacao": "lat"}}},
       # {"posicoes": {"3": {"id": 3, "nome": "Zagueiro", "abreviacao": "zag"}}},
       # {"posicoes": {"4": {"id": 4, "nome": "Meia", "abreviacao": "mei"}}},
       # {"posicoes": {"5": {"id": 5, "nome": "Atacante", "abreviacao": "ata"}}},
      #  {"posicoes": {"6": {"id": 6, "nome": "Tecnico", "abreviacao": "tec"}}}
   # ]
    
   # return selec_jogadores
esquema_selec = input("Escolha um dos esquemas mostrado! ")

esquemas = {
    '1': esquema1, '2': esquema2, '3': esquema3, '4': esquema4,
    '5': esquema5, '6': esquema6, '7': esquema7
}

if esquema_selec in esquemas:
    atletas_selecionados = jogadores(esquemas[esquema_selec])
    print("atletas_selecionados!" )
    for jogadores in atletas_selecionados:
        #print(f"{jogadores['posicoes']}, Nome Abreviado: {jogadores['apelido']}, Time: {jogadores['time']}, Pontuação Média: {jogadores['pontos_num']}")
        print(jogadores)
else:
    print("Esquema inválido.")
