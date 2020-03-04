import sys
import os
import json
import csv
import random as rd

import mysql.connector
from pymongo import MongoClient

secrets = None
with open(os.path.join(os.path.dirname(__file__), "../.secrets.json")) as json_file:
    secrets = json.load(json_file)

config = None
with open(
    os.path.join(os.path.dirname(__file__), "bootstrap_config.json")
) as json_file:
    config = json.load(json_file)

data = None

cursor_group = []


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


def readCsv():
    global data
    f = open(sys.argv[1], newline="")
    data = csv.reader(f)


def createMySQLCursors(c):
    # print(c)
    try:
        cnx = mysql.connector.connect(
            user=secrets["mysql"]["user"],
            password=secrets["mysql"]["password"],
            host="127.0.0.1",
        )

        cursor = cnx.cursor()

        # Create DBs
        for db, info in c["dbs"].items():
            # print(db, ":", info)
            cursor.execute("DROP DATABASE IF EXISTS {}".format(db))
            cursor.execute("CREATE DATABASE {}".format(db))
            cursor.execute("USE {}".format(db))

            for tableName, tableInfo in info["tables"].items():
                # print(tableName, ":", tableInfo)
                cols = tableInfo["columns"]
                colsFormatted = "(" + ", ".join(cols) + ")"
                colTags = ["%s"] * len(cols)
                # print(cols)
                # print(colTags)
                cursor.execute("DROP TABLE IF EXISTS {}".format(tableName))
                cursor.execute(
                    "CREATE TABLE {} {}".format(tableName, tableInfo["schema"])
                )
                cursor_group.append(
                    {
                        "type": "mysql",
                        "db_name": db,
                        "db_obj": cnx,
                        "cursor": cursor,
                        "statement": "INSERT INTO {} {} VALUES ({})".format(
                            tableName, colsFormatted, ", ".join(colTags)
                        ),
                        "entry_likelihood": tableInfo["entry_likelihood"],
                        "required_entries_by_ssn": tableInfo["required_entries_by_ssn"],
                        "keys": tableInfo["keys"],
                    }
                )

    except mysql.connector.ProgrammingError as err:
        print("Error: {}".format(err))
        exit(1)

    except:
        print("Something went wrong in createMySQLCursors:", sys.exc_info()[0])
        exit(1)


def createMongoCursors(c):
    # print(c)
    try:
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
        # print(client.list_database_names())
        # Create DBs
        for db, info in c["dbs"].items():
            # print(db, ":", info)
            client.drop_database(db)
            _dbObj = client[db]
            for collection, colInfo in info["collections"].items():
                # print(collection, ":", colInfo)
                _colObj = _dbObj[collection]
                _colObj.drop()

                cursor_group.append(
                    {
                        "type": "mongodb",
                        "db_name": db,
                        "db_obj": _dbObj,
                        "collection_name": collection,
                        "collection_obj": _colObj,
                        "entry_likelihood": colInfo["entry_likelihood"],
                        "required_entries_by_ssn": colInfo["required_entries_by_ssn"],
                        "keys": colInfo["keys"],
                    }
                )

        client.close()

    except:
        print("Something went wrong in createMongoCursors:", sys.exc_info()[0])
        exit(1)


def _mysqlInsert(o, entry, keyIndexMap):
    # print(o["keys"])
    # print(entry)

    attrs = tuple([entry[keyIndexMap[k]] for k in o["keys"]])
    o["cursor"].execute(o["statement"], attrs)
    o["db_obj"].commit()


def _mongodbInsert(o, entry, keyIndexMap):
    # print(o)
    # print(entry)
    # print(keyIndexMap)
    doc = dict()
    for k in o["keys"]:
        doc[k] = entry[keyIndexMap[k]]

    o["collection_obj"].insert_one(doc)


def insertData():
    print("inserting data...")
    # print(cursor_group)
    # print(data)
    keyIndexMap = None

    db_type_map = {"mysql": _mysqlInsert, "mongodb": _mongodbInsert}

    for entry in data:
        if keyIndexMap is None:
            keyIndexMap = dict()
            for k in range(len(entry)):
                keyIndexMap[entry[k]] = k
            continue

        rn = rd.random()
        for c in cursor_group:
            if (
                rn > c["entry_likelihood"]
                and entry[keyIndexMap["ssn"]] not in c["required_entries_by_ssn"]
            ):
                continue

            if not c["type"] in db_type_map:
                raise Exception("Bad db type in cursor_group: " + c)

            db_type_map[c["type"]](c, entry, keyIndexMap)


if __name__ == "__main__":
    # print(sys.argv)
    if len(sys.argv) != 2:
        print("Expected one arguement (path to CSV file of data)")
        exit(1)

    checkMySQLConnectionAllowed()
    checkMongoConnectionAllowed()

    readCsv()

    createMySQLCursors(config["mysql"])
    createMongoCursors(config["mongodb"])

    # print(cursor_group)
    insertData()

    print("\n\n...All done!")

