from pymongo import MongoClient
import statistics_creator


def create_db_connection():
    DB_NAME = 'bpm'
    HOST = 'localhost'
    PORT = 27017
    CONNECTION_STRING = f'mongodb://{HOST}:{PORT}/{DB_NAME}?authSource=admin'
    client = MongoClient(CONNECTION_STRING)
    return client


def handle_data(data: object):
    c = create_db_connection()
    coll = c['bpm']['data']
    coll.insert_many(data['data'])
    statistics_creator.run_statistics_job()
    return "data saved"

# using for tests


def init_database():
    client = create_db_connection()
    client.drop_database('bpm')
    db = client['bpm']
    coll = db['data']
    coll.insert_one({})
