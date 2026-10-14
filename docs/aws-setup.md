# CloudStudy AWS Setup

## 1. Overview

CloudStudy uses AWS services to manage student notes and store uploaded study documents. This document records the main AWS resources and configuration used by the project.

## 2. AWS Region

- Region: Europe (Stockholm)
- Region code: `eu-north-1`

## 3. AWS Lambda

- Function name: `CloudStudyNotesFunction`
- Runtime: Python 3.14
- Execution role: `CloudStudyLambdaRole`

The Lambda function processes API requests, manages notes in DynamoDB, and uploads documents to S3.

## 4. Amazon API Gateway

- API name: `CloudStudyApi`
- API type: HTTP API
- Stage: `$default`
- Automatic deployment: Enabled

### Invoke URL

https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com

### API Routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | Checks whether the backend is running. |
| GET | `/notes` | Retrieves saved notes. |
| POST | `/notes` | Creates a note. |
| DELETE | `/notes/{noteId}` | Deletes a note. |
| POST | `/documents` | Uploads a document. |

### Health Check

Open the following URL in a browser:

https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com/health

Expected response:

```json
{
  "message": "Welcome to CloudStudy",
  "project": "CloudStudy Student Notes Portal",
  "status": "running"
}
```

## 5. Amazon DynamoDB

- Table name: `CloudStudyNotes`

DynamoDB stores student notes so that they remain available after the website is refreshed.

The Lambda function has permissions to retrieve, create, and delete notes in this table.

## 6. Amazon S3

- Bucket name: `cloud-study-portal-docs-20261011`
- Document prefix: `study-documents/`
- Public access: Blocked
- Server-side encryption: SSE-S3

Uploaded PDF, TXT, and DOCX documents are stored under the `study-documents/` prefix in the private bucket.

The Lambda execution role has permission to upload objects to this prefix.

## 7. Lambda Environment Variables

| Variable | Value |
|---|---|
| `TABLE_NAME` | `CloudStudyNotes` |
| `BUCKET_NAME` | `cloud-study-portal-docs-20261011` |

## 8. IAM Permissions

The Lambda function uses the dedicated execution role `CloudStudyLambdaRole`.

The role provides:

- CloudWatch Logs permissions for Lambda logging.
- Access to the `CloudStudyNotes` DynamoDB table for the required note operations.
- Permission to upload documents to the S3 `study-documents/` prefix.

The role was tested after being assigned to the Lambda function. The health check worked, notes persisted after refreshing the website, and document uploads succeeded.

## 9. CORS Configuration

The API allows browser requests from the local development origin:

`http://127.0.0.1:5500`

Configured methods include GET, POST, and DELETE. The allowed request header includes `content-type`.

If the frontend is hosted at a different address, the permitted origin must be updated to match it.

## 10. Testing Notes

The API health check was tested successfully. Note creation and persistence after refreshing the website were verified. Document uploads were also tested, and uploaded objects were confirmed in the S3 `study-documents/` prefix.

For the automated backend unit tests, see the `tests/` directory in the project repository.