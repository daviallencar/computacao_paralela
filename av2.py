from collections import deque
import concurrent.futures
import time

# ---------- ALGORITMO BFS ----------
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
                    fila.append(caminho + [vizinho])

    return caminhos


# ---------- EXECUÇÃO PARALELA ----------
def buscar_subgrafo(subgrafo, start, end):
    return bfs(subgrafo, start, end)

def gerar_subgrafos(grafo, n=3):
    return [grafo.copy() for _ in range(n)]

def busca_paralela(grafo, start, end):
    subgrafos = gerar_subgrafos(grafo)

    resultados = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(buscar_subgrafo, sg, start, end) for sg in subgrafos]
        for future in concurrent.futures.as_completed(futures):
            resultados.extend(future.result())
    return resultados


# ---------- TESTE ----------
def testar_grafo(nome, grafo, start, end):
    print(f"\n{'='*60}")
    print(f"TESTANDO GRAFO: {nome}")
    print(f"De {start} até {end}")
    print('-' * 60)

    # Sequencial
    inicio_seq = time.time()
    resultado_seq = bfs(grafo, start, end)
    fim_seq = time.time()

    print("\n[Sequencial]")
    for caminho in resultado_seq:
        print(caminho)
    print(f"Total de caminhos: {len(resultado_seq)}")
    print(f"Tempo: {fim_seq - inicio_seq:.4f} segundos")

    # Paralelo
    inicio_par = time.time()
    resultado_par = busca_paralela(grafo, start, end)
    fim_par = time.time()

    print("\n[Paralelo]")
    for caminho in resultado_par:
        print(caminho)
    print(f"Total de caminhos (com repetição): {len(resultado_par)}")
    print(f"Tempo: {fim_par - inicio_par:.4f} segundos")
    print('='*60)


# ---------- GRAFOS DE TESTE ----------

grafo_pequeno = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

grafo_grande = {
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


# ---------- EXECUÇÃO DOS TESTES ----------
if __name__ == "__main__":
    testar_grafo("Grafo Pequeno", grafo_pequeno, 'A', 'F')
    testar_grafo("Grafo Grande", grafo_grande, 'A', 'P')
