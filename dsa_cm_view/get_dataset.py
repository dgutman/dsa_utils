import sqlite3
import dash_bootstrap_components as dbc
import pandas as pd


# Connect to the sqlite database
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def getConfusionMatrixData(dbName):
    con = sqlite3.connect(dbName)
    con.row_factory = dict_factory
    c = con.cursor()

    c.execute('select modelLabel, "meta.npSchema.stainID" as currentStain, *  from modelResponses m left join dsai on "_id"=imageId')
    mr_df = pd.DataFrame(c.fetchall())
    con.close()
    return mr_df


# This will return the dataframe being used by the dash ap


# table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

# How to describe a table
# c.execute("PRAGMA table_info('modelResponses');")
