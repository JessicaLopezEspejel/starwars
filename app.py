import os
from typing import Dict, Union

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

from src.odds_counter import OddsCounter

app = Flask(__name__)
CORS(app)


@app.route("/api/computeOdds", methods=["POST"])
def compute_odds() -> Union[Dict[str, float], Response]:
    """
    This function is the intermediate between the frontend and backend.

    Returns:
    Union[Dict[str, float], Response]: The probability of success in a dictionary
    """

    boat_params = request.json.get("boat_params")
    empire_params = request.json.get("empire_params")
    boat_file_path = "./config/millennium-falcon.json"

    routes_file_path: str = os.path.join(
        os.path.dirname(boat_file_path), boat_params["routes_db"]
    )

    odds_counter = OddsCounter(
        boat_params=boat_params,
        empire_params=empire_params,
        routes_file_path=routes_file_path,
    )

    success_prob = odds_counter.compute_odds()

    return jsonify({"probability": success_prob})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
