import requests
import json
from typing import Any, Dict

CONFIG = {'url': 'http://localhost:4000/graphql/'}

def get_repo(repo_name: str = None, repo_id: str = None) -> Dict[str, Any]:
    """
    Makes a POST request to get a repo by its name or ID.

    Args:
        repo_name (str, optional): The name of the repo.
        repo_id (str, optional): The ID of the repo.

    Returns:
        Dict[str, Any]: The JSON response from the server.
    """
    url = CONFIG['url']

    if repo_name:
        query = {
            'query': f'''
            {{
                getNameSpaceRepo(repoNameOrID: "{repo_name}") {{
                    status
                    message
                    repoName
                    repoID
                    repoSignature
                }}
            }}
            '''
        }
    elif repo_id:
        query = {
            'query': f'''
            {{
                getNameSpaceRepo(repoNameOrID: "{repo_id}") {{
                    status
                    message
                    repoName
                    repoID
                    repoSignature
                }}
            }}
            '''
        }
    else:
        raise ValueError("Either repo_name or repo_id must be provided.")

    print(f"get_repo called with repo_name: {repo_name}, repo_id: {repo_id}")  # Print the input arguments

    response = requests.post(url, json=query, headers={'accept': 'json'})
    print(f"Response from GraphQL endpoint: {response.text}")  # Print the response text

    return response

def parse_get_repo_response(response):
    """
    Parses the response from the get_repo function and formats it for CLI output.

    Args:
        response (requests.Response): The response object from the get_repo request.

    Returns:
        tuple(str, str): A tuple containing the status of the repo retrieval process and a formatted string message.
    """
    print(f"parse_get_repo_response called with response status code: {response.status_code}")  # Print the response status code

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"Parsed response data: {data}")  # Print the parsed response data
            repo_data = data.get('data', {}).get('getNameSpaceRepo', {})
            status = repo_data.get('status')
            message = repo_data.get('message')
            repo_id = repo_data.get('repoID')
            repo_name = repo_data.get('repoName')
            repo_signature = repo_data.get('repoSignature')

            if status == 200:
                return ('success', f"Repo '{repo_name}' retrieved successfully.\nID: {repo_id}\nSignature: {repo_signature}")
            else:
                return (status, f"{message}")

        except json.JSONDecodeError:
            print("Error: Invalid response format. Unable to parse JSON.")  # Print the error message
            return ('error', "Invalid response format. Unable to parse JSON.")
    else:
        print(f"Error: HTTP Error: {response.status_code}. Failed to retrieve repo.")  # Print the error message
        return ('error', f"HTTP Error: {response.status_code}. Failed to retrieve repo.")
