import csv

arquivo = open("//home//livia//Área de trabalho//eleicao_acre.csv", "r", encoding="ISO-8859-1")

lendo_votos = {}

for linha in arquivo:
    elementos = [e [1: -1] for e in linha.split(";")]
    #lendo_dados.append([elementos[12], elementos[17],])
    #candidato_presidente = list(filter(lambda x: elementos.index(x) in [31], elementos))

    candidato_presidente = elementos[31]
    if candidato_presidente in lendo_votos:
        lendo_votos[candidato_presidente] += 1
    else:
        lendo_votos[candidato_presidente] = 1

arquivo.close()

candidato_presidente_max = max(candidato_presidente, key=lambda x: lendo_votos[x])
resultado_presidente = lendo_votos[candidato_presidente]
print(f"O candidato a presidente com mais votos foi: {candidato_presidente_max} com {resultado_presidente} votos")



#print(lendo_dados)