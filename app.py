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

@app.route('/api/add-to-fav', methods=['POST'])
def add_team_to_fav() -> Response:
    """
    Route to add a new team to favorites.

    Expected JSON Input:
        - nfl_id (int): The NFL-assigned id of the team.

    Returns:
        JSON response indicating the success of adding select team to favorites.
    Raises:
        500 error if there is an issue adding the team to favorites.
    """
    app.logger.info('Adding team to favorites')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        nfl_id = data.get('nfl_id')

        # Call the locker_model function to add the team to favorites
        app.logger.info('Adding team to favorites: %d', nfl_id)
        locker_model.add_to_favorites(nfl_id)

        app.logger.info("Team added: %d", nfl_id)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error("Failed to add team: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/remove-from-fav', methods=['POST'])
def remove_team_from_fav() -> Response:
    """
    Route to remove an existing team from favorites.

    Expected JSON Input:
        - nfl_id (int): The NFL-assigned id of the team.

    Returns:
        JSON response indicating the success of removing select team from favorites.
    Raises:
        500 error if there is an issue removing the team from favorites.
    """
    app.logger.info('Removing team from favorites')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        nfl_id = data.get('nfl_id')

        # Call the locker_model function to remove the team from favorites
        app.logger.info('Removing team from favorites: %d', nfl_id)
        locker_model.remove_from_favorites(nfl_id)

        app.logger.info("Team removed: %d", nfl_id)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error("Failed to remove team: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-favs', methods=['GET'])
def get_favorites():
    """
    Route to get all NFL teams marked as favorite.

    Expected JSON Input:
        none

    Returns:
        JSON response indicating the success of favorites retrieval.
    Raises:
        500 error if there is an issue retrieving teams marked as favorite.
    """
    app.logger.info("Retrieving all teams marked favorite")
    try:
        fav_data = locker_model.get_favorites()

        return make_response(jsonify({'status': 'success', 'favorites': fav_data}), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve favorites: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-teams', methods=['GET'])
def get_nfl_teams():
    """
    Route to add all NFL teams to the database.

    Expected JSON Input:
        none

    Returns:
        JSON response indicating the success of the addition of all teams.
    Raises:
        500 error if there is an issue retrieving NFL teams from external API.
    """
    app.logger.info("Retrieving all NFL teams from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
        response = requests.get(url)
        data = response.json()
        for t in data["sports"][0]["leagues"][0]["teams"]:
            nfl_id = t["team"]["id"]
            team = t["team"]["name"]
            loc = t["team"]["location"]
            locker_model.create_team(team, nfl_id, loc)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve NFL teams from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/team-schedule/<int:nfl_id>', methods=['GET'])
def team_schedule(nfl_id: int) -> Response:
    """
    Route to retrieve team schedule by NFL team id.

    Expected JSON Input:
        - nfl_id (int): The NFL-assigned id of the team.

    Returns:
        JSON response indicating the success of the schedule retrieval.
    Raises:
        500 error if there is an issue retrieving team schedule from external API.
    """
    app.logger.info("Retrieving the team schedule from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{nfl_id}/schedule"
        response = requests.get(url)
        data = response.json()
        events = {"events": []}
        for e in data["events"]:
            event = {"week": e["week"]["text"], "date": e["date"], "name": e["name"]}
            events["events"].append(event)
        return make_response(jsonify(events), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve the team schedule from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/team-roster/<int:nfl_id>', methods=['GET'])
def team_roster(nfl_id: int) -> Response:
    """
    Route to retrieve team roster by NFL team id.

    Expected JSON Input:
        - nfl_id (int): The NFL-assigned id of the team.

    Returns:
        JSON response indicating the success of the roster retrieval.
    Raises:
        500 error if there is an issue retrieving team roster from external API.
    """
    app.logger.info("Retrieving the team roster from ESPN")
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{nfl_id}/roster"
        response = requests.get(url)
        data = response.json()
        roster = {"athletes": []}
        for p in data["athletes"]:
            for a in p["items"]:
                athlete = {"name": a["displayName"], "age": a["age"], "position": p["position"]}
                roster["athletes"].append(athlete)
        return make_response(jsonify(roster), 200)
    except Exception as e:
        app.logger.error("Failed to retrieve the team roster from ESPN: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
