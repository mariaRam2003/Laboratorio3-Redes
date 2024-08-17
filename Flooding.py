from slixmpp import ClientXMPP
import logging
import asyncio

class Flooding(ClientXMPP):
    def __init__(self, jid, password, config):
        super().__init__(jid, password)
        self.config = config
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.sent_messages = set()
        self.logger = logging.getLogger(__name__)


    async def start(self, event):
        self.logger.info("Starting session")
        self.send_presence()
        await self.get_roster()
        self.logger.info("Presence sent and roster retrieved")
        # Send a test message to the neighbors
        self.send_flood_message('Hello, this is a test message!')

    async def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            if (msg['from'], msg['body']) not in self.sent_messages:
                self.logger.info(f"Received message from {msg['from']}: {msg['body']}")
                print(f"Received message from {msg['from']}: {msg['body']}")
                self.sent_messages.add((msg['from'], msg['body']))
                self.flood_message(msg['body'], msg['from'])

    def flood_message(self, message, origin):
        self.logger.info(f"Flooding message from {origin}: {message}")
        for node in self.config.get_neighbors(self.boundjid.bare):
            if node != origin:
                self.logger.debug(f"Sending message to {node}")
                self.send_message(mto=node, mbody=message, mtype='chat')

    def send_flood_message(self, message):
        self.logger.info(f"Sending flood message: {message}")
        for node in self.config.get_neighbors(self.boundjid.bare):
            self.logger.debug(f"Sending message to {node}")
            self.send_message(mto=node, mbody=message, mtype='chat')