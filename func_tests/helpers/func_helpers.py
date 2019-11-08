import json

def load_json(path):
    """
    Load data from json.load_json and return to further reuse.
    :return: dictionary with keys and values from json load_json file.
    """
    with open(path) as file:
        data = json.load(file)
    return data
