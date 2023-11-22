import copy
import sqlite3
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from src.boat import Boat
from src.empire import Empire
from src.path import Path


class OddsCounter:
    def __init__(
        self,
        boat_params: Dict[str, Any],
        empire_params: Dict[str, Any],
        routes_file_path: str,
    ) -> None:
        # initialize main class variables
        self.routes_file_path = routes_file_path
        self.boat_params = boat_params
        self.empire_params = empire_params
        self.initiate_objects()


        # get the list of all possible paths respecting the countdown
        self.all_paths = self.compute_possible_paths(
            origin=self.boat_params["departure"],
            destination=self.boat_params["arrival"],
            countdown=self.empire_params["countdown"],
            routes_file_path=self.routes_file_path
        )

        # filter very long paths
        self.possible_paths: List[Path] = [
            path
            for path in self.all_paths
            if sum([stop[1] for stop in path.get_all()]) <= self.empire.countdown
        ]

        # remove redundunt paths if there are any
        self.possible_paths = list(set(self.possible_paths))

    def initiate_objects(self) -> None:
        self.boat = Boat(autonomy=self.boat_params["autonomy"])
        self.empire = Empire(
            countdown=self.empire_params["countdown"],
            bounty_hunters=self.empire_params["bounty_hunters"],
        )

    def compute_possible_paths(
        self, origin: str, destination: str, countdown: int, routes_file_path:str
    ) -> List[Path]:
        graph: Dict[str, List[Tuple[str, int]]] = defaultdict(list)

        # Connect to the SQLite database
        conn = sqlite3.connect(routes_file_path)
        cursor = conn.cursor()

        # Query the data from the database (assuming the table is named ROUTES)
        _ = cursor.execute("SELECT * FROM ROUTES")
        rows = cursor.fetchall()

        # Populate the graph based on the database records
        for row in rows:
            src, dest, time = row
            graph[src].append((dest, time))
            graph[dest].append((src, time))  # Undirected graph

        conn.close()

        def dfs(
            current: str, path: Path, remaining_time: int, consecutive_days: int
        ) -> None:
            if current == destination and remaining_time >= 0:
                result.append(
                    copy.deepcopy(path)
                )  # Append a copy of the path to the result
                return

            # Stay in the current planet
            if remaining_time >= 0 and consecutive_days < 2:
                path.add_stop((current, 1))
                dfs(current, path, remaining_time - 1, consecutive_days + 1)
                path.pop()  # Backtrack

            for neighbor, travel_time in graph[current]:
                if (
                    neighbor not in path.get_planet_names()
                    and remaining_time - travel_time >= 0
                ):
                    path.add_stop((neighbor, travel_time))
                    dfs(neighbor, path, remaining_time - travel_time, 0)
                    path.pop()  # Backtrack

        result: List[Path] = []
        dfs(origin, Path(), countdown, 0)
        return result

    def compute_odds_for_one_path(self, path: Path) -> float:
        self.initiate_objects()
        current = self.boat_params["departure"]
        for subpath in path.get_all():
            dest, travel_time = subpath

            if dest != current:
                # if not enough autonomy, we need to refuel to recharge energy
                if self.boat.autonomy < travel_time:
                    fail = self.empire.update_countdown(1)  # recharge
                    if fail:  # the countdown finished, no need to continue
                        path.set_fail_prob(1.0)
                        return float(path.get_fail_prob())

                    # fuel the boat
                    self.boat.increase_autonomy(6 - self.boat.autonomy)

                    # update the date and the fail probability
                    path.update_date(1)
                    path.update_probability(
                        current, self.empire_params["bounty_hunters"]
                    )

            # travel
            self.boat.reduce_autonomy(travel_time)
            fail = self.empire.update_countdown(travel_time)

            if fail:  # the countdown finished, no need to continue
                path.set_fail_prob(1.0)
                return float(path.get_fail_prob())

            path.update_date(travel_time)
            path.update_probability(dest, self.empire_params["bounty_hunters"])
            current = dest
        return float(path.get_fail_prob())

    def compute_odds(self) -> float:
        probas: List[float] = []
        for path in self.possible_paths:
            fail_prob = self.compute_odds_for_one_path(path)
            probas.append(fail_prob)

        # return the highest success probability
        fail_probability = min(probas)
        success_proba = (1.0 - fail_probability) * 100
        return success_proba
