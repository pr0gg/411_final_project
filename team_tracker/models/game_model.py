import logging
from typing import List

from team_tracker.models.kitchen_model import Team, update_team_stats
from team_tracker.utils.logger import configure_logger
from team_tracker.utils.random_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class GameModel:

    def __init__(self):
        self.competitors: List[Team] = []

    def battle(self) -> str:
        logger.info("Two teams enter, one team leaves!")

        if len(self.competitors) < 2:
            logger.error("Not enough competitors to play a game.")
            raise ValueError("Two competitors must be prepped for a game.")

        competitors_1 = self.competitors[0]
        competitors_2 = self.competitors[1]

        # Log the start of the battle
        logger.info("Battle started between %s and %s", competitors_1.meal, competitors_2.meal)

        # Get battle scores for both combatants
        score_1 = self.get_battle_score(competitors_1)
        score_2 = self.get_battle_score(competitors_2)

        # Log the scores for both combatants
        logger.info("Score for %s: %.3f", competitors_1.meal, score_1)
        logger.info("Score for %s: %.3f", competitors_2.meal, score_2)

        # Compute the delta and normalize between 0 and 1
        delta = abs(score_1 - score_2) / 100

        # Log the delta and normalized delta
        logger.info("Delta between scores: %.3f", delta)

        # Get random number from random.org
        random_number = get_random()

        # Log the random number
        logger.info("Random number from random.org: %.3f", random_number)

        # Determine the winner based on the normalized delta
        if delta > random_number:
            winner = competitors_1
            loser = competitors_2
        else:
            winner = competitors_2
            loser = competitors_1

        # Log the winner
        logger.info("The winner is: %s", winner.meal)

        # Update stats for both combatants
        update_team_stats(winner.id, 'win')
        update_team_stats(loser.id, 'loss')

        # Remove the losing combatant from combatants
        self.competitors.remove(loser)

        return winner.team

    def clear_competitors(self):
        logger.info("Clearing the competitors list.")
        self.competitors.clear()

    def get_battle_score(self, combatant: Team) -> float:
        difficulty_modifier = {"HIGH": 1, "MED": 2, "LOW": 3}

        # Log the calculation process
        logger.info("Calculating game score for %s: price=%.3f, cuisine=%s, difficulty=%s",
                    competitor.meal, competitor.price, competitor.cuisine, competitor.difficulty)

        # Calculate score
        score = (combatant.price * len(combatant.cuisine)) - difficulty_modifier[combatant.difficulty]

        # Log the calculated score
        logger.info("Battle score for %s: %.3f", combatant.meal, score)

        return score

    def get_competitors(self) -> List[Team]:
        logger.info("Retrieving current list of competitors.")
        return self.competitors

    def prep_competitor(self, competitors_data: Team):
        if len(self.competitors) >= 2:
            logger.error("Attempted to add competitor '%s' but competitors list is full", competitors_data.meal)
            raise ValueError("competitor list is full, cannot add more competitors.")

        # Log the addition of the combatant
        logger.info("Adding competitor '%s' to competitors list", competitors_data.meal)

        self.competitors.append(competitors_data)

        # Log the current state of combatants
        logger.info("Current competitors list: %s", [competitor.meal for competitor in self.competitors])
