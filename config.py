import json
import os

default_file = os.path.dirname(__file__) + os.sep + "default.config"
local_file = os.path.dirname(__file__) + os.sep + "local.config"

config = json.load(open(default_file))
if os.path.exists(local_file):
    local = json.load(open(local_file))
    config.update(local)
