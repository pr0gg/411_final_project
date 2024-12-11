# 411 Final Project


## High Level Description: 
An NFL team-tracking platform which allows the user to construct and manage their own set of their favorite teams. It is designed to help football fans get details about teams of interest and track teams based on a number of characteristics.

# API Documentation

### Create Account
**Route:** `/create-account`  
**Request Type:** POST  
**Purpose:** Creates a new user account with a username and password.

**Request Body:**
- `username` (string): User's chosen username
- `password` (string): User's chosen password

**Response Format:**  
Success (200):
```json
{
    "message": "Account created successfully"
}
```

Error (400):
```json
{
    "error": "Username already exists"
}
```

**Example:**
```bash
curl -X POST http://localhost:5001/create-account \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser123",
    "password": "securepassword"
  }'
```

### Login
**Route:** `/login`  
**Request Type:** POST  
**Purpose:** Verifies user credentials by checking username and password against stored hash.

**Request Body:**
- `username` (string): User's username
- `password` (string): User's password

**Response Format:**  
Success (200):
```json
{
    "message": "Login successful"
}
```

Error (401):
```json
{
    "error": "Invalid username or password"
}
```

**Example:**
```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Update Password
**Route:** `/update-password`  
**Request Type:** POST  
**Purpose:** Updates an existing user's password after verifying their current password.

**Request Body:**
- `username` (string): User's username
- `old_password` (string): User's current password
- `new_password` (string): User's desired new password

**Response Format:**  
Success (200):
```json
{
    "message": "Password updated successfully"
}
```

Error (401):
```json
{
    "error": "Invalid username or password"
}
```

Error (400):
```json
{
    "error": "Username, old password, and new password required"
}
```

**Example:**
```bash
curl -X POST http://localhost:5001/update-password \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "old_password": "testpass123",
    "new_password": "newpass456"
  }'
```

## Team Management Routes

### Add to Favorites
**Route:** `/api/add-to-fav`  
**Request Type:** POST  
**Purpose:** Toggles favorite characteristic of select team to true.

**Request Body:**
- `nfl_id` (int): NFL-assigned team ID

**Response Format:**  
Success (200):
```json
{
    "status": "success"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/add-to-fav \
  -H "Content-Type: application/json" \
  -d '{
    "nfl_id": "22"
  }'
```

### Remove from Favorites
**Route:** `/api/remove-from-fav`  
**Request Type:** POST  
**Purpose:** Toggles favorite characteristic of select team to false.

**Request Body:**
- `nfl_id` (int): NFL-assigned team ID

**Response Format:**  
Success (200):
```json
{
    "status": "success"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/remove-from-fav \
  -H "Content-Type: application/json" \
  -d '{
    "nfl_id": "22"
  }'
```

### Get Favorites
**Route:** `/api/get-favs`  
**Request Type:** GET  
**Purpose:** Retrieves all teams marked as favorite.

**Request Body:** None

**Response Format:**  
Success (200):
```json
{
    "status": "success",
    "favorites": []
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/get-favs \
  -H "Content-Type: application/json"
```

### Get Teams
**Route:** `/api/get-teams`  
**Request Type:** GET  
**Purpose:** Retrieves all NFL teams from external API and adds them to DB.

**Request Body:** None

**Response Format:**  
Success (200):
```json
{
    "teams": [
        {
            "id": "22",
            "name": "Arizona Cardinals"
        },
        {
            "id": "1",
            "name": "Atlanta Falcons"
        }
    ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/api/get-teams \
  -H "Content-Type: application/json"
```

### Get Team Schedule
**Route:** `/team-schedule/<int:team_id>`  
**Request Type:** GET  
**Purpose:** Displays team game schedule based on selected NFL-assigned team ID

**Request Body:**
- `nfl_id` (int): NFL-assigned team ID

**Response Format:**  
Success (200):
```json
{
    "events": [
        {
            "date": "2024-09-08T17:00Z",
            "name": "Arizona Cardinals at Buffalo Bills",
            "week": "Week 1"
        },
        {
            "date": "2024-09-15T20:05Z",
            "name": "Los Angeles Rams at Arizona Cardinals",
            "week": "Week 2"
        }
    ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/team-schedule/22 \
  -H "Content-Type: application/json"
```

### Get Team Roster
**Route:** `/team-roster/<int:team_id>`  
**Request Type:** GET  
**Purpose:** Displays team roster based on selected NFL-assigned team ID

**Request Body:**
- `nfl_id` (int): NFL-assigned team ID

**Response Format:**  
Success (200):
```json
{
    "athletes": [
        {
            "age": 24,
            "name": "Isaiah Adams",
            "position": "offense"
        },
        {
            "age": 29,
            "name": "Jackson Barton",
            "position": "offense"
        }
    ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/team-roster/22 \
  -H "Content-Type: application/json"
```
