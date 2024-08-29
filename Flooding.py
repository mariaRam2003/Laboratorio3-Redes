from slixmpp import ClientXMPP
from Config_Loader import NetworkConfiguration
from Dijkstra import dijkstra, get_path
import logging
import asyncio
import json
import time


class Flooding(ClientXMPP):
    def __init__(self, jid, password, config: NetworkConfiguration):
        super().__init__(jid, password)
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

    def _send_echo_message(self):
        echo_msg = '{\"type\": \"echo\"}'
        for neighbor_id in self.my_neighbors:
            neighbor_jid = self.config.node_names[neighbor_id]
            self.send_message(mto=neighbor_jid, mbody=echo_msg, mtype='chat')
            self.response_times[neighbor_jid] = time.time()

    def _add_event_handlers(self):
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        self._send_echo_message()

    async def message(self, msg):
        if msg['type'] not in ('chat', 'normal'):
            print("unknown message type")
            print("msg body: \n", msg['body'])
            return

        # Message's sender.
        sender = str(msg["from"])
        sender_jid = sender.split("/")[0]

        body = msg['body']
        # TODO: We must add a try catch here
        body = json.loads(body)  # We turn the string into a dictionary
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

            if not (self._weights[node_id]) or (self._weights[node_id]['version'] < version):
                self._weights[node_id] = {
                    'table': table,
                    'version': version
                }
                self.broadcast_weight(node_id)

                pre_processed_table = self.pre_process_table()

                self.dijkstra_distances, self.dijkstra_sortest_path = dijkstra(pre_processed_table, self.my_id)

        elif msg_type == 'send_routing':
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

    def pre_process_table(self):
        new_dict = {}
        for node_id, table_dict in self._weights.items():
            new_dict[node_id] = table_dict['table']

        return new_dict

    def broadcast_weight(self, node_id):
        """
        Args:
            node_id: the id of the node table we want to broadcast
        Returns: None
        """

        if node_id not in self._weights:
            print("Couldn't broadcast weight for node id: ", node_id)
            return

        table = self._weights[node_id]['table']
        json_table = json.loads(table)
        version = self._weights[node_id]['version']
        table_jid = self.config.node_names[node_id]

        string = f'{{\"type\": \"weights\", \"table\": {{ {json_table} }}, \"version\": {version}, \"from\": \"{table_jid}\" }}'

        # we broadcast to all our neighbors
        for neighbor_id in self.my_neighbors:
            neighbor_jid = self.config.node_names[neighbor_id]
            self.send_message(mto=neighbor_jid, mbody=string, mtype='chat')

