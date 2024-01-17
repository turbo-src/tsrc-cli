
import sys
import os
import pytest
from unittest.mock import patch
import requests
# Add the parent directory of tsrc_cli to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tsrc_cli.lib.create_user import create_user

def test_create_user_success():
    # Example parameters for the test
    test_params = {
        'contributor_id': 'test_id',
        'contributor_name': 'test_name',
        'contributor_signature': 'test_signature',
        'token': 'test_token'
    }

    # Call the function
    response = create_user(**test_params)

    # Assertions
    assert response.status_code == 200
    assert 'createUser' in response.json()['data']
    assert response.json()['data']['createUser'] == {
        'message': 'User created successfully', 'status': 'success',
        'info': {
            'contributor_id': 'test_id',
            'contributor_name': 'test_name'
        }
    }


#@patch('requests.post')
#def test_create_user_failure(mock_post):
#    # Mocking a failure response
#    mock_response = requests.Response()
#    mock_response.status_code = 500
#    mock_response._content = b'{"error": "Server error"}'
#    mock_post.return_value = mock_response
#
#    # Call the function with the same test_params as above
#    response = create_user(**test_params)
#
#    # Assertions
#    assert response.status_code == 500
#    assert 'error' in response.json()
#