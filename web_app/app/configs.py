"""
configs.py

Contains environmental variables to be used in the app
"""
import os

class App_Configs():
    authorization = os.getenv('AUTHORIZATION')
    cron_string = '* * * * *'
    pg_user = os.getenv('PG_USER')
    pg_pass = os.getenv('PG_PASS')
    pg_host = os.getenv('PG_HOST')
    pg_port = os.getenv('PG_PORT')
    pg_db = os.getenv('PG_DB')
