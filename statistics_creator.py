import threading
import queue
import db as mongo_client
import numpy as np

q1 = queue.Queue()


def run_statistics_job():
    client = mongo_client.create_db_connection()
    collection = client["bpm"]['data']
    q1.put((create_avg_stats, [collection]))


def create_avg_stats(collection):

    data_list = list(collection.find({"day": {"$gte": 1}}))
    for item in data_list:
        measures_np = np.array([
            [
                item['measures']['am']['dia'],
                item['measures']['pm']['dia'],
            ],
            [
                item['measures']['am']['sys'],
                item['measures']['pm']['sys'],
            ],
        ])

        collection.update_one(
            {"_id": item['_id']},
            {
                "$set": {
                    "avg_dia": measures_np[0].mean(),
                    "avg_sys": measures_np[1].mean()
                }
            }
        )


def execute_background_process():
    while True:
        f, args = q1.get()
        f(*args)


threading.Thread(target=execute_background_process, daemon=True).start()
