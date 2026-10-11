import json
import os
import uuid
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body, default=decimal_to_number)
    }


def decimal_to_number(value):
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    raise TypeError("Value cannot be converted to JSON")


def lambda_handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("rawPath", "")

    if method == "GET" and path.endswith("/health"):
        return response(200, {
            "message": "Welcome to CloudStudy",
            "project": "CloudStudy Student Notes Portal",
            "status": "running"
        })

    if method == "GET" and path.endswith("/notes"):
        result = table.scan()
        return response(200, {"notes": result.get("Items", [])})

    if method == "POST" and path.endswith("/notes"):
        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return response(400, {"error": "Invalid JSON"})

        subject = str(body.get("subject", "")).strip()
        title = str(body.get("title", "")).strip()
        content = str(body.get("content", "")).strip()

        if not subject or not title or not content:
            return response(400, {
                "error": "Subject, title and content are required"
            })

        note = {
            "noteId": str(uuid.uuid4()),
            "subject": subject,
            "title": title,
            "content": content
        }

        table.put_item(Item=note)
        return response(201, {"note": note})

    if method == "DELETE" and "/notes/" in path:
        note_id = path.rsplit("/", 1)[-1]

        if not note_id:
            return response(400, {"error": "Note ID is required"})

        table.delete_item(Key={"noteId": note_id})
        return response(200, {"message": "Note deleted"})

    return response(404, {"error": "Route not found"})
