import os
import unittest
import json
from app import create_app
from models import db_drop_and_create_all

auth_header_admin = {'Authorization': os.environ['ADMIN_TOKEN']}
auth_header_analyst = {'Authorization': os.environ['ANALYST_TOKEN']}

new_team = {
    'name': 'Bulls',
    'players': []
}

new_player = {
    'name': 'Michael Jordan',
    'height': "6'6",
    'position': 'Shooting Guard'
}

new_player2 = {
    'name': 'Vince Carter',
    'height': "6'6",
    'position': 'Shooting Guard'
}

class ManagerTestCase(unittest.TestCase):

    # Sets up the testing app
    @classmethod
    def setUpClass(self):
        self.database_name = 'bball_test'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', 'abc', 'localhost:5432', self.database_name)

        self.app = create_app({
            'SQLALCHEMY_DATABASE_URI': self.database_path
        })
        self.client = self.app.test_client
    
    def setUp(self):
        pass

    # Executed after each test
    def tearDown(self):
        pass
    # Tests are made for each endpoint, including expected results for successes and errors, as well as tests for RBAC.

    # Passing test for GET '/teams'
    def test_get_teams(self):
        res = self.client().get('/teams', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['teams']), 3)

    # Failing test for GET '/teams'
    def test_401_get_teams_without_authorization(self):
        res = self.client().get('/teams')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    # Passing test for GET '/players'
    def test_get_players(self):
        res = self.client().get('/players', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['players']), 3)
    
    # Failing test for GET '/players'
    def test_401_get_players_without_authorization(self):
        res = self.client().get('/players')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Passing test for GET '/teams/<int:id>'
    def test_get_team_by_id(self):
        res = self.client().get('/teams/1', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], 'Heat')
        self.assertEqual(len(data['players']), 1)
    
    # Failing test for GET '/teams/<int:id>'
    def test_404_team_not_exist(self):
        res = self.client().get('/teams/500', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Passing test for GET '/players/<int:id>'
    def test_get_player_by_id(self):
        res = self.client().get('/players/1', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player']['name'], 'Lebron James')
        self.assertEqual(data['player']['team'], 'Heat')

    # Failing test for GET '/players/<int:id>'
    def test_404_player_not_exist(self):
        res = self.client().get('/players/1000', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    # Passing test for POST '/teams'
    def test_create_team(self):
        res = self.client().post('/teams', json=new_team, headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['team']['name'], 'Bulls')

    # Failing test for POST '/teams'
    def test_422_create_team(self):
        res = self.client().post('/teams', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    # Passing test for POST '/players'
    def test_create_player(self):
        res = self.client().post('/players', json=new_player, headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player']['name'], 'Michael Jordan')
        self.assertEqual(data['player']['team'], 'Free Agent')

    # Failing test for POST '/players'
    def test_422_create_player(self):
        res = self.client().post('/players', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Passing test for PATCH '/teams/<int:id>'
    def test_update_team(self):
        res = self.client().patch('/teams/1', json={"name": "Miami Heat"}, headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['team']['name'], 'Miami Heat')

    # Failing test for PATCH '/teams/<int:id>'
    def test_422_update_team_no_data(self):
        res = self.client().patch('/teams/1', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # Passing test for PATCH '/players/<int:id>'
    def test_update_player(self):
        res = self.client().patch('/players/2', json={"position": "Shooting Guard"}, headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player']['name'], 'Jalen Brunson')
        self.assertEqual(data['player']['team'], 'Knicks')
    
    # Failing test for PATCH '/players/<int:id>'
    def test_404_update_player_not_exist(self):
        res = self.client().patch('/players/100', json={"name": "Jowl Embiid"}, headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Passing test for DELETE '/teams/<int:id>'
    def test_delete_team(self):
        res = self.client().delete('/teams/3', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    # Failing test for DELETE '/teams/<int:id>'
    def test_404_delete_team(self):
        res = self.client().delete('/team/30', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    # Passing test for DELETE '/players/<int:id>'
    def test_delete_player(self):
        res = self.client().delete('/players/3', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    # Failing test for DELETE '/players/<int:id>'
    def test_404_delete_player(self):
        res = self.client().delete('/player/30', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # Passing test for analyst role
    def test_analyst_get_players(self):
        res = self.client().get('/players', headers=auth_header_analyst)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['players']), 3)

    # Failing test for analyst role
    def test_403_analyst_delete_player(self):
        res = self.client().delete('/players/1', headers=auth_header_analyst)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # Passing test for admin role
    def test_admin_delete_player(self):
        res = self.client().delete('/players/4', headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)

    # Passing test for admin role
    def test_admin_create_player(self):
        res = self.client().post('/players', json=new_player2, headers=auth_header_admin)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['player']['name'], 'Vince Carter')
        self.assertEqual(data['player']['team'], 'Free Agent')

if __name__ == '__main__':
    unittest.main()