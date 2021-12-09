import unittest
import random
import app
import db


class DBTests(unittest.TestCase):
    '''
    Sets up the test
        self.app: creates a Flask instance with test_client
        self.db: creates a mongodb client
        self.sample_upload_data: generates sample Sys/Dia data structure
    '''

    def setUp(self):
        self.app = app.createTestClient()
        self.db = db.create_db_connection()
        self.sample_upload_data = sample_data_helper()

    # test if the API is available
    def test_site_health_check(self):
        response = self.app.get('/ping')
        self.assertEqual(response.data, b'1')

    # tests if bpm db exists
    def test_database_exists(self):
        self.assertIn('bpm', self.db.list_database_names())

    # this should fail, because it's sending data instead of json
    def test_upload_failed(self):
        response = self.app.post(
            '/upload',
            data=self.sample_upload_data,
            content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # seeds up the databas through /upload API endpoint
    def test_upload_success(self):
        # drops and recreates the database
        db.init_database()
        response = self.app.post(
            '/upload',
            json=self.sample_upload_data,
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'data saved')


def sample_data_helper():
    sample_data = dict({"data": list()})
    for i in range(0, 365):

        sample_data['data'].append(dict(
            {
                "day": (i+1),
                "measures": dict({
                    "am":
                    {
                        "sys": random.randint(100, 175),
                        "dia": random.randint(100, 120)
                    },
                    "pm":
                    {
                        "sys": random.randint(100, 150),
                        "dia": random.randint(70, 90)
                    }
                })
            }
        ))
    return sample_data


if __name__ == '__main__':
    unittest.main()
