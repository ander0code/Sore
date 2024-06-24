from gtts import gTTS
import networkx as nx
import matplotlib.pyplot as plt
import random
import os

def Esquema_grafo_hospital():
    G = nx.Graph()  

    # Piso 1
    G.add_node("Recepción", pos=(5, 5), floor=1)
    G.add_node("Escaleras 1A", pos=(20, 5), floor=1)
    G.add_node("Emergencias", pos=(35, 5), floor=1)
    G.add_node("Escaleras 1B", pos=(50, 5), floor=1)
    G.add_node("Consultorios", pos=(65, 5), floor=1)
    G.add_node("Escaleras 1C", pos=(80, 5), floor=1)
    G.add_node("Radiología", pos=(95, 5), floor=1)
    G.add_node("Escaleras 1D", pos=(110, 5), floor=1)

    G.add_edge("Recepción", "Escaleras 1A", weight=2)
    G.add_edge("Escaleras 1A", "Emergencias", weight=1)
    G.add_edge("Emergencias", "Escaleras 1B", weight=2)
    G.add_edge("Escaleras 1B", "Consultorios", weight=1)
    G.add_edge("Consultorios", "Escaleras 1C", weight=2)
    G.add_edge("Escaleras 1C", "Radiología", weight=1)
    G.add_edge("Radiología", "Escaleras 1D", weight=2)
    
    # Piso 2
    G.add_node("Laboratorio", pos=(5, 15), floor=2)
    G.add_node("Escaleras 2A", pos=(20, 15), floor=2)
    G.add_node("Quirófanos", pos=(35, 15), floor=2)
    G.add_node("Escaleras 2B", pos=(50, 15), floor=2)
    G.add_node("UCI", pos=(65, 15), floor=2)
    G.add_node("Escaleras 2C", pos=(80, 15), floor=2)
    G.add_node("Farmacia", pos=(95, 15), floor=2)
    G.add_node("Escaleras 2D", pos=(110, 15), floor=2)

    G.add_edge("Laboratorio", "Escaleras 2A", weight=2)
    G.add_edge("Escaleras 2A", "Quirófanos", weight=1)
    G.add_edge("Quirófanos", "Escaleras 2B", weight=2)
    G.add_edge("Escaleras 2B", "UCI", weight=1)
    G.add_edge("UCI", "Escaleras 2C", weight=2)
    G.add_edge("Escaleras 2C", "Farmacia", weight=1)
    G.add_edge("Farmacia", "Escaleras 2D", weight=2)

    # Piso 3
    G.add_node("Dormitorios", pos=(5, 25), floor=3)
    G.add_node("Escaleras 3A", pos=(20, 25), floor=3)
    G.add_node("Pediatría", pos=(35, 25), floor=3)
    G.add_node("Escaleras 3B", pos=(50, 25), floor=3)
    G.add_node("Ginecología", pos=(65, 25), floor=3)
    G.add_node("Escaleras 3C", pos=(80, 25), floor=3)
    G.add_node("Sala de Espera", pos=(95, 25), floor=3)
    G.add_node("Escaleras 3D", pos=(110, 25), floor=3)

    G.add_edge("Dormitorios", "Escaleras 3A", weight=2)
    G.add_edge("Escaleras 3A", "Pediatría", weight=1)
    G.add_edge("Pediatría", "Escaleras 3B", weight=2)
    G.add_edge("Escaleras 3B", "Ginecología", weight=1)
    G.add_edge("Ginecología", "Escaleras 3C", weight=2)
    G.add_edge("Escaleras 3C", "Sala de Espera", weight=1)
    G.add_edge("Sala de Espera", "Escaleras 3D", weight=2)

    # Conexiones verticales
    G.add_edge("Escaleras 1A", "Escaleras 2A", weight=1)
    G.add_edge("Escaleras 2A", "Escaleras 3A", weight=1)
    G.add_edge("Escaleras 1B", "Escaleras 2B", weight=1)
    G.add_edge("Escaleras 2B", "Escaleras 3B", weight=1)
    G.add_edge("Escaleras 1C", "Escaleras 2C", weight=1)
    G.add_edge("Escaleras 2C", "Escaleras 3C", weight=1)
    G.add_edge("Escaleras 1D", "Escaleras 2D", weight=1)
    G.add_edge("Escaleras 2D", "Escaleras 3D", weight=1)

    return G

hospital_graph = Esquema_grafo_hospital()


def accidentes_aleatorios(G, punto_partida, target="Recepción", num_nodes=3):
    # Crear una lista de todos los nodos excepto el punto de partida y el destino
    all_nodes = list(set(G.nodes()) - {punto_partida, target})
    # Seleccionar aleatoriamente un número de nodos para bloquear, asegurándose de no incluir el punto de partida ni el destino
    nodes_to_block = random.sample(all_nodes, k=min(num_nodes, len(all_nodes)))
    G.remove_nodes_from(nodes_to_block)
    return nodes_to_block

def camnimo_mas_corto(G, punto_partida, target="Recepción"):
    try:
        path = nx.dijkstra_path(G, punto_partida, target, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None
def draw_hospital_graph(G, path=None, nodo_bloqueado=None):
    pos = nx.get_node_attributes(G, 'pos')
    labels = {node: node for node in G.nodes() if node in pos}  # Asegurar que solo dibujamos nodos existentes

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
    nx.draw_networkx_labels(G, pos, labels)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True) if u in pos and v in pos})

    if path:
        # Filtrar los segmentos de caminos que incluyen nodos eliminados
        path_edges = list(zip(path, path[1:]))
        path_edges = [edge for edge in path_edges if edge[0] in pos and edge[1] in pos]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="r", width=2)

    # Si los nodos bloqueados existen y se deben dibujar
    if nodo_bloqueado:
        nodo_bloqueado = [node for node in nodo_bloqueado if node in pos]  # Verificar si los nodos bloqueados aún existen en el grafo
        if nodo_bloqueado:
            nx.draw_networkx_nodes(G, pos, nodelist=nodo_bloqueado, node_color="red", node_size=500)

    plt.show()


punto_partida = "Sala de Espera" #se puede cambiar de lugar

nodo_bloqueado = accidentes_aleatorios(hospital_graph, punto_partida, num_nodes=3)
print("Nodos bloqueados:", nodo_bloqueado)

ruta = camnimo_mas_corto(hospital_graph, punto_partida)

if ruta:
    texto = "EMERGENCIA DETECTADA. "
    for i in range(1, len(ruta) - 1):
        texto += f"Diríjase a la {ruta[i]}. "
    texto += f"Desde la {ruta[-1]} salga del edificio siguiendo las señales de emergencia."
    print(texto)
else:
    texto = ("Todo los caminos disponibles han sido bloqueados, mantenga la calma y espere en su lugar, hasta que la ayuda llegue.")
    print(texto)

output = gTTS(text=str(texto), lang="es", slow=False)
output.save("audio1.mp3")

os.system("start audio1.mp3")

draw_hospital_graph(hospital_graph, ruta, nodo_bloqueado)

