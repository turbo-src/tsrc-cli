import unittest
import subprocess
import json

class TestCLIApp(unittest.TestCase):

    def run_cli_command(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

    def test_01_create_user(self):
        # contributor-password: algo mnemonic
        username = "test_user_name"
        contributor_id = "VAX6M7SZY65NXSMAFRNUYHDAZK3326IUPZFKO63QZAAMIPVAK7ECTS2F4M"
        contributor_password = "twin pumpkin plastic stage fortune shallow melt betray ribbon receive claim enrich price exile absent avoid woman toilet print settle shiver inform rookie absorb unaware"

        command = f"poetry run tsrc-cli user create --contributor-id={contributor_id} --contributor-password='{contributor_password}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"User '{username}' with ID '{contributor_id}' created successfully", stdout)

    def test_02_create_user_exists(self):
        username = "test_user_name"
        #contributor_id = "ELNJI3EFJYG5T7L3FXZEWAPUVUE24UUXKOUQALZQWXYUCWUM5J4DHLNU2A"
        contributor_id = "XNDK5BBUOCENNRQ3FT4SQSCENFBNSY3BMOU3W2EZGNLH7ZD5ZSANKIRJZM"
        contributor_password = "brain rough jazz defy absent ability jeans much hire retire metal tragic fury culture stem beach farm upset relief stove sound comic bunker able exist"

        command = f"poetry run tsrc-cli user create --contributor-id={contributor_id} --contributor-password='{contributor_password}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for contributor-id that already exists
        self.assertIn(f"User '{username}' already exists", stderr)

    def test_03_create_id_exists(self):
        username = "test_user_name_other"
        contributor_id = "VAX6M7SZY65NXSMAFRNUYHDAZK3326IUPZFKO63QZAAMIPVAK7ECTS2F4M"
        contributor_password = "twin pumpkin plastic stage fortune shallow melt betray ribbon receive claim enrich price exile absent avoid woman toilet print settle shiver inform rookie absorb unaware"

        command = f"poetry run tsrc-cli user create --contributor-id={contributor_id} --contributor-password='{contributor_password}' {username}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for user already exists
        self.assertIn(f"Contributor ID '{contributor_id}' already exists", stderr)

    # contributor-id: algo account
    def test_04_get_user(self):
        # Assuming the user 'test_user_id' is already created
        username = "test_user_name"
        contributor_id = "VAX6M7SZY65NXSMAFRNUYHDAZK3326IUPZFKO63QZAAMIPVAK7ECTS2F4M"
        command = f"poetry run tsrc-cli user get {contributor_id}"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertEqual(exit_code, 0)
        self.assertIn(f"User '{username}' with ID '{contributor_id}' retrieved successfully", stdout)

    def test_05_get_user_non_existent(self):
        # Assuming the user 'test_user_id' is not created
        command = f"poetry run tsrc-cli user get test_user_id_non_existent"
        stdout, stderr, exit_code = self.run_cli_command(command)
        self.assertNotEqual(exit_code, 0)  # Expecting a non-zero exit code for non-existent user
        self.assertIn(f"User not found", stderr)

if __name__ == '__main__':
    unittest.main()
