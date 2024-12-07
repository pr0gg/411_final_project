from dataclasses import dataclass   
import hashlib   #to get hash for password
import sqlite3  
import os           #this will let us get random salts from OS (encryption data)
import logging
from typing import Any

from team_tracker.utils.sql_utils import get_db_connection
from team_tracker.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    salt: str

def generate_salt() -> str:
    """Generate a random string for password security."""
    return os.urandom(16).hex()

def hash_password(password: str, salt: str) -> str:
    """Convert password + salt into encrypted string."""
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

def create_user(username: str, password: str) -> None:
    """Create a new user in the database."""
    try:
        # Create salt and hash password
        salt = generate_salt()
        password_hash = hash_password(password, salt)
        
        # Save to database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password_hash, salt)
                VALUES (?, ?, ?)
            """, (username, password_hash, salt))
            conn.commit()
            
            logger.info("User created: %s", username)
            
    except sqlite3.IntegrityError:
        logger.error("Username already exists: %s", username)
        raise ValueError(f"Username '{username}' already exists")

def verify_user(username: str, password: str) -> bool:
    """Check if login credentials are correct."""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash, salt FROM users
                WHERE username = ?
            """, (username,))
            result = cursor.fetchone()
            
            if not result:
                return False
                
            stored_hash, salt = result
            test_hash = hash_password(password, salt)
            return test_hash == stored_hash
            
    except Exception as e:
        logger.error("Login error: %s", str(e))
        return False
    
def update_password(username: str, old_password: str, new_password: str) -> bool:
    """Update a user's password."""
    try:
        # First verify the old password
        if not verify_user(username, old_password):
            return False
            
        # Generate new salt and hash for the new password
        salt = generate_salt()
        new_hash = hash_password(new_password, salt)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET password_hash = ?, salt = ?
                WHERE username = ?
            """, (new_hash, salt, username))
            conn.commit()
            
            logger.info("Password updated for user: %s", username)
            return True
            
    except sqlite3.Error as e:
        logger.error("Database error during password update: %s", str(e))
        return False
    

    
