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
        conn = self.create_connection()
        with conn.cursor() as cur:
            cur.execute(f'create database if not exists {db_name}')

    def create_connection(self):
        '''
        Connects to Database.

        '''
        
        return pymysql.connect(host=self.db_host,
                               port=3306,
                               user=self.db_user,
                               password=self.db_password,
                               database=config.DB_NAME,
                               cursorclass=pymysql.cursors.DictCursor)
    
    def search_questions_by_criteria(self, table_name: str, criteria: dict[str, str]):
        '''
        Searches for questions in database by criteria.

        Args
            criteria: dictionary of criteria to search by. 
        '''
        criteria = ' and '.join([f'{key} = "{value}"' for key, value in criteria.items()])
        conn = self.create_connection()
        with conn.cursor() as cur:
            cur.execute(f'select * from {table_name} where {criteria}')
            return cur.fetchall()
        

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
