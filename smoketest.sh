#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

##########################################################
#
# Health Checks
#
##########################################################

# Function to check the health of the service
healthcheck() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
db_check() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

# Function to create a user account
create_account() {
  echo "Creating a user account..."

  UNIQUE_USERNAME="testuser_$(date +%s)"
  PASSWORD="testpass"

  RESPONSE=$(curl -s -X POST "$BASE_URL/create-account" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$UNIQUE_USERNAME\", \"password\": \"$PASSWORD\"}")
  
  echo "Response: $RESPONSE"
  
  echo "$RESPONSE" | grep -q '"message": "Account created"'
  if [ $? -eq 0 ]; then
    echo "User account created successfully for $UNIQUE_USERNAME."
    # Export these for use in other functions
    export TEST_USERNAME=$UNIQUE_USERNAME
    export TEST_PASSWORD=$PASSWORD
  else
    echo "Failed to create user account."
    exit 1
  fi
}

# Function to login with a user account
login() {
  echo "Logging in with the user account..."
  curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$TEST_USERNAME\", \"password\": \"$TEST_PASSWORD\"}" | grep -q '"message": "Login successful"'
  if [ $? -eq 0 ]; then
    echo "User logged in successfully."
  else
    echo "Failed to login."
    exit 1
  fi
}

# Function to update password
update_password() {
  echo "Updating user password..."
  curl -s -X POST "$BASE_URL/update-password" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"$TEST_USERNAME\", \"old_password\": \"$TEST_PASSWORD\", \"new_password\": \"newpass\"}" | grep -q '"message": "Password updated successfully"'
  if [ $? -eq 0 ]; then
    echo "Password updated successfully."
    export TEST_PASSWORD="newpass"  # Update the password for subsequent tests
  else
    echo "Failed to update password."
    exit 1
  fi
}

# Function to add a team to favorites
add_team_to_fav() {
  echo "Adding a team to favorites..."
  curl -s -X POST "$BASE_URL/add-to-fav" \
    -H "Content-Type: application/json" \
    -d '{"nfl_id": 1}' | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Team added to favorites."
  else
    echo "Failed to add team to favorites."
    exit 1
  fi
}

# Function to remove a team from favorites
remove_team_from_fav() {
  echo "Removing a team from favorites..."
  curl -s -X POST "$BASE_URL/remove-from-fav" \
    -H "Content-Type: application/json" \
    -d '{"nfl_id": 1}' | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Team removed from favorites."
  else
    echo "Failed to remove team from favorites."
    exit 1
  fi
}

# Function to get all favorite teams
get_favorites() {
  echo "Fetching favorite teams..."
  curl -s -X GET "$BASE_URL/get-favs" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Favorites fetched successfully."
  else
    echo "Failed to fetch favorites."
    exit 1
  fi
}

# Function to fetch all NFL teams from ESPN
get_nfl_teams() {
  echo "Fetching NFL teams from ESPN..."
  curl -s -X GET "$BASE_URL/get-teams" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "NFL teams fetched successfully."
  else
    echo "Failed to fetch NFL teams."
    exit 1
  fi
}

# Function to fetch the schedule for a specific NFL team
team_schedule() {
  echo "Fetching schedule for team with nfl_id 1..."
  curl -s -X GET "$BASE_URL/team-schedule/1" | grep -q '"events"'
  if [ $? -eq 0 ]; then
    echo "Team schedule fetched successfully."
  else
    echo "Failed to fetch team schedule."
    exit 1
  fi
}

# Function to fetch the roster for a specific NFL team
team_roster() {
  echo "Fetching roster for team with nfl_id 1..."
  curl -s -X GET "$BASE_URL/team-roster/1" | grep -q '"athletes"'
  if [ $? -eq 0 ]; then
    echo "Team roster fetched successfully."
  else
    echo "Failed to fetch team roster."
    exit 1
  fi
}


# Run smoketests
healthcheck
db_check
create_account
login
update_password
add_team_to_fav
remove_team_from_fav
get_favorites
get_nfl_teams
team_schedule
team_roster

echo "Yay! All tests passed successfully!"
