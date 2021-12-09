import db
import plot_bpm
from flask import request, Blueprint, Flask
from flask_expects_json import expects_json

app = Flask(__name__)

db_api = Blueprint('db', __name__)
plot_bpm_bp = Blueprint('plot_bpm', __name__)
schema = {
    'type': 'object',
    'properties': {
        'data': {'type': 'array'}
    },
    'required': ['data']
}


@db_api.route('/ping')
def health_check():
    return '1'


@db_api.route('/upload', methods=['POST'])
@expects_json(schema)
def save_data():
    return db.handle_data(request.get_json())


@plot_bpm_bp.route('/statistics', methods=['GET'])
def return_statistics():
    return plot_bpm.show()


def createTestClient():
    return app.test_client()


app.register_blueprint(db_api)
app.register_blueprint(plot_bpm_bp)
