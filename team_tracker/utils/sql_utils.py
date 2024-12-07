from contextlib import contextmanager
import logging
import os
import sqlite3

from team_tracker.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)




# load the db path from the environment with a default value
DB_PATH = os.getenv("DB_PATH", os.path.join(os.getcwd(), "data", "team_tracker.db"))

logger.info(f"Database path is: {DB_PATH}")

def initialize_database():
    """Create database tables if they don't exist."""
    try:
        # Make sure the data directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Create teams table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    team TEXT UNIQUE NOT NULL,
                    city TEXT NOT NULL,
                    sport TEXT NOT NULL,
                    league TEXT NOT NULL
                );
            """)
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                );
            """)
            
            conn.commit()
            logger.info("Database tables initialized successfully")
            
    except sqlite3.Error as e:
        logger.error("Database initialization error: %s", str(e))
        raise Exception(f"Failed to initialize database: {e}")


def check_database_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # This ensures the connection is actually active
        cursor.execute("SELECT 1;")
        conn.close()
    except sqlite3.Error as e:
        error_message = f"Database connection error: {e}"
        logger.error(error_message)
        raise Exception(error_message) from e

def check_table_exists(tablename: str):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM {tablename} LIMIT 1;")
        conn.close()
    except sqlite3.Error as e:
        error_message = f"Table check error: {e}"
        logger.error(error_message)
        raise Exception(error_message) from e

###################################################
#
# This one yields rather than returns.
# What is the type of the yielded value?
#
###################################################
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        yield conn
    except sqlite3.Error as e:
        logger.error("Database connection error: %s", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")


