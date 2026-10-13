
import json
import os
import unittest
from unittest.mock import patch

os.environ["TABLE_NAME"] = "CloudStudyNotes"
os.environ["BUCKET_NAME"] = "cloud-study-portal-docs-20261011"

with patch("boto3.resource"), patch("boto3.client"):
    from backend.lambda_function import lambda_handler, response


class LambdaResponseTests(unittest.TestCase):

    def test_response_returns_status_code(self):
        result = response(200, {"message": "OK"})
        self.assertEqual(result["statusCode"], 200)

    def test_response_has_json_content_type(self):
        result = response(200, {"message": "OK"})
        self.assertEqual(
            result["headers"]["Content-Type"],
            "application/json"
        )

    def test_response_body_is_valid_json(self):
        result = response(201, {"message": "Created"})
        body = json.loads(result["body"])
        self.assertEqual(body["message"], "Created")


class LambdaHealthTests(unittest.TestCase):

    def test_health_endpoint_returns_status_200(self):
        event = {
            "requestContext": {
                "http": {"method": "GET"}
            },
            "rawPath": "/health"
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 200)

    def test_health_endpoint_returns_project_information(self):
        event = {
            "requestContext": {
                "http": {"method": "GET"}
            },
            "rawPath": "/health"
        }

        result = lambda_handler(event, None)
        body = json.loads(result["body"])

        self.assertEqual(body["message"], "Welcome to CloudStudy")
        self.assertEqual(
            body["project"],
            "CloudStudy Student Notes Portal"
        )
        self.assertEqual(body["status"], "running")


class LambdaNotesTests(unittest.TestCase):

    @patch("backend.lambda_function.table")
    def test_get_notes_returns_status_200(self, mock_table):
        mock_table.scan.return_value = {"Items": []}

        event = {
            "requestContext": {
                "http": {"method": "GET"}
            },
            "rawPath": "/notes"
        }

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 200)
        mock_table.scan.assert_called_once()

    @patch("backend.lambda_function.table")
    def test_get_notes_returns_saved_notes(self, mock_table):
        saved_notes = [
            {
                "noteId": "test-note-1",
                "subject": "Cloud Computing",
                "title": "Amazon DynamoDB",
                "content": "DynamoDB is a NoSQL database."
            }
        ]

        mock_table.scan.return_value = {"Items": saved_notes}

        event = {
            "requestContext": {
                "http": {"method": "GET"}
            },
            "rawPath": "/notes"
        }

        result = lambda_handler(event, None)
        body = json.loads(result["body"])

        self.assertEqual(body["notes"], saved_notes)


if __name__ == "__main__":
    unittest.main()
