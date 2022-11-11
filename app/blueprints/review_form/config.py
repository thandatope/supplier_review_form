import json
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

json_file_path = os.path.join(THIS_FOLDER, "config.json")
with open(json_file_path, "r") as j:
    conf = json.loads(j.read())
