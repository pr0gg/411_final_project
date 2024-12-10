import pytest
from unittest.mock import patch, MagicMock
import sqlite3
from team_tracker.models.user_model import (
    User,
    generate_salt,
    hash_password,
    create_user,
    verify_user,
    update_password
)

@pytest.fixture
def user_data():
    """Fixture providing test user data."""
    return {
        'username': 'testuser',
        'password': 'testpass123',
        'salt': 'abcd1234'
    }

@pytest.fixture
def mock_db(monkeypatch):
    """Fixture providing a mock database connection."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_get_db = MagicMock()
    mock_get_db.return_value.__enter__.return_value = mock_conn
    
    monkeypatch.setattr('team_tracker.models.user_model.get_db_connection', mock_get_db)
    
    return mock_conn, mock_cursor

def test_generate_salt():
    """Test that salt generation produces expected format."""
    salt = generate_salt()
    assert len(salt) == 32  # 16 bytes = 32 hex chars
    # Verify it's a valid hex string
    assert int(salt, 16)

def test_hash_password():
    """Test password hashing is consistent."""
    # Same password + salt should produce same hash
    hash1 = hash_password("test123", "salt123")
    hash2 = hash_password("test123", "salt123")
    assert hash1 == hash2

    # Different salts should produce different hashes
    hash3 = hash_password("test123", "salt456")
    assert hash1 != hash3

def test_create_user_success(user_data, mock_db):
    """Test successful user creation."""
    mock_conn, mock_cursor = mock_db
    
    create_user(user_data['username'], user_data['password'])

    # Verify database was called correctly
    mock_cursor.execute.assert_called_once()
    args = mock_cursor.execute.call_args[0]
    assert "INSERT INTO users" in args[0]
    assert len(args[1]) == 3  # username, hash, salt

def test_create_user_duplicate(user_data, mock_db):
    """Test handling of duplicate username."""
    mock_conn, mock_cursor = mock_db
    mock_conn.cursor.side_effect = sqlite3.IntegrityError
    
    with pytest.raises(ValueError):
        create_user(user_data['username'], user_data['password'])

def test_verify_user_success(user_data, mock_db):
    """Test successful password verification."""
    mock_conn, mock_cursor = mock_db
    test_hash = hash_password(user_data['password'], user_data['salt'])
    mock_cursor.fetchone.return_value = (test_hash, user_data['salt'])

    result = verify_user(user_data['username'], user_data['password'])
    assert result is True

def test_verify_user_wrong_password(user_data, mock_db):
    """Test failed password verification."""
    mock_conn, mock_cursor = mock_db
    test_hash = hash_password(user_data['password'], user_data['salt'])
    mock_cursor.fetchone.return_value = (test_hash, user_data['salt'])

    result = verify_user(user_data['username'], "wrongpassword")
    assert result is False

def test_verify_user_nonexistent(user_data, mock_db):
    """Test verification with non-existent user."""
    mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None

    result = verify_user("nonexistent", user_data['password'])
    assert result is False

def test_update_password_success(user_data, mock_db):
    """Test successful password update."""
    mock_conn, mock_cursor = mock_db
    test_hash = hash_password(user_data['password'], user_data['salt'])
    mock_cursor.fetchone.return_value = (test_hash, user_data['salt'])

    result = update_password(
        user_data['username'],
        user_data['password'],
        "newpassword123"
    )
    assert result is True
    
    # Verify UPDATE was called
    mock_cursor.execute.assert_called_with(
        """
                UPDATE users 
                SET password_hash = ?, salt = ?
                WHERE username = ?
            """,
        pytest.approx  # We don't need to check the exact values
    )

def test_update_password_wrong_old_password(user_data, mock_db):
    """Test password update with wrong old password."""
    mock_conn, mock_cursor = mock_db
    test_hash = hash_password(user_data['password'], user_data['salt'])
    mock_cursor.fetchone.return_value = (test_hash, user_data['salt'])

    result = update_password(
        user_data['username'],
        "wrongoldpassword",
        "newpassword123"
    )
    assert result is False