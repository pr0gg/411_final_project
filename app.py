from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from team_tracker.utils.sql_utils import initialize_database
import requests

# from flask_cors import CORS

from team_tracker.models import locker_model
# from team_tracker.game_model import GameModel
from team_tracker.utils.sql_utils import check_database_connection, check_table_exists
from team_tracker.models import user_model

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
initialize_database()



# This bypasses standard security stuff we'll talk about later
# If you get errors that use words like cross origin or flight,
# uncomment this
# CORS(app)

# Initialize the BattleModel
# game_model = GameModel()

####################################################
#
# Healthchecks
#
####################################################


@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and teams table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if teams table exists...")
        check_table_exists("teams")
        app.logger.info("teams table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)
    
##########################################################
#
# User Routes
#
##########################################################


@app.route('/create-account', methods=['POST'])
def create_account():
    """Create new user account."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        user_model.create_user(username, password)
        return jsonify({'message': 'Account created'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    """Verify user login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if user_model.verify_user(username, password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/update-password', methods=['POST'])
def update_password():
    """Update user password."""
    try:
        data = request.get_json()
        username = data.get('username')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([username, old_password, new_password]):
            return make_response(jsonify({
                'error': 'Username, old password, and new password required'
            }), 400)
            
        if user_model.update_password(username, old_password, new_password):
            return make_response(jsonify({
                'message': 'Password updated successfully'
            }), 200)
        else:
            return make_response(jsonify({
                'error': 'Invalid username or password'
            }), 401)
            
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

##########################################################
#
# Teams
#
##########################################################

@app.route('/api/create-team', methods=['POST'])
def add_team() -> Response:
    """
    Route to add a new team to the database.

    Expected JSON Input:
        - team (str): The name of the team (team).
        - city (str): The home city of the team (e.g., Denver, New York).
        - sport (str): The sport the team plays (e.g., baseball, hockey).
        - league (str): The league the team belongs to (e.g., MLB, NBA).

    Returns:
        JSON response indicating the success of the combatant addition.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue adding the combatant to the database.
    """
    app.logger.info('Creating new meal')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        team = data.get('team')
        city = data.get('city')
        sport = data.get('sport')
        league = data.get('league')

        if not team or not city or not sport or not league:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        # Call the locker_model function to add the team to the database
        app.logger.info('Adding team: %s, %s, %s, %s', team, city, sport, league)
        locker_model.create_team(team, city, sport, league)

        app.logger.info("Team added: %s", team)
        return make_response(jsonify({'status': 'success', 'team': team}), 201)
    except Exception as e:
        app.logger.error("Failed to add team: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-teams', methods=['GET'])
def get_nfl_teams():
    app.logger.info("Retrieving all NFL teams from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        response = requests.get(url)
        data = response.json()
        teams = {"teams": []}
        for t in data["sports"][0]["leagues"][0]["teams"]:
            team = {"id": t["team"]["id"], "name": t["team"]["displayName"]}
            teams["teams"].append(team)
        return make_response(jsonify(teams), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve NFL teams from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
