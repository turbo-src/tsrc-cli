import requests
import json
from typing import Any, Dict

CONFIG = {'url': 'http://localhost:4000/graphql/"'}  # Replace with your actual configuration

def create_user(contributor_id: str,
                     contributor_name: str,
                     contributor_signature: str,
                     token: str) -> Dict[str, Any]:
    """
    Makes a POST request to create a user.

    Args:
        contributor_id (str): The ID of the contributor.
        contributor_name (str): The name of the contributor.
        contributor_signature (str): The signature of the contributor.
        token (str): The authentication token.

    Returns:
        Dict[str, Any]: The JSON response from the server.
    """
    url = CONFIG['url']

    query = {
        'query': f'''
        {{
            createUser(contributor_id: "{contributor_id}", contributor_name: "{contributor_name}", contributor_signature: "{contributor_signature}", token: "{token}") {{
                status
                message
                info {{
                    contributor_id
                    contributor_name
                }}
            }}
        }}
        '''
    }

    response = requests.post(url, json=query, headers={'accept': 'json'})

    return response