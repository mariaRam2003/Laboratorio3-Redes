import heapq


def dijkstra(graph, start):
    # Inicializar
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_path = {}

    while queue:
        (current_distance, current_node) = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_node

    return distances, shortest_path


def get_path(destination_id, start, shortest_path):
    path = [destination_id]

    try:
        while destination_id != start:
            destination_id = shortest_path[destination_id]
            path.insert(0, destination_id)

        return path
    except Exception as e:
        print("ERROR: topology might be incomplete. i.e there may be unreachable nodes")
        exit()
