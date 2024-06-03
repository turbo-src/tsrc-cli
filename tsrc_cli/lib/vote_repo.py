import requests
import json
from typing import Any, Dict

CONFIG = {'url': 'http://localhost:4000/graphql/'}  # Corrected URL

def vote_repo(url: str, commit_id: str) -> Dict[str, Any]:
    """
    Makes a POST request to vote for a repo by its URL and commit ID.

    Args:
        url (str): The URL of the repo.
        commit_id (str): The commit ID of the repo.

    Returns:
        Dict[str, Any]: The JSON response from the server.
    """
    endpoint = CONFIG['url']

    query = {
        'query': f'''
        {{
            setVote(
                owner: "test_user_name",
                repo: "test_user_name/test_repo_name",
                defaultHash: "{commit_id}",
                childDefaultHash: "{commit_id}",
                mergeable: true,
                contributor_id: "contributor_id_placeholder",
                side: "side_placeholder",
                token: "token_placeholder"
            )
        }}
        '''
    }

    print(f"vote_repo called with url: {url}, commit_id: {commit_id}")  # Print the input arguments

    response = requests.post(endpoint, json=query, headers={'accept': 'json'})
    print(f"Response from GraphQL endpoint: {response.text}")  # Print the response text

    return response

def parse_vote_repo_response(response):
    """
    Parses the response from the vote_repo function and formats it for CLI output.

    Args:
        response (requests.Response): The response object from the vote_repo request.

    Returns:
        tuple(str, str): A tuple containing the status of the vote process and a formatted string message.
    """
    print(f"parse_vote_repo_response called with response status code: {response.status_code}")  # Print the response status code

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Parsed response data: {data}")  # Print the parsed response data
            vote_result = data.get('data', {}).get('setVote')

            if vote_result:
                return ('success', f"Vote submitted successfully.")
            else:
                return ('error', "Failed to submit vote.")

        except json.JSONDecodeError:
            print("Error: Invalid response format. Unable to parse JSON.")  # Print the error message
            return ('error', "Invalid response format. Unable to parse JSON.")
    else:
        print(f"Error: HTTP Error: {response.status_code}. Failed to submit vote.")  # Print the error message
        return ('error', f"HTTP Error: {response.status_code}. Failed to submit vote.")
