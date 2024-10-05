import os
from flask_sqlalchemy import SQLAlchemy

# These are variables used to connect flask application to local database. Uncomment These out to run the app locally

# database_name = 'bball_manager'
# database_path = 'postgresql://{}:{}@{}/{}'.format('postgres', 'abc', 'localhost:5432', database_name)

# Comment this out and uncomment the above database path variables to run locally
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

# Binds the running flask application to a SQLAlchemy service.
def setup_db(app, database_path=database_path, test=False):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    if test:
        db_drop_and_create_all()

# Resets database and creates demo rows for testing
def db_drop_and_create_all():
    db.session.close()
    db.drop_all()
    db.create_all()

    team1 = Team(
        name = "Heat",
        players = []
    )
    team1.insert()

    team2 = Team(
        name = "Knicks",
        players = []
    )
    team2.insert()

    team3 = Team(
        name = "Nets",
        players = []
    )
    team3.insert()

    player1 = Player(
        name = "Lebron James",
        position = "Small Forward",
        height = "6'9",
        team_id = 1
    )
    player1.insert()

    player2 = Player(
        name = "Jalen Brunson",
        position = "Point Guard",
        height = "6'2",
        team_id = 2
    )
    player2.insert()

    player3 = Player(
        name = "Luka Doncic",
        position = "Point Guard",
        height = "6'7",
        team_id = None
    )
    player3.insert()

#Creates a class that models the teams table.
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    players = db.relationship('Player', backref='team', lazy=True)

    def __init__(self, name, players):
        self.name = name
        self.players = players

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        if self.players is None:
            player_list = []
        else:
            player_list = []
            for player in self.players:
                player_list.append(player.name)
        return {
            'id': self.id,
            'name': self.name,
            'players': player_list,
        }
    

#Creates a class that models the players table.
class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    height = db.Column(db.String(120), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)

    def __init__(self, name, position, height, team_id):
        self.name = name
        self.position = position
        self.height = height
        self.team_id = team_id
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        if self.team_id is None:
            team = "Free Agent"
        else:
            team = self.team.name

        return {
            'id': self.id,
            'name': self.name,
            'team': team,
        }
    
    def long(self):
        if self.team_id is None:
            team = "Free Agent"
        else:
            team = self.team.name

        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'height': self.height,
            'team': team,
        }