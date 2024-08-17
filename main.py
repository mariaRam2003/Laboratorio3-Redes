from Config_Loader import NetworkConfiguration

def main():
    config = NetworkConfiguration('files/topo2024-randomX-2024.txt', 'files/names2024-randomX-2024.txt')
    print(config)

    # Get neighbors of node 'A'
    print(config.get_neighbors('A'))

    print()

    # Get name of node 'A'
    print(config.get_node_name('A'))


if __name__ == "__main__":
    main()