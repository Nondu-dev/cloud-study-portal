
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


class LambdaCreateNoteTests(unittest.TestCase):

    def setUp(self):
        self.note_data = {
            "subject": "Cloud Computing",
            "title": "DynamoDB",
            "content": "DynamoDB stores data as items."
        }

    def make_event(self, note_data):
        return {
            "requestContext": {
                "http": {"method": "POST"}
            },
            "rawPath": "/notes",
            "body": json.dumps(note_data)
        }

    @patch("backend.lambda_function.table")
    def test_create_note_returns_status_201(self, mock_table):
        event = self.make_event(self.note_data)

        result = lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 201)

    @patch("backend.lambda_function.table")
    def test_create_note_saves_note_to_database(self, mock_table):
        event = self.make_event(self.note_data)

        result = lambda_handler(event, None)
        body = json.loads(result["body"])
        note = body["note"]

        mock_table.put_item.assert_called_once_with(Item=note)

        self.assertEqual(note["subject"], "Cloud Computing")
        self.assertEqual(note["title"], "DynamoDB")
        self.assertEqual(
            note["content"],
            "DynamoDB stores data as items."
        )

    @patch("backend.lambda_function.table")
    def test_create_note_generates_unique_id(self, mock_table):
        event = self.make_event(self.note_data)

        first_result = lambda_handler(event, None)
        second_result = lambda_handler(event, None)

        first_note = json.loads(first_result["body"])["note"]
        second_note = json.loads(second_result["body"])["note"]

        self.assertTrue(first_note["noteId"])
        self.assertNotEqual(
            first_note["noteId"],
            second_note["noteId"]
        )

    @patch("backend.lambda_function.table")
    def test_create_note_rejects_missing_subject(self, mock_table):
        note_data = {
            "title": "DynamoDB",
            "content": "Database notes"
        }

        result = lambda_handler(self.make_event(note_data), None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertIn("required", body["error"])
        mock_table.put_item.assert_not_called()

    @patch("backend.lambda_function.table")
    def test_create_note_rejects_missing_title(self, mock_table):
        note_data = {
            "subject": "Cloud Computing",
            "content": "Database notes"
        }

        result = lambda_handler(self.make_event(note_data), None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertIn("required", body["error"])
        mock_table.put_item.assert_not_called()

    @patch("backend.lambda_function.table")
    def test_create_note_rejects_missing_content(self, mock_table):
        note_data = {
            "subject": "Cloud Computing",
            "title": "DynamoDB"
        }

        result = lambda_handler(self.make_event(note_data), None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertIn("required", body["error"])
        mock_table.put_item.assert_not_called()

    @patch("backend.lambda_function.table")
    def test_create_note_rejects_invalid_json(self, mock_table):
        event = {
            "requestContext": {
                "http": {"method": "POST"}
            },
            "rawPath": "/notes",
            "body": '{"subject": "Cloud Computing",'
        }

        result = lambda_handler(event, None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(body["error"], "Invalid JSON")
        mock_table.put_item.assert_not_called()

class LambdaDocumentUploadTests(unittest.TestCase):

    def make_event(self, file_name, content_type, file_content):
        return {
            "requestContext": {
                "http": {"method": "POST"}
            },
            "rawPath": "/documents",
            "body": json.dumps({
                "fileName": file_name,
                "contentType": content_type,
                "fileContent": file_content
            })
        }

    @patch("backend.lambda_function.s3")
    def test_upload_rejects_unsupported_file_type(self, mock_s3):
        event = self.make_event(
            "image.jpg",
            "image/jpeg",
            "aGVsbG8="
        )

        result = lambda_handler(event, None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(
            body["error"],
            "Only PDF, TXT and DOCX files are allowed"
        )
        mock_s3.put_object.assert_not_called()

    @patch("backend.lambda_function.s3")
    def test_upload_rejects_mismatched_content_type(self, mock_s3):
        event = self.make_event(
            "notes.txt",
            "application/pdf",
            "aGVsbG8="
        )

        result = lambda_handler(event, None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(
            body["error"],
            "File type does not match the file extension"
        )
        mock_s3.put_object.assert_not_called()

    @patch("backend.lambda_function.s3")
    def test_upload_rejects_missing_file_content(self, mock_s3):
        event = self.make_event(
            "notes.txt",
            "text/plain",
            ""
        )

        result = lambda_handler(event, None)
        body = json.loads(result["body"])

        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(
            body["error"],
            "File content is required"
        )
        mock_s3.put_object.assert_not_called()



if __name__ == "__main__":
    unittest.main()
