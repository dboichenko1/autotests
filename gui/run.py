import json
from regression import Studilib

with open("config.json", "r") as q:
    config = json.load(q)
studilib = Studilib(config)
studilib.start()