import json
import os


def get_configuration():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory, 'config.json')

    with open(config_file_path, 'r') as file:
        return json.load(file)