from collections import deque
import concurrent.futures
import time

# Criação do grafo
grafo = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E', 'F'],
    'C': ['A', 'G'],
    'D': ['A', 'H'],
    'E': ['B', 'I'],
    'F': ['B', 'J', 'K'],
    'G': ['C', 'L'],
    'H': ['D', 'M'],
    'I': ['E', 'N'],
    'J': ['F'],
    'K': ['F', 'O'],
    'L': ['G', 'P'],
    'M': ['H'],
    'N': ['I'],
    'O': ['K'],
    'P': ['L']
}


# Implementação do BFS

def bfs(grafo, start, end):
    fila = deque([[start]])
    caminhos = []

    while fila:
        caminho = fila.popleft()
        no = caminho[-1]

        if no == end:
            caminhos.append(caminho)
        else:
            for vizinho in grafo.get(no, []):
                if vizinho not in caminho:
                    nova_rota = list(caminho)
                    nova_rota.append(vizinho)
                    fila.append(nova_rota)

    return caminhos


# Aplicando paralelismo

def buscar_subgrafo(subgrafo, start, end):
    return bfs(subgrafo, start, end)

# Função que gera subgrafos para simulação
def gerar_subgrafos(grafo, n=3):
    return [grafo.copy() for _ in range(n)]

# Executar as buscas em paralelo
def busca_paralela(grafo, start, end):
    subgrafos = gerar_subgrafos(grafo)

    resultados = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(buscar_subgrafo, sg, start, end) for sg in subgrafos]
        for future in concurrent.futures.as_completed(futures):
            resultados.extend(future.result())

    return resultados


# Testando e comparando com versão sequencial 
start_no = 'A'
end_no = 'F'

# Teste sequencial
inicio_seq = time.time()
resultado_seq = bfs(grafo, start_no, end_no)
fim_seq = time.time()

print("Resultado sequencial:")
for caminho in resultado_seq:
    print(caminho)
print(f"Tempo: {fim_seq - inicio_seq:.4f} segundos\n")

# Teste paralelo
inicio_par = time.time()
resultado_par = busca_paralela(grafo, start_no, end_no)
fim_par = time.time()

print("Resultado paralelo:")
for caminho in resultado_par:
    print(caminho)
print(f"Tempo: {fim_par - inicio_par:.4f} segundos")