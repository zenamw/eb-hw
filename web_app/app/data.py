"""
data.py

Module to get data from different sources
"""
from sqlalchemy import create_engine
import pandas as pd
import logging

from configs import App_Configs

class PG_Data():
    def __get_engine(self):
        try:
            engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(user = App_Configs.pg_user,
                                                                                  password = App_Configs.pg_pass,
                                                                                  host = App_Configs.pg_host,
                                                                                  port = App_Configs.pg_port,
                                                                                  db = App_Configs.pg_db))
            engine.connect()


        except:
            
            logging.error('Unable to connect to postgres')
            print('Unable to make engine connect to Postgres')
            engine = None
            raise Exception

        return engine 

    def __close_engine(self, engine):
        if engine != None:
            print('disposing engine')
            engine.dispose()

    def get_all_data(self):

        # Put a limit here because it is slow when loading to browser
        try:
            engine = self.__get_engine()
            
            logging.info('attempting to get all airlines data')
            query = """SELECT * FROM airlines LIMIT 100;"""
            airlines = pd.read_sql(query, engine)

            self.__close_engine(engine)
        except Exception as err:
            logging.error('Unable to get data from {db}'.format(db = App_Configs.pg_db), err)
            print('Unable to get data from {db}'.format(db = App_Configs.pg_db), err)
            airlines = None

        return airlines

    def get_airport_data(self, airport):

        try:
            engine = self.__get_engine()
            query = """SELECT *
	                FROM airlines
                    WHERE "Origin_airport" = '{airport_acronym}'""".format(airport_acronym = airport)
        
            dat = pd.read_sql(query, engine)
            self.__close_engine(engine)
        except Exception as err:
            print('Unable to get data from {db}'.format(db = App_Configs.pg_db), err)
            dat = None

        return dat
       
       