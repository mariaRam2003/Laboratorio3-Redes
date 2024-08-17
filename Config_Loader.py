import json
import os
import re

class NetworkConfiguration:
    """
    A class to represent a network configuration.
    Attributes:
    - topology (dict): A dictionary representing the network topology.
    - node_names (dict): A dictionary representing the names of the nodes.
    Methods:
    - load_topology(topo_file): Loads a topology file.
    - load_names(names_file): Loads a names file.
    - fix_single_quotes(content): Replaces all single quotes with double quotes in the given content.
    - validate_configuration(): Validates the configuration by checking if all the nodes in the names file are present in the topology file.
    - get_neighbors(node_id): Retrieves the neighbors of a given node.
    - get_node_name(node_id): Retrieves the name of a node based on its ID.
    - __str__(): Returns a string representation of the object.
    """
    def __init__(self, topo_file, names_file):
        self.topology = {}
        self.node_names = {}
        self.load_topology(topo_file)
        self.load_names(names_file)
        self.validate_configuration()

    def load_topology(self, topo_file):
        """
        Loads a topology file and sets the 'topology' attribute of the object.
        Parameters:
        - topo_file (str): The path to the topology file.
        Raises:
        - FileNotFoundError: If the topology file does not exist.
        - ValueError: If the topology file is not of the correct type.
        Returns:
        - None
        """
        if not os.path.exists(topo_file):
            raise FileNotFoundError(f"Topology file '{topo_file}' does not exist.")
        
        with open(topo_file, 'r') as file:
            content = file.read()
            content = self.fix_single_quotes(content)
            data = json.loads(content)
            if data['type'] != 'topo':
                raise ValueError("Topology file is not of the correct type.")
            self.topology = data['config']

    def load_names(self, names_file):
        """
        Load names from a JSON file.
        Parameters:
            names_file (str): The path to the JSON file containing the names.
        Raises:
            FileNotFoundError: If the names file does not exist.
            ValueError: If the names file is not of the correct type.
        """
        if not os.path.exists(names_file):
            raise FileNotFoundError(f"Names file '{names_file}' does not exist.")
        
        with open(names_file, 'r') as file:
            content = file.read()
            content = self.fix_single_quotes(content)
            data = json.loads(content)
            if data['type'] != 'names':
                raise ValueError("Names file is not of the correct type.")
            self.node_names = data['config']

    def fix_single_quotes(self, content):
        """
        Replaces all single quotes with double quotes in the given content.
        Parameters:
        - content (str): The content to be fixed.
        Returns:
        - str: The fixed content with double quotes.

        """
        content = re.sub(r"'", '"', content)  # Change single quotes to double quotes
        return content

    def validate_configuration(self):
        """
        Validates the configuration by checking if all the nodes in the names file are present in the topology file.
        Raises:
            ValueError: If a node in the names file is not found in the topology file.
        """
        for node in self.node_names.keys():
            if node not in self.topology:
                raise ValueError(f"Node '{node}' in names file is not in the topology file.")

    def get_neighbors(self, node_id):
        """
        Retrieves the neighbors of a given node.
        Parameters:
            node_id (str): The ID of the node.
        Returns:
            list: A list of neighbor nodes.

        """
        print(f"Node '{node_id}' Neighbors:")
        return self.topology.get(node_id, [])

    def get_node_name(self, node_id):
        """
        Retrieves the name of a node based on its ID.
        Parameters:
            node_id (str): The ID of the node.
        Returns:
            str: The name of the node if found, None otherwise.
        """
        print(f"Node '{node_id}' name:")
        return self.node_names.get(node_id, None)

    def __str__(self):
        """
        Returns a string representation of the object.
        The string includes the topology and node names.
        Returns:
            str: A string representation of the object.
        """
        topo_str = "Topology:\n"
        for node, neighbors in self.topology.items():
            topo_str += f"{node} -> {', '.join(neighbors)}\n"
        
        names_str = "Node Names:\n"
        for node_id, node_name in self.node_names.items():
            names_str += f"{node_id}: {node_name}\n"
        
        return topo_str + "\n" + names_str