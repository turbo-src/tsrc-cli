import requests
import json
from typing import Any, Dict

CONFIG = {'url': 'http://localhost:4000/graphql/'}  # Replace with your actual configuration

def get_user(contributor_id: str) -> Dict[str, Any]:
    """
    Makes a POST request to get a user.

    Args:
        contributor_id (str): The ID of the contributor.

    Returns:
        Dict[str, Any]: The JSON response from the server.
    """
    url = CONFIG['url']

    query = {
        'query': f'''
        {{
            getUser(contributor_id: "{contributor_id}") {{
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

def parse_get_user_response(response):
    """
    Parses the response from the get_user function and formats it for CLI output.

    Args:
        response (requests.Response): The response object from the get_user request.

    Returns:
        tuple(str, str): A tuple containing the status of the user retrieval process and a formatted string message.
    """
    if response.status_code == 200:
        try:
            data = response.json()
            user_data = data.get('data', {}).get('getUser', {})
            status = user_data.get('status')
            message = user_data.get('message')
            contributor_id = user_data.get('info', {}).get('contributor_id')
            contributor_name = user_data.get('info', {}).get('contributor_name')

            if status == 'success':
                return ('success', f"User '{contributor_name}' with ID '{contributor_id}' retrieved successfully.")
            else:
                return (status, f"{message}")

        except json.JSONDecodeError:
            return ('error', "Invalid response format. Unable to parse JSON.")
    else:
        return ('error', f"HTTP Error: {response.status_code}. Failed to retrieve user.")

