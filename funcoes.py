import time
import random


class Caminho:
    # Classe Caminho que contem atributos para o grafo_matriz origem, numero de vertices e arestas do grafo origem e ...
    # o caminho encontrado
    def __init__(self, arquivo, tempo_limite):
        self.inicio = time.perf_counter() #inicio contagem de tempo
        (self.num_vertices, self.num_arestas, self.grafo) = self.converte_matriz(arquivo)
        (self.caminho, self.peso_total, self.peso_maior) = self.vizinho_proximo(tempo_limite)
        self.refinamento_2_opt()
        self.escreve_saida()

    def converte_matriz(self, arquivo):
        # Converte o grafo do arquivo .txt em uma matriz de adjacencias
        linha = arquivo.readline()
        conteudo = linha.split(' ')       # divide a linha, interpretando ' ' como o fim de uma informação, uma quebra
        num_vertices = int(conteudo[0])
        num_arestas = float(conteudo[1])
        num_arestas = int(num_arestas)
        grafo = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        for linha in arquivo:       # adiciona as posição V1 e V2 da lista a conexão
            conteudo = linha.split(' ')
            v1 = int(conteudo[0])
            v2 = int(conteudo[1])
            a = float(conteudo[2])
            grafo[v1][v2] = a
            grafo[v2][v1] = a
        return (num_vertices, num_arestas, grafo)

    def vizinho_proximo(self, tempo):
        #  Função que retorna uma lista com as arestas (v1, v2) no caminho
        u = 0 #  vertice inicial
        C = []  # lista vazia do caminho
        Q = []
        for i in range(self.num_vertices):
            Q.append(i)  # inserir todos os vertices do grafo na lista Q
        Q.remove(u)     # removo o elemente u já encontrado
        peso_total = 0  # inicio o peso dos vertices encontrados = 0
        maior_peso_encontrado  = 0
        pos_maior = u # variavel que guardar a posição no caminho que tem o maior peso
        k = 0
        while Q != []:  # Enquanto Q ainda contem elementos
            v = -10
            peso = max(self.grafo[u]) # pego o maior peso a partir de u, a tendencia é esse valor ir diminuindo
            for i in range(self.num_vertices):
                if i in Q and self.grafo[u][i] != 0 and self.grafo[u][i] < peso:
                    # encontro vertice v (v = i) com menor peso em relação a u
                    v = i
                    peso = self.grafo[u][i]
            if time.perf_counter() - self.inicio >= 60:
                return([], -1)
            if maior_peso_encontrado < peso:
                maior_peso_encontrado = peso
                pos_maior = k
            k = k+1
            peso_total = peso_total + peso
            C.append((u,v)) # inserir aresta encontrada em caminho
            Q.remove(v) # remover vertice ja encontrado
            u = v   # procurar caminho a partir do vertice encontrado
        C.append((u,C[0][0]))
        peso_total = peso_total + self.grafo[u][C[0][0]]
        if maior_peso_encontrado < self.grafo[u][C[0][0]]:
            pos_maior = k
        return (C, peso_total, pos_maior)

    def refinamento_2_opt(self):
        if self.peso_total > -1:
            pos = [0, 0]
            pos[1] = self.peso_maior # sempre vai tentar remover a aresta com maior peso
            while True:
                # Escolha aleatoria para a segunda aresta a ser substituição
                x = random.randrange(1, self.num_vertices)
                if x != pos[1]:
                    pos[0] = x
                    break
            pos = sorted(pos)

            # peso é o peso das possiveis arestas a serem substituidas
            peso = self.grafo[self.caminho[pos[0]][0]][self.caminho[pos[0]][1]]
            peso = peso + self.grafo[self.caminho[pos[1]][0]][self.caminho[pos[1]][1]]
            # peso_tentativa é o peso das arestas que podem substituir as originais no caminho
            peso_tentativa = self.grafo[self.caminho[pos[0]][0]][self.caminho[pos[1]][0]]
            peso_tentativa = peso_tentativa + self.grafo[self.caminho[pos[0]][1]][self.caminho[pos[1]][1]]

            if peso_tentativa < peso:
                # troca se tentativa tem peso menor que o caminho anterior
                aux = (self.caminho[pos[0]][0], self.caminho[pos[1]][0])
                aux2 = (self.caminho[pos[0]][1], self.caminho[pos[1]][1])
                self.caminho[pos[0]] = aux
                self.caminho[pos[1]] = aux2
                self.caminho[pos[1]-1] = (self.caminho[pos[1]-1][1], self.caminho[pos[1]-1][0])
                self.peso_total = self.peso_total - peso + peso_tentativa
                ida = pos[0] + 1
                volta = pos[1] - 1
                Aux = [self.caminho[i] for i in range(self.num_vertices)]
                while ida < pos[1]: # reorganiza as arestas no caminho entre os vertices com arestas removidas
                    self.caminho[ida] = (Aux[volta][1], Aux[volta][0])
                    ida = ida +1
                    volta = volta - 1
                self.caminho[pos[0]+1] = (self.caminho[pos[0]+1][1], self.caminho[pos[0]+1][0])



    def escreve_saida(self):
        #escreve caminho final encontrado em uma arquivo saida
        if self.peso_total > 0:
            arquivo2 = open('arquivo_saida.txt', 'w')
            saida = str(self.peso_total) + '\n'
            arquivo2.write(saida)
            saida = ''
            for i in range(self.num_vertices):
                saida = saida + str(self.caminho[i][0]) + ' '
            saida = saida + str(self.caminho[0][0])
            arquivo2.write(saida)
            arquivo2.close()