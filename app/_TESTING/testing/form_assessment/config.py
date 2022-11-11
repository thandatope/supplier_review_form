import json
import os

json_file_path = (
    r"C:\Git\Git\Work\1_FlaskSupplierReview\testing\form_assessment\config.json"
)
with open(json_file_path, "r") as j:
    conf = json.loads(j.read())

os.path(__file__)
