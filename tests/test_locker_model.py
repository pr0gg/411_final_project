from contextlib import contextmanager
import re
import sqlite3

import pytest

from team_tracker.models.locker_model import (
    Team,
    create_team,
    add_to_favorites,
    remove_from_favorites,
    get_favorites
)

######################################################
#
#    Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("team_tracker.models.locker_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#
#    Add and delete
#
######################################################

def test_create_team(mock_cursor):
    """Test creating a new team in the list."""

    # Call the function to create a new song
    create_team(team="Patriots", nfl_id="14", loc="New England")

    expected_query = normalize_whitespace("""
        INSERT INTO teams (team, nfl_id, loc)
        VALUES (?, ?, ?)
    """)

    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])

    # Assert that the SQL query was correct
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call (second element of call_args)
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Assert that the SQL query was executed with the correct arguments
    expected_arguments = ("Patriots", "14", "New England")
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_create_team_duplicate(mock_cursor):
    """Test creating a team with a duplicate team name (should raise an error)."""

    # Simulate that the database will raise an IntegrityError due to a duplicate entry
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: teams.team")

    # Expect the function to raise a ValueError with a specific message when handling the IntegrityError
    with pytest.raises(ValueError, match="Team with name 'Patriots' already exists"):
        create_team(team="Patriots", nfl_id="14", loc="New England")

def test_add_to_favorites(mock_cursor):
    """Test adding team to favorites."""

    # Simulate that the team exists (nfl_id = 22)
    mock_cursor.fetchone.return_value = [False]

    # Call the add_to_favorites function with a sample NFL team ID
    nfl_id = 22
    add_to_favorites(nfl_id)

    # Normalize the expected SQL query
    expected_query = normalize_whitespace("""
        UPDATE teams SET favorite = TRUE WHERE nfl_id = ?
    """)

    # Ensure the SQL query was executed correctly
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])

    # Assert that the SQL query was correct
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call
    actual_arguments = mock_cursor.execute.call_args_list[0][0][1]

    # Assert that the SQL query was executed with the correct arguments (song ID)
    expected_arguments = (nfl_id,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_remove_from_favorites(mock_cursor):
    """Test removing team from favorites."""

    # Simulate that the team exists (nfl_id = 22)
    mock_cursor.fetchone.return_value = [False]

    # Call the add_to_favorites function with a sample NFL team ID
    nfl_id = 22
    remove_from_favorites(nfl_id)

    # Normalize the expected SQL query
    expected_query = normalize_whitespace("""
        UPDATE teams SET favorite = FALSE WHERE nfl_id = ?
    """)

    # Ensure the SQL query was executed correctly
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])

    # Assert that the SQL query was correct
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call
    actual_arguments = mock_cursor.execute.call_args_list[0][0][1]

    # Assert that the SQL query was executed with the correct arguments (song ID)
    expected_arguments = (nfl_id,)
    assert actual_arguments == expected_arguments, f"The SQL query arguments did not match. Expected {expected_arguments}, got {actual_arguments}."

def test_get_favorites(mock_cursor):
    """Test getting all teams marked favorite."""

    # Call the add_to_favorites function with a sample NFL team ID
    get_favorites()

    # Normalize the expected SQL query
    expected_query = normalize_whitespace("""
        SELECT id, team, nfl_id, loc FROM teams WHERE favorite = TRUE
    """)

    # Ensure the SQL query was executed correctly
    actual_query = normalize_whitespace(mock_cursor.execute.call_args_list[0][0][0])

    # Assert that the SQL query was correct
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

