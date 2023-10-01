import csv

arquivo = open("/home/livia/Área de trabalho/eleicao_acre.csv", "r", encoding="ISO-8859-1")
lendo_dados = []

for linha in arquivo:
    elementos = [e.strip() for e in linha.split(";")]
    for linha in arquivo:
            cargo = linha[17]
            nome_candidato = linha[30]
            votos = linha[31]
        
        # Verifique se o cargo é "Presidente"
            if cargo == "Presidente":
            # Atualize a contagem de votos para o candidato
                if nome_candidato in lendo_dados:
                    lendo_dados[nome_candidato] += votos
                else:
                    lendo_dados[nome_candidato] = votos

# Encontre o candidato a presidente com mais votos
candidato_mais_votado = max(lendo_dados, key=lambda x: votos[x])
total_votos = lendo_dados[candidato_mais_votado]

print(f"O candidato a Presidente com mais votos foi: {candidato_mais_votado} com {votos} votos.")

arquivo.close()

print(lendo_dados)