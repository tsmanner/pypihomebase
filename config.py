import copy
import json
import os


def dict_merge(target, *args):
    # Merge multiple dicts
    if len(args) > 1:
        for obj in args:
            dict_merge(target, obj)
        return target

    # Recursively merge dicts and set non-dict values
    obj = args[0]
    if not isinstance(obj, dict):
        return obj
    for k, v in obj.items():
        if k in target and isinstance(target[k], dict):
            dict_merge(target[k], v)
        else:
            target[k] = copy.deepcopy(v)


default_file = os.path.dirname(__file__) + os.sep + "default.config"
local_file = os.path.dirname(__file__) + os.sep + "local.config"

config = json.load(open(default_file))
if os.path.exists(local_file):
    local = json.load(open(local_file))
    dict_merge(config, local)
