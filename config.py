import json
import os

config = json.load(open("default.config"))
if os.path.exists("local.config"):
    local = json.load(open("local.config"))
    config.update(local)
