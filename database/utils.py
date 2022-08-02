import json
import os
import sys
path = os.path.abspath('.')
sys.path.insert(1, path)


def read_json(filename, encoding="utf-8"):
    with open(filename, encoding=encoding) as f:
        return json.load(f)
