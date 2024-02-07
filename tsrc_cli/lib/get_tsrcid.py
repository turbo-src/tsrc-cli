import json
import os

def get_tsrcid():
    # Path to the config file
    config_path = os.path.expanduser('~/.tsrc/config')

    try:
        # Open and read the config file
        with open(config_path, 'r') as file:
            config_data = json.load(file)

        # Retrieve the tsrcid value
        tsrcid = config_data.get('tsrcid')

        if tsrcid is None:
            raise ValueError("tsrcid not found in the config file.")

        return tsrcid

    except FileNotFoundError:
        print(f"Config file not found at {config_path}.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON from the config file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None