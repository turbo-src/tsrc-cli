import unittest
import subprocess
import json

class TestCLIApp(unittest.TestCase):

    def run_cli_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

    def test_01_create_user(self):
        command = "poetry run tsrc-cli user create --contributor-id=test_user_id --contributor-password=test_password test_user_name"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn("User 'test_user_name' with ID 'test_user_id' created successfully", stdout)

    def test_02_create_user_exists(self):
        command = "poetry run tsrc-cli user create --contributor-id=test_user_id_other --contributor-password=test_password test_user_name"
        stdout, stderr, exit_code = self.run_cli_command(command)
        #self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for contributor-id that already exists
        self.assertIn("User 'test_user_name' already exists", stderr)

    def test_03_create_id_exists(self):
        command = "poetry run tsrc-cli user create --contributor-id=test_user_id --contributor-password=test_password test_user_name_other"
        stdout, stderr, exit_code = self.run_cli_command(command)
        #self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for user already exists
        self.assertIn("User 'test_user_name' already exists", stderr)

    def test_04_get_user(self):
        # Assuming the user 'test_user_id' is already created
        command = "poetry run tsrc-cli user get test_user_id"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn("User 'test_user_name' with ID 'test_user_id' retrieved successfully", stdout)

    def test_05_get_user_non_existent(self):
        # Assuming the user 'test_user_id' is not created
        command = "poetry run tsrc-cli user get test_user_id_non_existent"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for non-existent user
        self.assertIn("User not found", stderr)

if __name__ == '__main__':
    unittest.main()
