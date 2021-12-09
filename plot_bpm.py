import db
from matplotlib import pyplot as plt
import numpy as np
import uuid
from flask.helpers import send_file
from flask import after_this_request
import os


def show():
    client = db.create_db_connection()
    dbase = client['bpm']
    coll = dbase['data']
    data_list = list(coll.find({"day": {"$gte": 1}}))
    count = len(data_list)
    filename = uuid.uuid4().hex.upper()[0:6]+'.png'
    plt.xlabel("DAYS")
    plt.ylabel("AVG DIA/SYS")
    plt.title(f'BPM data from the last {count} days')
    x = range(0, count)
    y1 = list(map(lambda x: x['avg_dia'], data_list))
    y2 = list(map(lambda x: x['avg_sys'], data_list))
    avg_dia_overall = np.repeat(np.array(y1).mean(), count)
    avg_sys_overall = np.repeat(np.array(y2).mean(), count)
    line1, = plt.plot(x, y1, color="blue")
    line2, = plt.plot(x, y2, color="red")
    line3, = plt.plot(x, avg_dia_overall, color="yellow")
    line4, = plt.plot(x, avg_sys_overall, color="green")
    plt.legend(
        (line1, line2, line3, line4),
        (
            "Average DIA (daily)", "Average SYS (daily)",
            "Overall average DIA", "Overall average SYS"
        )
    )
    plt.show()
    plt.savefig(filename)
    plt.figure().clear()

    @after_this_request
    def remove_file(request):
        os.remove(filename)
        return request
    return send_file(filename, 'image/png')
