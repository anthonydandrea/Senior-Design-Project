import os
import json
from db_connector import DBConnector

config = None
with open(os.path.join(os.path.dirname(__file__), "db_configs.json")) as json_file:
    config = json.load(json_file)

connector = DBConnector()
# print(connector.fetchMetadata(config))
print(connector.readMetadataFile())
