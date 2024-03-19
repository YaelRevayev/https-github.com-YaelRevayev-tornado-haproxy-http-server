import unittest
from fastapi.testclient import TestClient
from http_server import app
import os

client = TestClient(app)

class TestServer(unittest.TestCase):

    def test_file_upload_and_logging(self):
        source_dir = './task_azure_output'
        files_to_send = [file for file in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, file))]
        files = []
        for file_name in files_to_send:
            file_path = os.path.join(source_dir, file_name)

            with open(file_path, 'rb') as file:
                file_data = file.read()
                files.append(('files', (file_name, file_data)))

        num_files = len(files_to_send)

        # Use assertLogs to capture logging messages
        with self.assertLogs(level='INFO') as log:
            response = client.post("/upload/", files=files)
            self.assertEqual(response.status_code, 200)

        # Assert that the expected log message is present for each file
        for index in range(num_files):
            self.assertIn("A file is created.", log.output[index])


if __name__ == '__main__':
    unittest.main()
