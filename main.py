from Config_Loader import NetworkConfiguration
from LinkStateRouting import LinkStateRouting
from dotenv import load_dotenv
import os
import platform
import asyncio


def main():
    if platform.system() == 'Windows':
        # On Windows, the proactor event loop is necessary to listen for
        # events on stdin while running the asyncio event loop.
        print("INFO: The current platform is Windows")
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Load the .env file
    load_dotenv()

    # Load the network configuration
    config = NetworkConfiguration('files/topo2024-randomX-2024.txt', 'files/names2024-randomX-2024.txt')
    print(config)

    # Get the environment variables
    jid = os.getenv("JID")
    password = os.getenv("PASSWORD")

    print("jid: ", jid)
    print("pw: ", password)
    print()

    # Logging configuration
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

    xmpp = LinkStateRouting(jid, password, config)

    xmpp.connect(disable_starttls=True, use_ssl=False)
    xmpp.process(forever=False)


if __name__ == "__main__":
    main()
