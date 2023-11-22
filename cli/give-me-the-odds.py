import json
import os
import sys

from src.odds_counter import OddsCounter

assert (
    len(sys.argv) == 3
), "please provide the millennium-falcon.json and empire.json files"

boat_file_path = sys.argv[1]
empire_file_path = sys.argv[2]

assert os.path.exists(boat_file_path), "boat file doesn't exist!"
assert os.path.exists(empire_file_path), "empire file doesn't exist!"

with open(empire_file_path) as empire_file:
    empire_params = json.load(empire_file)

with open(boat_file_path) as boat_file:
    boat_params = json.load(boat_file)

routes_file_path = os.path.join(
    os.path.dirname(boat_file_path), boat_params["routes_db"]
)

odds_counter = OddsCounter(
    boat_params=boat_params,
    empire_params=empire_params,
    routes_file_path=routes_file_path,
)
success_proba = odds_counter.compute_odds()


print(f"Success probability = {success_proba:.2f}%")
