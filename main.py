from Config_Loader import NetworkConfiguration
from Flooding import Flooding
from dotenv import load_dotenv
import os
import asyncio
import logging

def main():
    # Load the .env file
    load_dotenv()

    # Load the network configuration
    config = NetworkConfiguration('files/topo2024-randomX-2024.txt', 'files/names2024-randomX-2024.txt')
    print(config)

    # Get the environment variables
    jid = os.getenv("JID")
    password = os.getenv("PASSWORD")

    # Logging configuration
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
    
    xmpp = Flooding(jid, password, config)

    xmpp.connect()
    xmpp.process(forever=False)

if __name__ == "__main__":
    main()