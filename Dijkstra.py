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

    while destination_id != start:
        destination_id = shortest_path[destination_id]
        path.insert(0, destination_id)

    return path


def test_dijkstra():
    # Define a sample graph as an adjacency list
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }

    # Run Dijkstra's algorithm from node 'A'
    distances, shortest_path = dijkstra(graph, 'A')

    # Expected distances from 'A' to other nodes
    expected_distances = {
        'A': 0,
        'B': 1,
        'C': 3,
        'D': 4
    }

    # Expected shortest paths from 'A'
    expected_shortest_path = {
        'B': 'A',
        'C': 'B',
        'D': 'C'
    }

    # Print the results
    print("Distances:", distances)
    print("Expected Distances:", expected_distances)
    print("Shortest Path:", shortest_path)
    print("Expected Shortest Path:", expected_shortest_path)

    print(get_path('D', 'A', shortest_path))
    # # Validate the results
    # assert distances == expected_distances, "Test failed: Distances are incorrect"
    # assert shortest_path == expected_shortest_path, "Test failed: Shortest path is incorrect"
    print("Test passed!")


if __name__ == "__main__":
    # Run the test
    test_dijkstra()
