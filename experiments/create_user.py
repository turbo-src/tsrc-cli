import requests
import json
from typing import Any, Dict

CONFIG = {'url': 'http://localhost:4000/graphql/"'}  # Replace with your actual configuration

def create_user(owner: str,
                     repo: str,
                     contributor_id: str,
                     contributor_name: str,
                     contributor_signature: str,
                     token: str) -> Dict[str, Any]:
    """
    Makes a POST request to create a user.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        contributor_id (str): The ID of the contributor.
        contributor_name (str): The name of the contributor.
        contributor_signature (str): The signature of the contributor.
        token (str): The authentication token.

    Returns:
        Dict[str, Any]: The JSON response from the server.
    """
    url = CONFIG['url']
    query = {
        'query': f'{{ createUser(owner: "{owner}", repo: "{repo}", contributor_id: "{contributor_id}", contributor_name: "{contributor_name}", contributor_signature: "{contributor_signature}", token: "{token}") }}'
    }
    response = requests.post(url, json=query, headers={'accept': 'json'})

    print('status code', response.status_code)
    print('text', response.text)
    response_json_text = json.loads(response.text)
    print('text json', response_json_text)
    print('example field access', response_json_text['data']['createUser'])
    return response

    #response_json = json.loads(response)

    return response_json
    # Check if response is JSON and return it
    #if response.headers.get('Content-Type') == 'application/json':
    #    return response.json()
    #else:
    #return response.text.data.createUser
    #return response.text
    #return {'error': 'Non-JSON response', 'status_code': response.status_code, 'response': response.text}

# Add the main function
def main():
    # Example parameters - replace these with actual values
    owner = ""
    repo = ""
    contributor_id = "example"
    contributor_name = "example"
    contributor_signature = "example",
    token = "example"

    # Call the function
    response = create_user(owner, repo, contributor_id, contributor_name, contributor_signature, token)
    # Print the response
    print(response)

if __name__ == "__main__":
    main()