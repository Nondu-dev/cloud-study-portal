import json
import os
import unittest
from unittest.mock import patch

os.environ["TABLE_NAME"] = "CloudStudyNotes"
os.environ["BUCKET_NAME"] = "cloud-study-portal-docs-20261011"

with patch("boto3.resource"), patch("boto3.client"):
    from backend.lambda_function import response


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


if __name__ == "__main__":
    unittest.main()
