from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from auth import AuthError, requires_auth
from models import setup_db, Team, Player

# This creates and configures the app.
def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path, test=True)
    
    # CORS is set up to allow '*' for origins
    CORS(app)

    # The '/teams' GET endpoint returns a success indicator, and a list of formatted teams
    # or an appropiate status code and message in case of failure.
    @app.route('/teams', methods=['GET'])
    @requires_auth('get:teams')
    def retrieve_teams(jwt):
        team_list = Team.query.all()

        return jsonify(
            {
                'success': True,
                'teams': [team.format() for team in team_list],
            }
        ), 200
    
    # The '/teams/<int:id>' GET endpoint returns a success indicator, a team name, and a list of player names
    # or an appropiate status code and message in case of failure.
    @app.route('/teams/<int:id>', methods=['GET'])
    @requires_auth('get:teams/id')
    def retrieve_team(jwt, id):
        team = Team.query.filter(Team.id == id).one_or_none()

        if team is None:
            abort(404)
        
        return jsonify(
            {
                'success': True,
                'name': team.name,
                'players': [player.long() for player in team.players],
            }
        ), 200
    
    # The '/teams' POST endpoint creates a team and returns a success indicator, the team name, and an empty list of players,
    # or an appropiate status code and message in case of failure.
    @app.route('/teams', methods=['POST'])
    @requires_auth('post:teams')
    def create_team(jwt):
        try:
            body = request.get_json()
            new_name = body.get('name')

            new_team = Team(name=new_name, players=[])
            new_team.insert()

            return jsonify(
                {
                    'success': True,
                    'team': new_team.format(),
                }
            ), 200
        
        except:
            abort(422)

    # The '/teams/<int:id>' PATCH endpoint updates a team's name and returns a success indicator, the team name, 
    # and a list of players or an appropiate status code and message in case of failure.
    @app.route('/teams/<int:id>', methods=['PATCH'])
    @requires_auth('patch:teams')
    def update_team(jwt, id):
        team = Team.query.filter(Team.id == id).one_or_none()

        if team is None:
            abort(404)

        try:
            body = request.get_json()
            new_name = body.get('name')

            team.name = new_name
            team.update()

            return jsonify(
                {
                    'success': True,
                    'team': team.format(),
                }
            ), 200
        
        except:
            abort(422)

    # The '/teams/<int:id>' DELETE endpoint deletes a team and returns a success indicator and the deleted id
    # or an appropiate status code and message in case of failure.
    @app.route('/teams/<int:id>', methods=['DELETE'])
    @requires_auth('delete:teams')
    def delete_team(jwt, id):
        team = Team.query.filter(Team.id == id).one_or_none()

        if team is None:
            abort(404)
        
        try:
            for player in team.players:
                player.team = None
            team.delete()
            return jsonify(
                {
                    'success': True,
                    'deleted': id,
                }
            ), 200
        
        except:
            abort(422)

    # The '/players' GET endpoint returns a success indicator, and a list of players with abreviated information for each
    # or an appropiate status code and message in case of failure.
    @app.route('/players', methods=['GET'])
    @requires_auth('get:players')
    def retrieve_players(jwt):
        player_list = Player.query.all()

        return jsonify(
            {
                'success': True,
                'players': [player.short() for player in player_list],
            }
        ), 200
    
    # The '/players/<int:id>' GET endpoint returns a success indicator, and information about a player
    # or an appropiate status code and message in case of failure.
    @app.route('/players/<int:id>', methods=['GET'])
    @requires_auth('get:players/id')
    def retrieve_player(jwt, id):
        player = Player.query.filter(Player.id == id).one_or_none()

        if player is None:
            abort(404)

        return jsonify(
            {
                'success': True,
                'player': player.long(),
            }
        ), 200
    
    # The '/players' POST endpoint creates a player and returns a success indicator and information about the player
    # or an appropiate status code and message in case of failure.
    @app.route('/players', methods=['POST'])
    @requires_auth('post:players')
    def create_player(jwt):
        try:
            body = request.get_json()
            new_name = body.get('name')
            new_position = body.get('position')
            new_height = body.get('height')
            new_team = body.get('team_id', None)

            player = Player(name=new_name, position=new_position, height=new_height, team_id=new_team)
            player.insert()

            return jsonify(
                {
                    'success': True,
                    'player': player.long(),
                }
            ), 200
        
        except:
            abort(422)

    # The '/players/<int:id>' PATCH endpoint updates a player's information and returns a success indicator and updated 
    # information about the player or an appropiate status code and message in case of failure.
    @app.route('/players/<int:id>', methods=['PATCH'])
    @requires_auth('patch:players')
    def update_player(jwt, id):
        player = Player.query.filter(Player.id == id).one_or_none()

        if player is None:
            abort(404)

        try:
            body = request.get_json()
            new_name = body.get('name', player.name)
            new_position = body.get('position', player.position)
            new_height = body.get('height', player.height)
            new_team = body.get('team_id', player.team_id)

            player.name = new_name
            player.position = new_position
            player.height = new_height
            player.team_id = new_team
            player.update()

            return jsonify(
                {
                    'success': True,
                    'player': player.long(),
                }
            ), 200
        
        except:
            abort(422)

    # The '/teams/<int:id>' DELETE endpoint deletes a player and returns a success indicator and the deleted id
    # or an appropiate status code and message in case of failure.
    @app.route('/players/<int:id>', methods=['DELETE'])
    @requires_auth('delete:players')
    def delete_player(jwt, id):
        player = Player.query.filter(Player.id == id).one_or_none()

        if player is None:
            abort(404)
        
        try:
            player.delete()
            return jsonify(
                {
                    'success': True,
                    'deleted': id,
                }
            ), 200
        
        except:
            abort(422)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "not_found"
    }), 404

    @app.errorhandler(405)
    def bad_method(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "bad_method"
    }), 405

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
