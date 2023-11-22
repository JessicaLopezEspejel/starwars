# Star Wars

<p align="center">
  <img width="75%" src="star_wars_git.png" alt="Star Wars challenge">
</p>

## Project Summary 

This project aims to create a web application with a backend, front-end, and command-line interface for the Millennium Falcon's mission to reach Endor and destroy the Death Star. The backend reads a JSON configuration file with information about the Falcon's autonomy, departure and arrival planets, and routes database. The front-end allows users to upload a JSON file containing information about the Empire's plans, displaying the probability of success as a percentage. The command-line interface takes input files and prints the probability of success based on the provided data, considering factors such as travel time, fuel autonomy, and the presence of bounty hunters on specific planets.

## Use Poetry to install necessary packages

1. Download and install anaconda
2. Create a conda environement and install the requirements with poetry

```
conda create -n starwars_env python=3.9.0
conda activate starwars_env
pip install poetry
poetry install
```

### How to run the Command-Line Interface (CLI)
To run the program on our own json files:

```
python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_1/empire.json"

python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_2/empire.json"

python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_3/empire.json"

python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_4/empire.json"
```


### How to run the web application
1. Open a terminal, activate the starwars_env environement, and then type:  

```
python -m http.server 8080
```

2. Open another terminal, activate the starwars_env environement, and then type: 

```
python app.py
```

3. In your browser, visit:

```
http://localhost:8000/page.html
```

4. Upload the falcon.json file 
5. Click on "Show JSON" to display and load the json file
6. Click on "Compute Odds" to display success probibility. Note that you can clear the fields by clicking on "Clear". 