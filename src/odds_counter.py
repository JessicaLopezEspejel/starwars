import sqlite3
from collections import defaultdict
from typing import Any, Dict, Tuple, List

from src.boat import Boat
from src.empire import Empire


class OddsCounter:
    def __init__(
        self, boat_params: Dict[str, Any], empire_params: Dict[str, Any]
    ) -> None:
        self.boat_params = boat_params
        self.empire_params = empire_params
        self.initiate_objects()

        # Connect to the SQLite database
        self.conn = sqlite3.connect(
            "./config/universe.db"
        )  # Replace 'your_database.db' with the actual database name
        self.cursor = self.conn.cursor()

        self.all_paths = self.compute_possible_paths(
            origin="Tatooine",
            destination="Endor",
            countdown=self.empire_params["countdown"],
        )
        self.possible_paths = [
            path
            for path in self.all_paths
            if sum([stop[1] for stop in path]) <= self.empire.countdown
        ]

        # TODO - think about using set(paths) to remove redundunt paths if there are any

    def initiate_objects(self) -> None:
        self.boat = Boat(autonomy=self.boat_params["autonomy"])
        self.empire = Empire(
            countdown=self.empire_params["countdown"],
            bounty_hunters=self.empire_params["bounty_hunters"],
        )

    def compute_possible_paths(self, origin: str, destination: str, countdown: int) -> List[List[Tuple[str, int]]]:
        graph = defaultdict(list)

        # Query the data from the database (assuming the table is named ROUTES)
        self.cursor.execute("SELECT * FROM ROUTES")
        rows = self.cursor.fetchall()

        # Populate the graph based on the database records
        for row in rows:
            src, dest, time = row
            graph[src].append((dest, time))
            graph[dest].append((src, time))  # Undirected graph

        self.conn.close()

        def dfs(current: str, path: List[Tuple[str, int]], remaining_time: int, consecutive_days: int) -> None:
            if current == destination and remaining_time >= 0:
                result.append(path[:])  # Append a copy of the path to the result
                return

            # Stay in the current planet
            if remaining_time >= 0 and consecutive_days < 2:
                path.append((current, 1))
                dfs(current, path, remaining_time - 1, consecutive_days + 1)
                path.pop()  # Backtrack

            for neighbor, travel_time in graph[current]:
                if neighbor not in path and remaining_time - travel_time >= 0:
                    path.append((neighbor, travel_time))
                    dfs(neighbor, path, remaining_time - travel_time, 0)
                    path.pop()  # Backtrack

        result: List[List[Tuple[str, int]]] = []
        dfs(origin, [], countdown, 0)
        return result

    def update_date(self, time: int) -> None:
        self.date += time

    def update_probability(self, dst: str) -> None:
        for element in self.empire.bounty_hunters:
            planet, day = element["planet"], element["day"]

            if dst == planet and self.date == day:
                self.fail_prob += (9**self.k) / (10 ** (self.k + 1))
                self.k += 1
                return

    def compute_odds_for_one_path(self, possible_path: List[Tuple[str, int]]) -> float:
        self.fail_prob = 0.0
        self.k = 0
        self.date = 0
        self.initiate_objects()
        cur = "Tatooine"
        for subpath in possible_path:
            dst, time = subpath

            if dst != cur:
                # needs to do fuel to recharge energy
                if self.boat.autonomy < time:
                    fail = self.empire.update_countdown(1)  # recharge
                    if fail:  # the countdown finished
                        self.fail_prob = 1.0
                        return self.fail_prob

                    # fuel the boat
                    self.boat.increase_autonomy(6 - self.boat.autonomy)  # is it sure?

                    self.update_date(1)
                    self.update_probability(cur)

            # travel
            self.boat.reduce_autonomy(time)
            fail = self.empire.update_countdown(time)

            if fail:
                self.fail_prob = 1.0
                return self.fail_prob

            self.update_date(time)
            self.update_probability(dst)
            cur = dst
        return self.fail_prob

    def compute_odds(self) -> float:
        probas = []
        for possible_path in self.possible_paths:
            self.fail_prob = self.compute_odds_for_one_path(possible_path)
            probas.append(self.fail_prob)

        fail_probability = min(probas)
        success_proba = (1.0 - fail_probability) * 100
        return success_proba
