import unittest
import subprocess
import json
import os
import re

class TestCLIApp(unittest.TestCase):
    def setUp(self):
        # Read the test-config.json file
        config_file = os.path.join(os.path.dirname(__file__), 'test-config.json')
        with open(config_file) as f:
            self.config = json.load(f)

    def run_cli_command(self, command):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Add this line to capture output as text
        )
        stdout, stderr = process.communicate()
        exit_code = process.returncode

        print("Captured stdout:")  # Add this line to print the captured stdout
        print(stdout)  # Add this line to print the captured stdout

        print("Captured stderr:")  # Add this line to print the captured stderr
        print(stderr)  # Add this line to print the captured stderr

        return stdout, stderr, exit_code

    def test_01_create_user(self):
        username = "test_user_name"
        contributor_id = self.config['creatorInfo']['address']
        contributor_mnemonic = self.config['creatorInfo']['mnemonic']

        command = f"poetry run tsrc-cli user create --contributor-mnemonic='{contributor_mnemonic}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"User '{username}' with ID '{contributor_id}' created successfully", stdout)

    def test_02_create_user_exists(self):
        username = "test_user_name"
        contributor_id = self.config['user1Info']['address']
        contributor_mnemonic = self.config['user1Info']['mnemonic']

        command = f"poetry run tsrc-cli user create --contributor-mnemonic='{contributor_mnemonic}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for contributor-id that already exists
        self.assertIn(f"User '{username}' already exists", stderr)

    def test_03_create_id_exists(self):
        username = "test_user_name_other"
        contributor_id = self.config['creatorInfo']['address']
        contributor_mnemonic = self.config['creatorInfo']['mnemonic']

        command = f"poetry run tsrc-cli user create --contributor-mnemonic='{contributor_mnemonic}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for user already exists
        self.assertIn(f"Contributor ID '{contributor_id}' already exists", stderr)

    def test_04_get_user(self):
        username = "test_user_name"
        contributor_id = self.config['creatorInfo']['address']
        command = f"poetry run tsrc-cli user get {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"User '{username}' with ID '{contributor_id}' retrieved successfully", stdout)

    def test_04_get_user_by_id(self):
        username = "test_user_name"
        contributor_id = self.config['creatorInfo']['address']
        command = f"poetry run tsrc-cli user get --contributor-id {contributor_id}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"User '{username}' with ID '{contributor_id}' retrieved successfully", stdout)

    def test_05_get_user_non_existent(self):
        command = f"poetry run tsrc-cli user get test_user_id_non_existent"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for non-existent user
        self.assertIn(f"User not found", stderr)

    def test_06_create_repo(self):
        reponame = "test_repo_name"
        contributor_id = self.config['creatorInfo']['address']
        contributor_mnemonic = self.config['creatorInfo']['mnemonic']

        command = f"poetry run tsrc-cli repo create --contributor-mnemonic='{contributor_mnemonic}' {reponame}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)

        # Extract the repoID from stdout
        match = re.search(r"Repo 'test_repo_name' with ID '(.+)' created successfully", stdout)
        if match:
            repo_id = match.group(1)
            self.assertTrue(repo_id.startswith(contributor_id), "Repo ID does not start with contributor_id")
        else:
            self.fail("Expected message not found in stdout")

    def test_07_get_repo(self):
        reponame = "test_repo_name"
        contributor_id = self.config['creatorInfo']['address']

        # Get the repo by repo name
        command = f"poetry run tsrc-cli repo get {reponame}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"Repo '{reponame}' retrieved successfully", stdout)

        # Extract the repo ID from stdout
        match = re.search(r"ID: (.+)", stdout)
        if match:
            repo_id = match.group(1)
            self.assertTrue(repo_id.startswith(contributor_id), "Repo ID does not start with contributor_id")
        else:
            self.fail("Expected message not found in stdout")

        # Get the repo by repo ID
        command = f"poetry run tsrc-cli repo get --repo-id {repo_id}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"Repo '{reponame}' retrieved successfully", stdout)

    def test_08_vote_repo(self):
        reponame = "test_repo_name"
        contributor_id = self.config['creatorInfo']['address']
        # Get the repo by repo name to retrieve the repo ID
        command = f"poetry run tsrc-cli repo get {reponame}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        # Extract the repo ID from stdout
        match = re.search(r"ID: (.+)", stdout)
        self.assertTrue(match, "Repo ID not found in stdout")
        repo_id = match.group(1)
        print(f"Captured repo_id: {repo_id}")  # Print the captured repo_id
        # Extract the app_id from the repo_id
        app_id = repo_id.split("-")[-1]
        print(f"Extracted app_id: {app_id}")  # Print the extracted app_id
        # Simulate a commit ID (replace with actual commit ID if available)
        #url = "tsrctester1/demo/pullRequest1"
        url = "tsrc"
        #commit_id = "dcdaa43d22e488b99ff1b0a86255540ce0449cd7"
        commit_id = "dcdaa"
        # Vote for the repo using the repo ID, commit ID, and app_id
        command = f"poetry run tsrc-cli repo vote {url} {commit_id} {repo_id}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        print(f"Using app_id: {app_id} in repo vote command")  # Print the app_id used in the command
        # Check the exit code and stdout for success
        self.assertEqual(exit_code, 0)
        self.assertIn("Vote submitted successfully", stdout)

if __name__ == '__main__':
    unittest.main(buffer=False)
