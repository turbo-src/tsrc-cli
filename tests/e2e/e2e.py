import unittest
import subprocess
import json
import os

class TestCLIApp(unittest.TestCase):
    def setUp(self):
        # Read the test-config.json file
        config_file = os.path.join(os.path.dirname(__file__), 'test-config.json')
        with open(config_file) as f:
            self.config = json.load(f)

    def run_cli_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

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
        username = "test_user_name"
        contributor_id = self.config['creatorInfo']['address']
        contributor_mnemonic = self.config['creatorInfo']['mnemonic']

        command = f"poetry run tsrc-cli repo create --contributor-mnemonic='{contributor_mnemonic}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)

        print('\ncreat repo\n\n', stdout)

        self.assertIn(f"Repo '{username}' with ID '{contributor_id}' created successfully", stdout)

if __name__ == '__main__':
    unittest.main()
