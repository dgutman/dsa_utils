import sqlite3
import pandas as pd

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


dbName = 'sqlitedb/confMatrix.db'

raw_message_table = """CREATE TABLE IF NOT EXISTS rawMessageData (
    message_contents BLOB, local_message_id INTEGER,  data_source TEXT, generated_date TEXT,
    message_hash TEXT
)"""

def createMatrixTables( dbName):
    ### Create table to store confusion matrix data
    con = sqlite3.connect(dbName)
    sql = 'CREATE TABLE IF NOT EXISTS dsaItems ( id INTEGER PRIMARY KEY, dsaItemData JSON, itemHash TEXT)'
    con.close()


def createItemTable( dbName):
    ### Create table to store confusion matrix data
    con = sqlite3.connect(dbName)
    df = pd.read_csv("adrcThumbMetadata.csv")
    df.to_sql("dsai",con,if_exists='replace')
    # df = pd.read_sql_query("select * from %s" % tableName, con)

    sql = 'CREATE TABLE IF NOT EXISTS dsaItems ( id INTEGER PRIMARY KEY, dsaItemData JSON, itemHash TEXT)'
    c = con.cursor()
    sql = 'CREATE TABLE IF NOT EXISTS modelResponses ( id INTEGER PRIMARY KEY, modelName TEXT, modelResponse JSON)'
    c.execute(sql)
    con.close()


def insertItemData( dbName):
    ### Create table to store confusion matrix data
    con = sqlite3.connect(dbName)
    # df = pd.read_csv("adrcThumbMetadata.csv")
    # df.to_sql("dsai",con)
    # df = pd.read_sql_query("select * from %s" % tableName, con)

    sql = 'CREATE TABLE IF NOT EXISTS dsaItems ( id INTEGER PRIMARY KEY, dsaItemData JSON, itemHash TEXT)'
    con.close()


# INSERT INTO users (id, data) VALUES (1, json_encode({
#   "name": "Alice",
#   "age": 25,
#   "email": "alice@example.com"
# }));
# Querying JSON Data
# To query this table, you can use the json_extract function, which allows you to extract values from the JSON column by specifying a JSON path. For example, to get the email address of the user with id 1, you can use the following query:

# SELECT json_extract(data, '$.email') AS email
# FROM users
# WHERE id = 1;
    
