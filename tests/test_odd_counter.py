import unittest
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ..src.odds_counter import OddsCounter

boat_params = {
    "autonomy": 6,
    "departure": "Tatooine",
    "arrival": "Endor",
    "routes_db": "universe.db",
}

routes_file_path = "./config/universe.db"


class TestOddsCounter(unittest.TestCase):
    def test_odds_counter_example_1(self) -> None:
        empire_params = {
            "countdown": 7,
            "bounty_hunters": [
                {"planet": "Hoth", "day": 6},
                {"planet": "Hoth", "day": 7},
                {"planet": "Hoth", "day": 8},
            ],
        }

        odds_counter = OddsCounter(
            boat_params=boat_params,
            empire_params=empire_params,
            routes_file_path=routes_file_path,
        )
        success_proba = odds_counter.compute_odds()

        self.assertEqual(success_proba, 0.0)

    def test_odds_counter_example_2(self) -> None:
        empire_params = {
            "countdown": 8,
            "bounty_hunters": [
                {"planet": "Hoth", "day": 6},
                {"planet": "Hoth", "day": 7},
                {"planet": "Hoth", "day": 8},
            ],
        }

        odds_counter = OddsCounter(
            boat_params=boat_params,
            empire_params=empire_params,
            routes_file_path=routes_file_path,
        )
        success_proba = odds_counter.compute_odds()

        self.assertEqual(success_proba, 81.0)

    def test_odds_counter_example_3(self) -> None:
        empire_params = {
            "countdown": 9,
            "bounty_hunters": [
                {"planet": "Hoth", "day": 6},
                {"planet": "Hoth", "day": 7},
                {"planet": "Hoth", "day": 8},
            ],
        }

        odds_counter = OddsCounter(
            boat_params=boat_params,
            empire_params=empire_params,
            routes_file_path=routes_file_path,
        )
        success_proba = odds_counter.compute_odds()

        self.assertEqual(success_proba, 90.0)

    def test_odds_counter_example_4(self) -> None:
        empire_params = {
            "countdown": 10,
            "bounty_hunters": [
                {"planet": "Hoth", "day": 6},
                {"planet": "Hoth", "day": 7},
                {"planet": "Hoth", "day": 8},
            ],
        }

        odds_counter = OddsCounter(
            boat_params=boat_params,
            empire_params=empire_params,
            routes_file_path=routes_file_path,
        )
        success_proba = odds_counter.compute_odds()

        self.assertEqual(success_proba, 100.0)


if __name__ == "__main__":
    _ = unittest.main()
