from sqlalchemy import create_engine
import pymysql
import pandas as pd

DB_USER = 'admin'
DB_PASSWORD = 'CIS400401'
DB_HOST = 'seniordesign.ccaubeo15ans.us-east-2.rds.amazonaws.com'
DB_NAME = 'CIS521'


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
        conn = pymysql.connect(host=DB_HOST, user=DB_USER,
                               password=DB_PASSWORD, connect_timeout=10)
        with conn.cursor() as cur:
            cur.execute(f'create database {db_name}')

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

    def upload_csv_to_database(self, path: str, class_name: str):
        '''
        Uploads CSV file containing QA pairs to AWS SQL Database.

        Args
            path: path to csv file 
            class_name: the name of the class corresponding to the qa pairs.
                For example if the questions are generated from qa pairs
                for CIS521, class_name would be CIS521.
        '''
        df = pd.read_csv(path)
        sqlEngine = create_engine(
            f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{class_name}', pool_recycle=3600)
        db_connection = sqlEngine.connect()
        df.to_sql(class_name, db_connection, if_exists='replace', index=False)

        db_connection.close()

    def read_sql_table(self, class_name: str):
        sqlEngine = create_engine(
            f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{class_name}', pool_recycle=3600)
        db_connection = sqlEngine.connect()
        df = pd.read_sql(class_name, db_connection)
        print(df.head(10))


if __name__ == "__main__":
    print('hello')
