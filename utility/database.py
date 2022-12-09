from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from resources import config

class DatabaseHandler:
    def __init__(self, db_user, db_password, db_host):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host

    def initialize_database_table(self, db_name):
        '''
        Initalizes table into database.

        Args
            db_name: name of new table in database.
        '''
        conn = pymysql.connect(host=self.db_host, user=self.db_user,
                               password=self.db_password, connect_timeout=10)
        with conn.cursor() as cur:
            cur.execute(f'create database [if not exists] {db_name}')

    def create_connection(self, db_name):
        '''
        Initalizes table into database.

        Args
            db_name: name of new table in database.
        '''
        
        return pymysql.connect(host=self.db_host,
                               port=3306,
                               user=self.db_user,
                               password=self.db_password,
                               database=db_name,
                               cursorclass=pymysql.cursors.DictCursor)

    def upload_csv_to_database(self, path: str, table_name: str):
        '''
        Uploads CSV file containing QA pairs to AWS SQL Database.

        Args
            path: path to csv file. 
            table_name: name of the SQL table. 
        '''
        df = pd.read_csv(path)
        sqlEngine = create_engine(
            f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{table_name}', pool_recycle=3600)
        db_connection = sqlEngine.connect()
        df.to_sql(table_name, db_connection, if_exists='append', index=False)

        db_connection.close()

    def read_sql_table(self, table_name: str):
        '''
        Reads QA pairs from AWS SQL Database.

        Args
            table_name: name of the SQL table. 
        '''

        sqlEngine = create_engine(
            f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{table_name}', pool_recycle=3600)
        db_connection = sqlEngine.connect()
        df = pd.read_sql(table_name, db_connection)
        print(df.head(10))


if __name__ == "__main__":
    handler = DatabaseHandler(config.DB_USER, config.DB_PASSWORD, config.DB_HOST)
    handler.initialize_database_table('test')
    handler.upload_csv_to_database('Search_Problems_question_answer.csv')
    handler.read_sql_table('test')
