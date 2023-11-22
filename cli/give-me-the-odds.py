import json
import sys

from src.odds_counter import OddsCounter

assert (
    len(sys.argv) == 3
), "please provide the empire.json and the millennium-falcon.json files"

boat_file_path = sys.argv[1]
empire_file_path = sys.argv[2]


with open(empire_file_path) as empire_file:
    empire_params = json.load(empire_file)

with open(boat_file_path) as boat_file:
    boat_params = json.load(boat_file)


odds_counter = OddsCounter(boat_params=boat_params, empire_params=empire_params)
success_proba = odds_counter.compute_odds()


print(f"Success probability = {success_proba:.2f}%")
