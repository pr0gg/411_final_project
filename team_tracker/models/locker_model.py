from dataclasses import dataclass
import logging
import os
import sqlite3
from typing import Any

from team_tracker.utils.sql_utils import get_db_connection
from team_tracker.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class Team:
    id: int
    team: str
    nfl_id: int
    loc: str


def create_team(team: str, nfl_id: int, loc: str) -> None:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teams (team, nfl_id, loc)
                VALUES (?, ?, ?)
            """, (team, nfl_id, loc))
            conn.commit()

            logger.info("Team successfully added to the database: %s", team)

    except sqlite3.IntegrityError:
        logger.error("Duplicate team name: %s", team)
        raise ValueError(f"Team with name '{team}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def add_to_favorites(nfl_id: int) -> None:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE teams SET favorite = TRUE WHERE nfl_id = ?", (nfl_id,))
            conn.commit()

            logger.info("Team successfully added to favorites.")
    
    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
    
def remove_from_favorites(nfl_id: int) -> None:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE teams SET favorite = FALSE WHERE nfl_id = ?", (nfl_id,))
            conn.commit()

            logger.info("Team successfully removed from favorites.")
    
    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
    
def get_favorites() -> None:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, team, nfl_id, loc FROM teams WHERE favorite = TRUE")
            rows = cursor.fetchall()

            favorites = []
            for row in rows:
                fav = {
                    'id': row[0],
                    'team': row[1],
                    'nfl_id': row[2],
                    'loc': row[3]
                }
                favorites.append(fav)

            logger.info("Favorites retrieved successfully")
            return favorites

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e