import sys
import os
import json
import csv
import mysql.connector
import random as rd
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


def insertMySQLData(c):
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
                        "keys": tableInfo["keys"],
                    }
                )

    except mysql.connector.ProgrammingError as err:
        print("Error: {}".format(err))
        exit(1)

    except:
        print("Something went wrong inserting the MySQL data:", sys.exc_info()[0])
        # print("Unexpected error:", )
        exit(1)


def insertMongoData(c):
    # print(c)
    try:
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)

        # Create DBs
        for db, info in c["dbs"].items():
            print(db, ":", info)

        client.close()

    except:
        print("Something went wrong inserting the Mongo data")
        exit(1)


def _mysqlInsert(o, entry):
    print(o)
    print(entry)
    attrs = tuple([entry[k] for k in o["keys"]])
    # for k in o["keys"]:
    #     attrs.append(entry[k])
    print(o["statement"])
    print(attrs)
    o["cursor"].execute(o["statement"], attrs)
    o["db_obj"].commit()


def insertData():
    # print(cursor_group)
    print(data)
    for entry in data:
        for c in cursor_group:
            if rd.random() > c["entry_likelihood"]:
                continue

            if c["type"] == "mysql":
                _mysqlInsert(c, entry)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Expected one arguement (path to CSV file of data)")
        exit(1)

    checkMySQLConnectionAllowed()
    checkMongoConnectionAllowed()

    readCsv()

    insertMySQLData(config["mysql"])
    # insertMongoData(config["mongodb"])

    insertData()
