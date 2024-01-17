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

def parse_create_user_response(response):
    """
    Parses the response from the create_user function and formats it for CLI output.

    Args:
        response (requests.Response): The response object from the create_user request.

    Returns:
        str: A formatted string with the status and message of the user creation process.
    """
    if response.status_code == 200:
        # Assuming the response is JSON and has the expected structure.
        try:
            data = response.json()
            user_data = data.get('data', {}).get('createUser', {})
            status = user_data.get('status')
            message = user_data.get('message')
            contributor_id = user_data.get('info', {}).get('contributor_id')
            contributor_name = user_data.get('info', {}).get('contributor_name')

            if status == 'success':
                return f"User '{contributor_name}' with ID '{contributor_id}' created successfully."
            else:
                return f"Failed to create user: {message}"

        except json.JSONDecodeError:
            return "Invalid response format. Unable to parse JSON."
    else:
        return f"HTTP Error: {response.status_code}. Failed to create user."