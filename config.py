import copy
import json
import os
import tkinter as tk


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


class Configuration:
    def __init__(self):
        self.images = {}
        default_file = os.path.dirname(__file__) + os.sep + "default.config"
        local_file = os.path.dirname(__file__) + os.sep + "local.config"
        self.data = json.load(open(default_file))
        if os.path.exists(local_file):
            local = json.load(open(local_file))
            dict_merge(self.data, local)
        self.sanitize_config_dict(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def sanitize_config_dict(self, d):
        for k, v in d.items():
            if isinstance(v, dict):
                self.sanitize_config_dict(v)
            elif isinstance(k, str):
                if k == "image":
                    if v not in self.images:
                        self.images[v] = tk.PhotoImage(file=os.path.dirname(__file__) + os.sep + v)
                    d[k] = "master.master.settings.images['%s']" % v
