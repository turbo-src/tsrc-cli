import unittest
import subprocess
import json

class TestCLIApp(unittest.TestCase):

    def run_cli_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

    #def test_create_user(self):
    #    command = "poetry run tsrc-cli create-user test_user_id test_user_name test_password"
    #    stdout, stderr, exit_code = self.run_cli_command(command)
    #    self.assertEqual(exit_code, 0)
    #    self.assertIn("User 'test_user_name' with ID 'test_user_id' created successfully", stdout)

    def test_get_user(self):
        # Assuming the user 'test_user_id' is already created
        command = "poetry run tsrc-cli get-user test_user_id"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn("User 'test_user_name' with ID 'test_user_id' retrieved successfully", stdout)

    def test_get_user(self):
        # Assuming the user 'test_user_id' is not created
        command = "poetry run tsrc-cli get-user test_user_id_non_existant"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn("Failed to retrieve user: User not found\n", stdout)

if __name__ == '__main__':
    unittest.main()
