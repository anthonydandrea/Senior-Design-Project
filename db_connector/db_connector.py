# SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM information_schema.columns WHERE table_schema = 'db_name' ORDER BY TABLE_NAME, ORDINAL_POSITION
import json
import os
import sys

from mysql.connector import MySQLConnection, Error
from pymongo import MongoClient


class DBConnector:
    def __init__(self):
        self.metadataFileName = "db_metadata.json"

    def fetchMetadata(self, config):
        self.config = config

        for idx, db in enumerate(self.config):
            schema = None
            if db["type"] == "mysql":
                schema = self._fetchMySQLSchema(db)
            elif db["type"] == "mongo":
                schema = self._fetchMongoSchema(db)
            else:
                raise Exception(
                    "Bad database type in db_configs.json: {}".format(db["type"])
                )

        return self.config

    def writeMetadataFile(self, relativePath):
        if not self.config:
            raise Exception("No config given to DBConnector")

        with open(
            os.path.join(os.path.dirname(__file__), self.metadataFileName), "w"
        ) as f:
            json.dump(self.config, f)

    def readMetadataFile(self):
        with open(
            os.path.join(os.path.dirname(__file__), self.metadataFileName)
        ) as json_file:
            self.config = json.load(json_file)

        return self.config

    def _fetchMySQLSchema(self, db):
        SCHEMA_COMMAND = "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM information_schema.columns WHERE table_schema = '{}' ORDER BY TABLE_NAME, ORDINAL_POSITION"

        cnx = None
        try:
            cnx = MySQLConnection(
                user=db["user"], password=db["password"], host=db["host"],
            )

            cursor = cnx.cursor()
            cursor.execute(SCHEMA_COMMAND.format(db["name"]))
            data = cursor.fetchall()

            db["tables"] = dict()

            for row in data:
                tableName = row[0]
                if row[0] not in db["tables"]:
                    db["tables"][tableName] = dict()

                db["tables"][tableName][row[1]] = row[2]

        except Error as e:
            print("Problem in MySQL Connection: {}".format(e))
        finally:
            if cnx:
                cnx.close()

    def _fetchMongoSchema(self, db):
        client = None
        try:
            if "user" in db and "password" in db:
                client = MongoClient(
                    db["host"],
                    db["port"],
                    username=db["user"],
                    password=db["password"],
                    serverSelectionTimeoutMS=2000,
                )
            else:
                client = MongoClient(
                    db["host"], db["port"], serverSelectionTimeoutMS=2000,
                )

            collections = client[db["name"]].list_collection_names()
            db["collections"] = collections

        except:
            print("Problem in Mongo Connections:", sys.exc_info()[0])
        finally:
            if client:
                client.close()


config = None
with open(os.path.join(os.path.dirname(__file__), "db_configs.json")) as json_file:
    config = json.load(json_file)

