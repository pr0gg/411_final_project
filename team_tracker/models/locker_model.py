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
    city: str
    sport: str
    league: str


def create_team(team: str, city: str, sport: str, league: str) -> None:
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO teams (team, city, sport, league)
                VALUES (?, ?, ?, ?)
            """, (team, city, sport, league))
            conn.commit()

            logger.info("Team successfully added to the database: %s", team)

    except sqlite3.IntegrityError:
        logger.error("Duplicate team name: %s", team)
        raise ValueError(f"Team with name '{team}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
