# Star Wars




## Use Poetry to run the project

1. Download and install anaconda
2. Create a conda environement and install the requirements with poetry

```
conda create -n starwars_env python=3.9.0
conda activate starwars_env
pip install poetry
poetry install
```

### How to run
To run the program on our own json files:

```
python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_1/empire.json"

python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_2/empire.json"

python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_3/empire.json"

python -m cli.give-me-the-odds "./config/millennium-falcon.json" "./config/example_4/empire.json"
```