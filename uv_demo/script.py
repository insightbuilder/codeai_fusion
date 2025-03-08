# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pandas",
#     "requests",
#     "rich",
# ]
# ///

import pandas as pd
from sys import argv
import requests
from rich.pretty import pprint

if len(argv) > 1:
    print("This is first demo", argv[:-1])


resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])


def get_add():
    print("Getting to add...")


get_add()
