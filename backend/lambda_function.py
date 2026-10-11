import json
import os
import uuid
import base64
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

table = dynamodb.Table(os.environ["TABLE_NAME"])
bucket_name = os.environ["BUCKET_NAME"]


def decimal_to_number(value):
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    raise TypeError("Value cannot be converted to JSON")


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=decimal_to_number)
    }


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

    if method == "POST" and path.endswith("/documents"):
        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return response(400, {"error": "Invalid JSON"})

        file_name = os.path.basename(str(body.get("fileName", ""))).strip()
        content_type = str(body.get("contentType", "")).strip()
        file_content = body.get("fileContent", "")

        allowed_types = {
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }

        extension = os.path.splitext(file_name)[1].lower()

        if not file_name or extension not in allowed_types:
            return response(400, {
                "error": "Only PDF, TXT and DOCX files are allowed"
            })

        if content_type != allowed_types[extension]:
            return response(400, {
                "error": "File type does not match the file extension"
            })

        if not isinstance(file_content, str) or not file_content:
            return response(400, {"error": "File content is required"})

        try:
            file_bytes = base64.b64decode(file_content, validate=True)
        except (ValueError, base64.binascii.Error):
            return response(400, {"error": "Invalid file encoding"})

        if not file_bytes or len(file_bytes) > 3 * 1024 * 1024:
            return response(400, {
                "error": "File must be smaller than or equal to 3 MB"
            })

        object_key = f"study-documents/{uuid.uuid4()}-{file_name}"

        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
            ServerSideEncryption="AES256"
        )

        return response(201, {
            "message": "Document uploaded successfully",
            "fileName": file_name,
            "objectKey": object_key
        })

    return response(404, {"error": "Route not found"})
