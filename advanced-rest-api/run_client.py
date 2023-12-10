""" Deploys internal client.
    Requires connection to api and database.
"""
import logging

from configuration import Config
from client import create_client

logging.basicConfig(format=Config.LOGS_FORMAT, filename=Config.CLIENT_LOGS_FILE, level=logging.ERROR)
client = create_client()

client.startup()
client.run()
