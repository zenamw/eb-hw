from flask import Flask, request
from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import create_engine
import pandas as pd
import json
import os
import logging
from dotenv import load_dotenv

from configs import App_Configs
from data import PG_Data
from verify import verify
from logic import print_time

logging.basicConfig(filename = 'app_logs.log',  level = logging.DEBUG)
pg_data = PG_Data()

app = Flask(__name__)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

scheduler.add_job(func = print_time, trigger = CronTrigger.from_crontab(App_Configs.cron_string), name = 'print time', id = '1')

@app.route('/health-check')
def health_check():
    return 'OK'

@app.route('/get_all_data', methods = ['GET'])
def get_all_data():
    logging.info('Checking auth token')
    auth_token = request.headers.get('Authorization')
    if not verify(auth_token):
        logging.info('Do not have the correct auth token')
        return 'Do not have the correct auth token', 400

    logging.info('getting_all_data')
    airlines = pg_data.get_all_data()

    return airlines.to_json()

@app.route('/get_origin_airport_data', methods = ['POST'])
def get_airport_data():
    auth_token = request.headers.get('Authorization')

    if not verify(auth_token):
        return 'Do not have the correct auth token', 400

    params = request.get_json(force = True)
    
    if 'airport' not in params:
        return 'Missing arguement: airport', 400

    else:
        dat =  pg_data.get_airport_data(params['airport'])
        return dat.to_json(), 200

if __name__ == '__main__':
    load_dotenv('../env_vars.env')
    app.run(host= '0.0.0.0', port=5000, debug = True)