import time
import matplotlib.pyplot as plt
import networkx as nx

#ALGORITMO 1: GULOSO
def coloracao_gulosa_3_cores(grafo):
    cores_vertice = {vertice: -1 for vertice in grafo.nodes()}
    paleta = {0: "red", 1: "blue", 2: "green"}
    cor_falha = "dimgray"

    # Ordena por maior grau para melhorar a heurística gulosa
    vertices_ordenados = sorted(
        grafo.nodes(), key=lambda x: grafo.degree(x), reverse=True
    )

    for u in vertices_ordenados:
        cores_vizinhos = {
            cores_vertice[v] for v in grafo.neighbors(u) if cores_vertice[v] != -1
        }
        cor_escolhida = 0
        while cor_escolhida in cores_vizinhos:
            cor_escolhida += 1
        cores_vertice[u] = cor_escolhida

    cores_para_desenho = []
    sucesso = True
    for node in grafo.nodes():
        cor_id = cores_vertice[node]
        if cor_id in paleta:
            cores_para_desenho.append(paleta[cor_id])
        else:
            cores_para_desenho.append(cor_falha)
            sucesso = False

    return cores_para_desenho, sucesso


# ALGORITMO 2: BACKTRACKING
def eh_seguro(u, grafo, cores_vertice, cor_atual):
    for vizinho in grafo.neighbors(u):
        if cores_vertice[vizinho] == cor_atual:
            return False
    return True


def resolver_coloracao_bt(grafo, K, cores_vertice, vertices, index_atual):
    if index_atual == len(vertices):
        return True

    u = vertices[index_atual]
    for cor in range(K):
        if eh_seguro(u, grafo, cores_vertice, cor):
            cores_vertice[u] = cor
            if resolver_coloracao_bt(
                grafo, K, cores_vertice, vertices, index_atual + 1
            ):
                return True
            cores_vertice[u] = -1
    return False


def coloracao_backtracking_3_cores(grafo):
    cores_vertice = {vertice: -1 for vertice in grafo.nodes()}
    paleta = {0: "red", 1: "blue", 2: "green"}
    cor_falha = "dimgray"
    vertices = list(grafo.nodes())

    sucesso = resolver_coloracao_bt(
        grafo, K=3, cores_vertice=cores_vertice, vertices=vertices, index_atual=0
    )

    cores_para_desenho = []
    for node in grafo.nodes():
        cor_id = cores_vertice[node]
        if cor_id in paleta and sucesso:
            cores_para_desenho.append(paleta[cor_id])
        else:
            cores_para_desenho.append(cor_falha)

    return cores_para_desenho,sucesso


# interação
print("=" * 50)
print("  SIMULADOR DE COLORACÃO DE GRAFOS (MÁXIMO 3 CORES)  ")
print("=" * 50)

try:
    num_vertices = int(input("Digite o número de vértices (ex: 10, 15, 20): "))
    prob_aresta = float(
        input("Digite a probabilidade de conexão de arestas (0.0 a 1.0, ex: 0.2): ")
    )
except ValueError:
    print("Por favor, insira valores válidos.")
    exit()

print("\nGerando grafo aleatório...")
# Cria um grafo aleatório de Erdos-Renyi
G = nx.erdos_renyi_graph(n=num_vertices, p=prob_aresta, seed=42)

print("Executando o Algoritmo Guloso...")
t0 = time.time()
cores_guloso, sucesso_guloso = coloracao_gulosa_3_cores(G)
tempo_guloso = time.time() - t0

print("Executando o Algoritmo de Backtracking (pode demorar se o grafo for complexo)...")
t1 = time.time()
cores_bt, sucesso_bt = coloracao_backtracking_3_cores(G)
tempo_bt = time.time() - t1

print("\n--- RESULTADOS ---")
print(
    f"Guloso:      {'Sucesso' if sucesso_guloso else 'Falhou (usou > 3 cores)'} | Tempo: {tempo_guloso:.6f}s"
)
print(
    f"Backtracking: {'Sucesso' if sucesso_bt else 'Falhou (impossível com 3)'} | Tempo: {tempo_bt:.6f}s"
)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
pos = nx.spring_layout(G, seed=42)  # Mantém o mesmo layout nos dois plots

#  Guloso
nx.draw(
    G,
    pos,
    ax=ax1,
    with_labels=True,
    node_color=cores_guloso,
    node_size=500,
    font_color="white",
    font_weight="bold",
    edge_color="gainsboro",
)
titulo_guloso = (
    "Guloso: Sucesso" if sucesso_guloso else "Guloso: Falhou (Nós cinzas)"
)
ax1.set_title(
    f"{titulo_guloso}\nTempo: {tempo_guloso:.5f}s",
    color="green" if sucesso_guloso else "red",
)

#  Backtracking
nx.draw(
    G,
    pos,
    ax=ax2,
    with_labels=True,
    node_color=cores_bt,
    node_size=500,
    font_color="white",
    font_weight="bold",
    edge_color="gainsboro",
)
titulo_bt = "Backtracking: Sucesso" if sucesso_bt else "Backtracking: Impossível"
ax2.set_title(
    f"{titulo_bt}\nTempo: {tempo_bt:.5f}s", color="green" if sucesso_bt else "red"
)

plt.suptitle(
    f"Comparação de Coloração (Vértices: {num_vertices}, Prob. Arestas: {prob_aresta})",
    fontsize=16,
)
plt.show()