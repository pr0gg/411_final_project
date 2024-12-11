# 411 Final Project

## High Level Description: 
An NFL team-tracking platform which allows the user to construct and manage their own set of their favorite teams. It is designed to help football fans get details about teams of interest and track teams based on a number of characteristics.

## Description of each route:


Route: /create-account
Request Type1: POST
Purpose: Creates a new user account with a username and password.
Request Body
username (string): User's chosen username
password (string): User's chosen password
Response Format Success (200):
message: "Account created successfully"
Error (400):
error: "Username already exists"
Example
Request: curl -X POST http://localhost:5001/create-account
 -H "Content-Type: application/json"
 -d '{ "username": "newuser123", "password": "securepassword" }'
Response: { "message": "Account created successfully", "status": "200" }

----------

Route: /login
Request Type POST
Purpose Verifies user credentials by checking username and password against stored hash.
Request Body
username (string): User's username
password (string): User's password
Response Format Success (200):
message: "Login successful"
Error (401):
error: "Invalid username or password"
Example
Request: curl -X POST http://localhost:5001/login
 -H "Content-Type: application/json"
 -d '{ "username": "testuser", "password": "testpass123" }'
Response: { "message": "Login successful" }

----------

Route: /update-password
Request Type POST
Purpose Updates an existing user's password after verifying their current password.
Request Body:
username (string): User's username
old_password (string): User's current password
new_password (string): User's desired new password
Response Format Success (200):
message: "Password updated successfully"
Error (401):
error: "Invalid username or password" Error (400):
error: "Username, old password, and new password required"
Example:
Request: curl -X POST http://localhost:5001/update-password
 -H "Content-Type: application/json"
 -d '{ "username": "testuser", "old_password": "testpass123", "new_password": "newpass456" }'
Response: { "message": "Password updated successfully" }

----------

Route: /api/add-to-fav
Request Type: POST
Purpose: Toggles favorite characteristic of select team to true.
Request Body:
nfl_id (int): NFL-assigned team ID
Response Format Success (200):
'status': 'success'
Error (500):
'error': <error message>
Request: curl -X POST http://localhost:5000/api/add-to-fav
 -H "Content-Type: application/json"
 -d '{ "nfl_id": "22" }'
Response: { "status": "success" }

----------

Route: /api/remove-from-fav
Request Type: POST
Purpose: Toggles favorite characteristic of select team to false.
Request Body:
nfl_id (int): NFL-assigned team ID
Response Format Success (200):
'status': 'success'
Error (500):
'error': <error message>
Request: curl -X POST http://localhost:5000/api/remove-from-fav
 -H "Content-Type: application/json"
 -d '{ "nfl_id": "22" }'
Response: { "status": "success" }

----------

Route: /api/get-favs
Request Type: GET
Purpose: Retrieves all teams marked as favorite.
Request Body:
none
Response Format Success (200):
'status': 'success', 'favorites': <favorites data>
Error (500):
'error': <error message>
Example:
Request: curl -X GET http://localhost:5000/api/get-favs
 -H "Content-Type: application/json"
Response: {"favorites": [],"status": "success"}

----------

Route: /api/get-teams
Request Type: GET
Purpose: Retrieves all NFL teams from external API and adds them to DB.
Request Body:
none
Response Format Success (200):
'status': 'success'
Error (500): 
'error': <error message>
Example: 
Request: curl -X GET http://localhost:5000/api/get-teams
 -H "Content-Type: application/json"
Response:  {"teams": [{"id": "22","name": "Arizona Cardinals"},{"id": "1","name": "Atlanta Falcons"}]}

----------

Route: /team-schedule/<int:team_id>
Request Type: GET
Purpose: Displays team game schedule based on selected NFL-assigned team ID
Request Body:
nfl_id (int): NFL-assigned team ID
Response Format Success (200): 
events data
Error (500): 
'error': <error message>
Example:
Request: curl -X GET http://localhost:5000/team-schedule/22
 -H "Content-Type: application/json"
 -d '{ "nfl_id": "22" }'
Response: {"events": [{"date": "2024-09-08T17:00Z","name": "Arizona Cardinals at Buffalo Bills","week": "Week 1"},{"date": "2024-09-15T20:05Z","name": "Los Angeles Rams at Arizona Cardinals","week": "Week 2"}]}

----------

Route: /team-roster/<int:team_id>
Request Type: GET
Purpose: Displays team roster based on selected NFL-assigned team ID
Request Body:
nfl_id (int): NFL-assigned team ID
Response Format Success (200):
roster data
Error (500):
'error': <error message>
Example:
Request: curl -X GET http://localhost:5000/team-roster/22
 -H "Content-Type: application/json"
 -d '{ "nfl_id": "22" }'
Response: {"athletes": [{"age": 24,"name": "Isaiah Adams","position": "offense"},{"age": 29,"name": "Jackson Barton","position": "offense"}]}
