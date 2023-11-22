from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from typing import Union, Dict
from src.odds_counter import OddsCounter

app = Flask(__name__)
CORS(app)


@app.route("/api/computeOdds", methods=["POST"])
def compute_odds() ->  Union[Dict[str, float], Response]:
    boat_params = request.json.get("boat_params")
    empire_params = request.json.get("empire_params")

    odds_counter = OddsCounter(boat_params=boat_params, empire_params=empire_params)
    success_prob = odds_counter.compute_odds()

    return jsonify({"probability": success_prob})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
