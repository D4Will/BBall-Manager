# BBall-Manager
Manage teams of basketball players and list details about players.

### Project motivation
This API allows for the making of custom basketball teams with custom players. This api could be used as part of fantasy sports leagues or managing teams for local basketball leagues.

### Hosted URL
The hosted api can be accessed through `https://bball-manager.onrender.com` from Render. Look below for authorization tokens.
### Project dependencies and platforms
* Flask - A backend microservices framework
* SQLAlchemy - A Python SQL toolkit
* PostgreSQL - A powerful relational database
* Auth0 - An authentication and authurization system
* Render - A cloud service for api deployment

## Setting up locally
#### Installing dependencies
Python 3.12.7 - This project was created using this version of Python, use this version for the least incompatibilties.

virtualenv - Set up a virtualenv to provide a fresh environent for the project dependencies. Use the -p flag to set a specific version of Python.

In your set up environment run the code below to install all the needed dependencies from the requirements.txt file.

```bash
pip install -r requirements.txt
```
### Database setup
If postgreSQL is not already installed on your local machine, install it following the directions from the [postgreSQL website](https://www.postgresql.org/download/). This project was created using postgreSQL 15.

To run this project locally, you will have to create two databases, one for the main environment and one for the testing environment. The names can be set to anything. This can be done by entering into psql on the command line and running the create database command.

For local running, the database path will have to be updated at the top of models.py and test_app.py to work with your local postgreSQL environement. Additionally the app is using the internal database path for hosting on Render, the comments at the top of models.py indicate how to switch the path for local running.

### Auth0
Auth0 is needed for generating Bearer tokens for the api's authentication and authorization. You will have to make an account if your want to configure the authentication. You will have to update the variables shown below in setup.sh after setting up your Auth0 application.

```bash
AUTH0_DOMAIN=[your tenent domain]
ALGORITHMS="RS256"
API_AUDIENCE=[your api audience]
ADMIN_TOKEN=[created token]
ANALYST_TOKEN=[created token]
```

### Roles and permissions
The following Permissions are used in this application
* get:teams
* get:players
* get:teams/id
* get:players/id
* post:teams
* post:players
* patch:teams
* patch:players
* delete:teams
* delete:players

The following Roles are used in this application
*Analyst
  * Can retrieve information about teams and players
*Administrator
  * Can retrieve information about teams and players
  * Can create new teams and players
  * Can update teams and players
  * Can delete teams and players

If you do not want to create and set up Auth0 locally, you can use the following Bearer tokens to gain authorization for the endpoints, although they expire in a couple of days.
```bash
ANALYST_TOKEN="bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY1RThjQmNUNlh0Q1VsYWdQQVQ1SiJ9.eyJpc3MiOiJodHRwczovL2Rldi1xMGE4MnJjbGxlY2wxYWY1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJxMFplMm9OeDNnWDFIVzI3VmxSVHhIOWNXR1B5aHlJNEBjbGllbnRzIiwiYXVkIjoiYmJhbGwiLCJpYXQiOjE3MjgwNzY0MTYsImV4cCI6MTcyODQyMjAxNiwic2NvcGUiOiJnZXQ6dGVhbXMgZ2V0OnBsYXllcnMgZ2V0OnRlYW1zL2lkIGdldDpwbGF5ZXJzL2lkIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoicTBaZTJvTngzZ1gxSFcyN1ZsUlR4SDljV0dQeWh5STQiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dGVhbXMiLCJnZXQ6cGxheWVycyIsImdldDp0ZWFtcy9pZCIsImdldDpwbGF5ZXJzL2lkIl19.HX_4jb5Oz25CFt8zBroKOqbXoTQivFLix8syRFAW2gow-7BAKgXRyNcfohFh0sU-UWKZ1mIfNF07vIIr2F9TZHwR5El9LapCRx_zUNihCKWjPtY8xHpvo8UAJkJBSlaDKEVyd8aM199yeVZPfBnB70fOKRHQylxW55Udz5dQ0VILIMneeVvUznHS_Rym7zOW2z1Q93TGOw7CL25h48rLuys2wu7H_lpAl9zulJu7wrPDYpJJk3hyIsPMkW_n9SYo4xJzTQbK6EtCszVTMCZSxXt4CxpDfacnh1QCgd15kNCoO-YgeFjgcjjV5Ul98157nLvPLAgZGVFwFDTAbD27cw"
ADMIN_TOKEN="bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY1RThjQmNUNlh0Q1VsYWdQQVQ1SiJ9.eyJpc3MiOiJodHRwczovL2Rldi1xMGE4MnJjbGxlY2wxYWY1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJxMFplMm9OeDNnWDFIVzI3VmxSVHhIOWNXR1B5aHlJNEBjbGllbnRzIiwiYXVkIjoiYmJhbGwiLCJpYXQiOjE3MjgwNzY0ODksImV4cCI6MTcyODQyMjA4OSwic2NvcGUiOiJnZXQ6dGVhbXMgZ2V0OnBsYXllcnMgcG9zdDp0ZWFtcyBwb3N0OnBsYXllcnMgcGF0Y2g6dGVhbXMgcGF0Y2g6cGxheWVycyBkZWxldGU6dGVhbXMgZGVsZXRlOnBsYXllcnMgZ2V0OnRlYW1zL2lkIGdldDpwbGF5ZXJzL2lkIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoicTBaZTJvTngzZ1gxSFcyN1ZsUlR4SDljV0dQeWh5STQiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6dGVhbXMiLCJnZXQ6cGxheWVycyIsInBvc3Q6dGVhbXMiLCJwb3N0OnBsYXllcnMiLCJwYXRjaDp0ZWFtcyIsInBhdGNoOnBsYXllcnMiLCJkZWxldGU6dGVhbXMiLCJkZWxldGU6cGxheWVycyIsImdldDp0ZWFtcy9pZCIsImdldDpwbGF5ZXJzL2lkIl19.lXCAUKEaSn_QWz7982EMnw6CFVFOILYZ5R7b5_b9IRgzMLta1tlee8M4D9EA2TJS5xCgB7VD7dLavo8fgFjTaYrKzTSHRZ6pIC4gaXOP1LnIh_JeZ0jSR8oAB0wXYAM57_iZvL-TP4LNdK4IBqT7pZp2ulVX2r2O7gIw9w01bMGTJsqXt6Kt6uYHiw_XlJvwyHJa1mA71_Vuwb8VLryvR5ES2g6r5j_aRhqHOB4xtPoj_bePFgVp4YBGEt_XLOmVFDllLP2E6vqglixuQgVQE8phW47XIL0GzQUBxl7U0Kj4k6VsxU-m4cil8x0gnEn4Wy_1ptA97PKDgTX3mSWrfw"
```
Alternatively, these tokens can be found in the postman collection in this repo

### Running the app
1. Make sure that you have created and are using the proper project environment. This can be done by creating a virtualenv using the code below
```bash
virtualenv -p python3.12 env
#Windows
source env/Scripts/activate
#otherwise
source env/bin/activate
```
2. Make sure that all requirements are installed using:
```bash
pip install -r requirements.txt
```
3. Configuring the database path in models.py and in test_app.py
```
database_path = 'postgresql://{}:{}@{}/{}'.format([your user], [your password], 'localhost:5432', [your database name])
```
4. Configure setup.sh if needed and run the following:
```bash
source setup.sh
```
5. Now run the flask app using:
```bash
flask run --reload
```
6. For testing, run
```bash
py test_app.py
```

## API documentation
### Models
*Team
  * name
  * players
*Player
  * name
  * height
  * position
  * team_id
    
### Endpoints
#### GET /teams
* Get all teams
* Required `get:teams` permission
* Example request: `curl 'http://localhost:5000/teams'`
* Example response:
```bash
{
    "success": true,
    "teams": [
        {
            "id": 1,
            "name": "Heat",
            "players": [
                "Lebron James"
            ]
        },
        {
            "id": 2,
            "name": "Knicks",
            "players": []
        },
        {
            "id": 3,
            "name": "Cavs",
            "players": []
        }
    ]
}
```
#### GET /players
* Get all players
* Required `get:players` permission
* Example request: `curl 'http://localhost:5000/players'`
* Example response:
```bash
{
    "players": [
        {
            "id": 1,
            "name": "Lebron James",
            "team": "Heat"
        },
        {
            "id": 3,
            "name": "Luka Doncic",
            "team": "Free Agent"
        },
        {
            "id": 4,
            "name": "Kevin Durant",
            "team": "Free Agent"
        }
    ],
    "success": true
}
```
#### GET /teams/<int:id>
* Get a team by id
* Required `get:teams/id` permission
* Example request: `curl 'http://localhost:5000/teams/1'`
* Example response:
```bash
{
    "name": "Heat",
    "players": [
        {
            "height": "6'9",
            "id": 1,
            "name": "Lebron James",
            "position": "Small Forward",
            "team": "Heat"
        },
        {
            "height": "6'4",
            "id": 5,
            "name": "Dwyane Wade",
            "position": "Shooting Guard",
            "team": "Heat"
        }
    ],
    "success": true
}
```
#### GET /players/<int:id>
* Get a player by id
* Required `get:players/id` permission
* Example request: `curl 'http://localhost:5000/players/3'`
* Example response:
```bash
{
    "player": {
        "height": "6'7",
        "id": 3,
        "name": "Luka Doncic",
        "position": "Point Guard",
        "team": "Free Agent"
    },
    "success": true
}
```
#### POST /teams
* Create a team
* Required `post:teams` permission
* Example request:
```bash
curl --request POST 'http://localhost:5000/teams' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Mavs",
		}'
```
* Example response:
```bash
{
    "success": true,
    "team": {
        "id": 5,
        "name": "Mavs",
        "players": []
    }
}
```
#### POST /players
* Create a player
* Required `post:players` permission
* Example request:
```bash
curl --request POST 'http://localhost:5000/teams' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Kobe Bryant",
      "height": "6'6",
      "position": "Shooting Guard"
		}'
```
* Example response:
```bash
{
    "player": {
        "height": "6'6",
        "id": 6,
        "name": "Kobe Bryant",
        "position": "Shooting Guard",
        "team": "Free Agent"
    },
    "success": true
}
```
#### PATCH /teams
* Update a team
* Required `patch:teams` permission
* Example request:
```bash
curl --request PATCH 'http://localhost:5000/teams/3' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"name": "Spurs",
		}'
```
* Example response:
```bash
{
    "success": true,
    "team": {
        "id": 3,
        "name": "Spurs",
        "players": []
    }
}
```
#### PATCH /players
* Update a player
* Required `patch:players` permission
* Example request:
```bash
curl --request PATCH 'http://localhost:5000/players/5' \
		--header 'Content-Type: application/json' \
		--data-raw '{
			"position": "Point Guard",
		}'
```
* Example response:
```bash
{
    "player": {
        "height": "6'4",
        "id": 5,
        "name": "Dwyane Wade",
        "position": "Shooting Guard",
        "team": "Heat"
    },
    "success": true
}
```
#### DELETE /teams/<int:id>
* Delete a team by id
* Required `delete:teams` permission
* Example request: `curl --request DELETE 'http://localhost:5000/teams/3'`
* Example response:
```bash
{
    "deleted": 3,
    "success": true
}
```
#### DELETE /players/<int:id>
* Delete a players by id
* Required `delete:players` permission
* Example request: `curl --request DELETE 'http://localhost:5000/players/3'`
* Example response:
```bash
{
    "deleted": 4,
    "success": true
}
```

### Error Handling
Handled errors are:
* 401: Unauthorized
* 403: Forbidden
* 404: Resource Not Found
* 405: Method Not Allowed
* 422: Not Processable

Errors are returned as JSON objects. The code below shows a sample 404 error.
```bash
{
    "error": 404,
    "message": "not_found",
    "success": false
}
```
