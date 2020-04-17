from mysql.connector import MySQLConnection, Error
from pymongo import MongoClient

def _get_mongo_db_connection(db):
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

            return client[db["name"]]
        except:
            pass

def _get_mysql_db_connection(db):
        cnx = None
        try:
            cnx = MySQLConnection(
                user=db["user"], password=db["password"], host=db["host"],
            )
            return cnx
            # cursor = cnx.cursor()
            # return cursor

        except Error as e:
            print("Problem in MySQL Connection: {}".format(e))
        # finally:
        #     if cnx:
        #         cnx.close()



# Gets metadata for a single database
def get_db_metadata(db):
	if db["type"] == "mongo":
		return _get_mongo_db_metadata(db)
	elif db["type"] == "mysql":
		return _get_mysql_db_metadata(db)
	else:
		raise Exception("Unsupported db type")

def _get_mongo_db_metadata(db):
	# connects to mongo db, gets collections, returns info
    db_connection = _get_mongo_db_connection(db)
    collections = db_connection.list_collection_names()
    db["collections"] = collections
	
def _get_mysql_db_metadata(db):
	# connects to mysql db, gets collections, returns info
    db_connection = _get_mysql_db_connection(db)
    db_cursor = db_connection.cursor()
    SCHEMA_COMMAND = "SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE FROM information_schema.columns WHERE table_schema = '{}' ORDER BY TABLE_NAME, ORDINAL_POSITION"
    print(db_cursor)
    print(db)
    # exit()

    # db_cursor.execute("SELECT TABLE_NAME FROM information_schema.columns")
    db_cursor.execute(SCHEMA_COMMAND.format(db["name"]))
    data = db_cursor.fetchall()

    db["tables"] = dict()

    for row in data:
        tableName = row[0]
        if row[0] not in db["tables"]:
            db["tables"][tableName] = dict()

        print(row)
        db["tables"][tableName][row[1]] = row[2]
    
    # exit()

# gets all keys inside a mongo collection, returns array
def get_mongo_keys(db, collection):
	db_connection = _get_mongo_db_connection(db)
	AGGREGATION_PIPELINE  = [
{"$project":{"arrayofkeyvalue":{"$objectToArray":"$$ROOT"}}}, 
{"$unwind":"$arrayofkeyvalue"}, {"$group":{"_id": None,"allkeys":{"$addToSet":"$arrayofkeyvalue.k"}}} 
]
	return list(db[collection].aggregate(AGGREGATION_PIPELINE))

# Samples from single database
def sample_db_table_col(db, table, col, n_items=20):
	if db["type"] == "mongo":
		return _sample_mongo_db_collection_key(db, table, col, n_items)
	elif db["type"] == "mysql":
		return _sample_mysql_db_table_col(db, table, col, n_items)
	else:
		raise Exception("Unsupported db type")

def _sample_mongo_db_collection_key(db, collection, key, n_items):
	db_connection = _get_mongo_db_connection(db)
	data = list( db[collection].aggregate([
    { "$match": { "key": "_is_not_null_" } },
    { "$sample": { "size": n_items } }
]))
	return list(map(lambda x: x[key], data))


def _sample_mysql_db_table_col(db, table, col, n_items):
    db_connection = _get_mysql_db_connection(db)
    db_cursor = _get_mysql_db_connection(db)
    command = "SELECT {} FROM {} ORDER BY RAND() LIMIT {}".format(col, table, n_items)
    db_cursor.execute(command)
    data = db_cursor.fetchall()
    return data
