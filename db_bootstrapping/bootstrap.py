import sys
import os
import json
import mysql.connector
from pymongo import MongoClient

print(sys.argv)

secrets = None
with open(os.path.join(os.path.dirname(__file__), "../.secrets.json")) as json_file:
    secrets = json.load(json_file)


def checkMySQLConnectionAllowed():
    try:
        cnx = mysql.connector.connect(
            user=secrets["mysql"]["user"],
            password=secrets["mysql"]["password"],
            host="127.0.0.1",
        )
        cnx.close()
        print("Able to connect to MySQL server!")

    except:
        print("Failed to connect to MySQL server")
        exit(1)


def checkMongoConnectionAllowed():
    try:
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
        client.server_info()
        client.close()
        print("Able to connect to Mongo server!")

    except:
        print("Failed to connect to Mongo server")
        exit(1)


if __name__ == "__main__":
    checkMySQLConnectionAllowed()
    checkMongoConnectionAllowed()
