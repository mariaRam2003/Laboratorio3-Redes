import heapq
from typing import Dict


def dijkstra(graph, start):
    """
    Dijkstra's algorithm to find the shortest path between two nodes in a graph
    
    Args:
        graph: dictionary of dictionaries containing the graph
        start: starting node

    Returns:
        distances: dictionary containing the distance from the starting node to each node
        shortest_path: dictionary containing the previous node in the shortest path to each node
    """
    # Inicializar
    graph = complete_graph_with_infinity(graph)
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_path = {}

    # Calcular distancias
    while queue:
        # Obtener nodo con menor distancia
        (current_distance, current_node) = heapq.heappop(queue)

        # Si la distancia actual es mayor a la distancia almacenada, continuar
        if current_distance > distances[current_node]:
            continue

        # Recorrer vecinos
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_node

    return distances, shortest_path


def complete_graph_with_infinity(graph):
    # Step 1: Identify all unique keys (nodes)
    nodes = set(graph.keys()) | {key for value in graph.values() for key in value.keys()}

    # Step 2: Create a new dictionary with n x n structure
    complete_graph = {node: {other_node: (graph.get(node, {}).get(other_node, float('inf')))
                             for other_node in nodes} for node in nodes}

    return complete_graph


def get_path(destination_id, start, shortest_path):
    """
    Get the shortest path from the starting node to the destination node

    Args:
        destination_id: destination node
        start: starting node
        shortest_path: dictionary containing the previous node in the shortest path to each node
    
    Returns:
        path: list containing the shortest path from the starting node to the destination node
    """
    # Inicializar
    path = [destination_id]

    try:
        # Recorrer nodos
        while destination_id != start:
            # Obtener nodo anterior en el camino
            destination_id = shortest_path[destination_id]
            path.insert(0, destination_id)

        return path
    except Exception as e:
        print(f"ERROR: {e} \n\tTopology might be incomplete. (There may be unreachable nodes)")
        exit()
