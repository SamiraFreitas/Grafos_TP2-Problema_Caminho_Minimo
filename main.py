import os
import funcoes

ch = False
entrada = ''
print('\n-Informe o arquivo: ')
while not ch:
    entrada = input('\t arquivo: ')
    entrada = entrada +'.txt'
    ch = os.path.isfile(entrada)
    if not ch: # verfica se o arquivo existe
        print("\nInfelizmente não foi possivel encontrar esse arquivo, tente novamente com um nome valido")
        espera = input('\t...aperte enter para continuar...\n')
arquivo = open(entrada, 'r')
tempo = input('Informe o tempo limite de execução:')
tempo = float(tempo)

saida = funcoes.Caminho(arquivo, tempo)
if saida.num_vertices < 15:
    for item in saida.grafo:
        print('\t', item)


if saida.peso_total > 0:
    print('-Arestas no Caminho:\n\t-> caminho:', saida.caminho)
    print('\t-> peso: %.2f' % saida.peso_total)
else:
    print("!!! Tempo limite de execução estourado !!!")
arquivo.close()




