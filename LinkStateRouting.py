import asyncio

from slixmpp import ClientXMPP
from Config_Loader import NetworkConfiguration
from Dijkstra import dijkstra, get_path
import logging
from aioconsole import ainput
from asyncio import sleep
import json
from json import JSONDecodeError
import time


class LinkStateRouting(ClientXMPP):
    def __init__(self, jid, password, config: NetworkConfiguration):
        super().__init__(jid, password)
        print(f"LSR initialized for JID: {jid}")
        print("\nWARNING: asegurarse de que la topología este completa antes de mandar un mensaje")
        # logging
        self.logger = logging.getLogger(__name__)

        # event handlers and instance vars
        self._add_event_handlers()
        self.sent_messages = set()
        self.config = config

        # we save config variables
        self.my_jid = jid
        self.my_id = config.jid_node_map[jid]
        self.my_neighbors = config.get_neighbors(self.my_id)

        # This dictionary is to keep track of the time the echo message was sent
        self.response_times = {}
        self._weights = {
            self.my_id: {
                # We use 10_000.0 instead of infinity because otherwise is not json compliant
                'table': {neighbor_id: 10_000.0 for neighbor_id in self.my_neighbors},
                'version': 0
            }
        }

        # dijkstra results
        self.dijkstra_distances = None
        self.dijkstra_sortest_path = None

    async def handle_send_message(self):
        """
        If we were to send a message, this function handles asking the user for a message and destiny
        Returns: None
        """
        await sleep(5)
        while True:
            print("Current weights table:")
            print(self._weights)
            destiny_id = await ainput("Ingrese el nodo destino: ")
            data = await ainput("Ingrese el mensaje: ")
            sender = self.my_id

            if destiny_id not in self.config.node_names:
                print("ERROR: el nodo destino no es parte de la topologia")
                return

            reciever_jid = self.config.node_names[destiny_id]
            hops = 0

            if destiny_id not in self.my_neighbors:
                string = f'{{\"type\": \"send_routing\", \"from\": \"{sender}\", \"data\": \"{data}\" , \"hops\": \"{hops + 1}\"}}'
                self.send_message(mto=reciever_jid, mbody=string, mtype='chat')
                return

            string = f'{{\"type\": \"message\", \"from\": \"{sender}\", \"data\": \"{data}\" }}'
            self.send_message(mto=reciever_jid, mbody=string, mtype='chat')
            print(f"Message sent to {reciever_jid} from {self.my_id} with data: {data}")


    def _send_echo_message(self):
        """This message handles sending the echo messages"""
        echo_msg = '{\"type\": \"echo\"}'
        for neighbor_id in self.my_neighbors:
            neighbor_jid = self.config.node_names[neighbor_id]
            self.send_message(mto=neighbor_jid, mbody=echo_msg, mtype='chat')
            self.response_times[neighbor_jid] = time.time()
            print(f"Sending echo message to neighbor: {neighbor_jid}")


    def _add_event_handlers(self):
        """We add the event handlers"""
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    async def start(self, event):
        """Function run on session start"""
        print("Session started, sending presence and getting roster...")
        self.send_presence()
        await self.get_roster()
        self._send_echo_message()
        await asyncio.create_task(self.handle_send_message())

    async def message(self, msg):
        """
        This function is triggered when we get any message
        and handles all the cases defined by the protocol
        """
        if msg['type'] not in ('chat', 'normal'):
            print("unknown message type")
            print("msg body: \n", msg['body'])
            return
        
        # Message's sender.
        sender = str(msg["from"])
        sender_jid = sender.split("/")[0]

        body = msg['body']

        print(f"Message received from {sender_jid} with body: {body}")

        try:
            body = json.loads(body)  # We turn the string into a dictionary
        except JSONDecodeError as e:
            print(f"ERROR: {sender_jid}'s message is NOT JSON compliant!")
            print("MESSAGE:\n~~~~~~~~~~~~~~~~~~~~~~~")
            print(body)
            print('\n~~~~~~~~~~~~~~~~~~~~~~~')
            return

        try:
            msg_type = body['type']

            if msg_type == 'echo':
                echo_response = '{\"type\": \"echo_response\"}'
                self.send_message(mto=sender_jid, mbody=echo_response, mtype='chat')

            elif msg_type == 'echo_response':
                end_time = time.time()
                start_time = self.response_times[sender_jid]
                elapsed = end_time - start_time

                # we update the weights
                sender_id = self.config.jid_node_map[sender_jid]
                self._weights[self.my_id]['table'][sender_id] = elapsed
                self._weights[self.my_id]['version'] += 1

                # logic for table broadcast
                self.broadcast_weight(self.my_id)

            elif msg_type == 'weights':
                table = body['table']
                version = body['version']
                user = body['from']
                node_id = self.config.jid_node_map[user]

                if node_id not in self._weights:
                    self._weights[node_id] = {
                        'table': table,
                        'version': version
                    }
                    self.broadcast_weight(node_id)

                    pre_processed_table = self.pre_process_table()

                    self.dijkstra_distances, self.dijkstra_sortest_path = dijkstra(pre_processed_table, self.my_id)
                    return

                if self._weights[node_id]['version'] < version:
                    self._weights[node_id] = {
                        'table': table,
                        'version': version
                    }
                    self.broadcast_weight(node_id)

                    pre_processed_table = self.pre_process_table()

                    self.dijkstra_distances, self.dijkstra_sortest_path = dijkstra(pre_processed_table, self.my_id)

            elif msg_type == 'send_routing':
                # TODO: the protocol doesnt specify if the destiny and sender should be node id or jid
                destiny = body['to']
                sender = body['from']
                data = body['data']
                hops = body['hops']

                path = get_path(destiny, self.my_id, self.dijkstra_sortest_path)
                next_step_id = path[0]
                reciever_jid = self.config.node_names[next_step_id]

                if destiny not in self.my_neighbors:
                    string = f'{{\"type\": \"send_routing\", \"from\": \"{sender}\", \"data\": \"{data}\" , \"hops\": \"{hops + 1}\"}}'
                    self.send_message(mto=reciever_jid, mbody=string, mtype='chat')
                    return

                string = f'{{\"type\": \"message\", \"from\": \"{sender}\", \"data\": \"{data}\" }}'
                self.send_message(mto=reciever_jid, mbody=string, mtype='chat')

            elif msg_type == 'message':
                print("Message has been recieved!")
                print("from: ", body['from'])
                print("message: ", body['data'])

        except KeyError as e:
            print("Recieved message is not correctly formated: ")
            print(body)

    def pre_process_table(self):
        """This method preprocess the table in order to be used by the Dijkstra's algorithm"""
        new_dict = {}
        print("Preprocessing table for Dijkstra's algorithm...")
        for node_id, table_dict in self._weights.items():
            new_dict[node_id] = table_dict['table']

        return new_dict

    def broadcast_weight(self, node_id):
        """
        Args:
            node_id: the id of the node table we want to broadcast
        Returns: None
        """
        print(f"Broadcasting weight for node_id: {node_id} to all neighbors")

        if node_id not in self._weights:
            print("Couldn't broadcast weight for node id: ", node_id)
            return

        table = self._weights[node_id]['table']
        json_table = json.dumps(table)
        version = self._weights[node_id]['version']
        table_jid = self.config.node_names[node_id]

        string = f'{{\"type\": \"weights\", \"table\": {json_table}, \"version\": {version}, \"from\": \"{table_jid}\" }}'

        # we broadcast to all our neighbors
        for neighbor_id in self.my_neighbors:
            neighbor_jid = self.config.node_names[neighbor_id]
            self.send_message(mto=neighbor_jid, mbody=string, mtype='chat')
