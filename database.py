import pyodbc
import pandas as pd

def connect_to_database(server_name, database, username, password):
    connection_string = f"DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database};UID={username};PWD={password}"
    connection = pyodbc.connect(connection_string)
    return connection

def execute_query(connection, query):
    df = pd.read_sql(query, connection)
    return df
