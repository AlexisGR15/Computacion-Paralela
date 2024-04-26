import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool, freeze_support
import time

def generar_grafo(niveles):
    G = nx.DiGraph()
    for nivel in range(1, niveles + 1):
        for nodo in range(nivel):
            G.add_node(f'{nivel}-{nodo}')
            if nivel > 1:
                for nodo_padre in range(nivel - 1):
                    G.add_edge(f'{nivel - 1}-{nodo_padre}', f'{nivel}-{nodo}')
    return G

def dfs_recursivo(G, nodo_actual, nodo_final, visitados, camino_actual):
    if nodo_actual == nodo_final:
        return camino_actual + [nodo_actual]
    visitados.add(nodo_actual)
    for vecino in G.neighbors(nodo_actual):
        if vecino not in visitados:
            camino = dfs_recursivo(G, vecino, nodo_final, visitados, camino_actual + [nodo_actual])
            if camino:
                return camino
    return None

def buscar_camino(args):
    G, nodo_inicial, nodo_final = args
    visitados = set()
    return dfs_recursivo(G, nodo_inicial, nodo_final, visitados, [])

if __name__ == '__main__':
    freeze_support()  # Esta línea es necesaria en Windows para evitar errores al usar multiprocessing
    
    G = generar_grafo(7)

    # Configurar el estilo del grafo
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)

    # Dibujar el grafo con estilo
    nx.draw_networkx(G, pos, with_labels=True, node_size=1500, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray', arrows=True)

    plt.title('Grafo de ejemplo', fontsize=12)
    plt.axis('off')  # Ocultar ejes
    plt.show()

    # Ejemplo de búsqueda de camino desde un nodo inicial a un nodo final usando multiprocessing
    nodo_inicial = '1-0'
    nodo_final = '4-2'

    # Medir el tiempo de ejecución para el DFS simple
    inicio_simple = time.time()
    camino_simple = dfs_recursivo(G, nodo_inicial, nodo_final, set(), [])
    fin_simple = time.time()

    # Medir el tiempo de ejecución para el DFS con multiprocessing
    inicio_multiprocessing = time.time()
    num_partes = 4
    partes = [(G, nodo_inicial, nodo_final)] * num_partes
    with Pool(processes=num_partes) as pool:
        caminos_multiprocessing = pool.map(buscar_camino, partes)
    fin_multiprocessing = time.time()

    # Filtrar los caminos encontrados y mostrar el primero
    camino_encontrado = next((camino for camino in caminos_multiprocessing if camino), None)
    if camino_encontrado:
        print("Camino encontrado con multiprocessing: ", camino_encontrado)
    else:
        print("No se encontró un camino desde ", nodo_inicial, " hasta ", nodo_final)

    # Imprimir tiempos de ejecución
    print("Tiempo de ejecución para DFS simple: ", fin_simple - inicio_simple, " segundos")
    print("Tiempo de ejecución para DFS con multiprocessing: ", fin_multiprocessing - inicio_multiprocessing, " segundos")
