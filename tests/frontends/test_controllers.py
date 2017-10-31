import json
import unittest

from app import create_app
from app.database import db
from tests.factories import BasePersonFactory


class PeopleTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.person = BasePersonFactory()
        self.person_json = self.person.to_json()

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_person_creation(self):
        """Test API can create a person (POST request)"""
        res = self.client().post(
            '/api/frontends/',
            content_type='application/json',
            data=self.person_json)
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.person.name, str(res.data))

    def test_api_can_get_all_people(self):
        """Test API can get a frontends list (GET request)."""
        res = self.client().post(
            '/api/frontends/',
            content_type='application/json',
            data=self.person_json)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/frontends/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.person.name, str(res.data))

    def test_api_can_get_person_by_id(self):
        """Test API can get a single person by using it's id."""
        rv = self.client().post(
            '/api/frontends/',
            content_type='application/json',
            data=self.person_json)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/api/frontends/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn(self.person.name, str(result.data))

    def test_person_can_be_edited(self):
        """Test API can edit a person. (PUT request)"""
        new_person = BasePersonFactory()
        res = self.client().post(
            '/api/frontends/',
            content_type='application/json',
            data=self.person_json)
        self.assertEqual(res.status_code, 201)
        id = json.loads(res.data.decode('utf-8').replace("'", "\""))['id']
        res = self.client().put(
            '/api/frontends/' + id,
            content_type='application/json',
            data=new_person.to_json())
        self.assertEqual(res.status_code, 200)
        self.assertIn(new_person.name, str(res.data))
        res = self.client().get('/frontends/' + id)
        self.assertEqual(res.status_code, 404)

    def test_person_deletion(self):
        """Test API can delete an existing person. (DELETE request)."""
        res = self.client().post(
            '/api/frontends/',
            content_type='application/json',
            data=self.person_json)
        self.assertEqual(res.status_code, 201)
        id = json.loads(res.data.decode('utf-8').replace("'", "\""))['id']
        res = self.client().delete('/api/frontends/' + id)
        self.assertEqual(res.status_code, 204)
        # Test to see if it exists, should return a 404
        res = self.client().get('/frontends/{}'.format(id))
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
