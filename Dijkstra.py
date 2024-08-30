import heapq


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
