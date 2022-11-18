
from itertools import chain
import logging
import os

import psycopg
from psycopg.rows import dict_row

class DBConnector:

    def __init__(self) -> None:

        try:
            self.db_params = {
                'DB_USER': os.environ.get('DB_USER'),
                'DB_PASSWORD': os.environ.get('DB_PASSWORD'),
                'DB_HOST': os.environ.get('DB_HOST'),
                'DB_PORT': int(os.environ.get('DB_PORT')),
                'DB_DATABASE': os.environ.get('DB_DATABASE'),
            }

            self.connect()
        except Exception as e:
            logging.error('Cannot connect to db:', e)

    def connect(self):
        self.connection = psycopg.connect(f'host={ self.db_params["DB_HOST"] } port={ self.db_params["DB_PORT"] } user={ self.db_params["DB_USER"] } password={ self.db_params["DB_PASSWORD"] } dbname={ self.db_params["DB_DATABASE"] } ', options="-c search_path=chain_1,chain_4,chain_56,chain_137,dao,public")

    ########## AUTH ##########
    def get_app_key(self, app_id: str):
        if app_id is None:
            return []

        if self.connection.closed:
            self.connect()

        with self.connection.cursor(row_factory=dict_row) as cur:
            query = f'''
                SELECT *
                FROM public.auth_clients
                WHERE LOWER("public"."auth_clients"."app_id") = '{app_id.lower()}'
            '''
            cur.execute(query)
            output = []
            records = cur.fetchall()
            for item in records:
                output.append(item)

            return output
    ########## END AUTH ##########

dbconnector = DBConnector()