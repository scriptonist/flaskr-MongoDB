from flaskr import app
import unittest
from pymongo import MongoClient


class BasicTestCase(unittest.TestCase):
    def test_website_online(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_db_exists(self):
        with app.app_context():
            client = MongoClient()
            self.assertNotEqual(client, None)


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        """ Setup   A blank database for testing """
        app.config.from_object('config.TestingConfig')
        self.client = MongoClient(app.config["MONGO_URI"])
        self.db = self.client[app.config['DB']]
        self.collection = self.db[app.config['COLLECTION']]
        self.collection.insert_one(({"test": "test"}))
        self.app = app.test_client()

    def tearDown(self):
        """ Destroy Blank Database After each Test"""
        self.client.drop_database("test_db_flaskr")
        app.config.from_object('config.DevelopmentConfig')

    def login(self, username, password):
        """ Login Helper Function """
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """ Logout Helper Function """
        return self.app.get("/logout", follow_redirects=True)
    # Assert Functions

    def test_empty_db(self):
        """ ensure that the database is blank """
        rv = self.app.get("/")
        self.assertIn("No entries So far", rv.data.decode("utf-8"))

    def test_login_logout(self):
        """ Test Login and Logout Using Helper Function """
        rv = self.login(app.config['USERNAME'],
                        self.login(app.config['PASSWORD'])
                        )
        self.assertIn("You Were Logged in", rv.data.decode("utf-8"))
        rv = self.logout()
        self.assetIn("You Were Logged Out", rv.data.decode('utf-8'))
        rv = self.login(app.config['USERNAME'] + 'x',
                        self.login(app.config['PASSWORD'])
                        )
        self.assertIn("Invalid Username", rv.data.decode('utf-8'))
        rv = self.login(app.config['USERNAME'],
                        self.login(app.config['PASSWORD'] + 'x')
                        )
        self.assertIn("Invalid Password", rv.data.decode('utf-8'))

    def test_messages(self):
        """ Ensure that the user can post messages """
        self.login(app.config['USERNAME'],
                   self.login(app.config['PASSWORD'])
                   )
        rv = self.app.post("/add", data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        self.assertNotIn("No Entries Here So Far", rv.data.decode('utf-8'))
        self.assertIn('&lt;Hello&gt;', rv.data.decode('utf-8'))
        self.assertIn('<strong>HTML</strong> allowed here', rv.data.decode
                      ('utf-8'))


if __name__ == "__main__":
    unittest.main()
