# CloudStudy — Student Notes and Document Portal

## 1. Project Overview

CloudStudy is a cloud-based student notes and document portal developed as a Cloud Computing project. It allows students to create, view, and delete study notes and upload study documents through a simple web interface.

The project demonstrates how AWS cloud services can work together to provide a backend API, persistent data storage, private document storage, access control, and monitoring.

## 2. Project Objectives

- Build a simple web application for managing study notes.
- Use AWS Lambda to process backend requests.
- Use Amazon API Gateway to expose HTTP endpoints.
- Use Amazon DynamoDB to store notes persistently.
- Use Amazon S3 to store uploaded documents privately.
- Apply IAM permissions to control access to AWS resources.
- Use Amazon CloudWatch for Lambda logging and monitoring.

## 3. Main Features

- Create and view study notes.
- Delete study notes.
- Keep notes saved in DynamoDB after refreshing the website.
- Upload PDF, TXT, and DOCX documents.
- Validate document file types and file sizes.
- Store uploaded documents in a private S3 bucket.
- Process requests through an HTTP API.
- Display a health-check response to confirm that the backend is running.

## 4. AWS Services Used

| AWS service | Purpose |
|---|---|
| AWS Lambda | Runs the Python backend and processes requests. |
| Amazon API Gateway | Provides HTTP endpoints for the application. |
| Amazon DynamoDB | Stores study notes. |
| Amazon S3 | Stores uploaded study documents privately. |
| AWS IAM | Controls permissions for the Lambda function. |
| Amazon CloudWatch | Stores Lambda execution logs and supports monitoring. |

## 5. System Architecture

The application uses a web frontend connected to a serverless AWS backend.

1. The student interacts with the CloudStudy website.
2. JavaScript sends HTTP requests to Amazon API Gateway.
3. API Gateway invokes the AWS Lambda function.
4. Lambda reads, creates, or deletes notes in DynamoDB.
5. Lambda uploads accepted documents to Amazon S3.
6. CloudWatch receives the Lambda execution logs.

### Architecture flow

```
Student
   |
   v
CloudStudy Web Interface
   |
   v
Amazon API Gateway
   |
   v
AWS Lambda
   |                 |
   v                 v
DynamoDB          Amazon S3
(Study Notes)     (Documents)
   |
   v
CloudWatch Logs
```

CloudWatch receives logs from Lambda independently of the note and document storage workflows.

## 6. Technologies Used

- HTML
- CSS
- JavaScript
- Python
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- Amazon S3
- AWS IAM
- Amazon CloudWatch
- Python `unittest` for automated backend testing

## 7. API Endpoints

The application uses the following HTTP API routes.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Checks whether the backend is running. |
| GET | `/notes` | Retrieves saved notes. |
| POST | `/notes` | Creates a new note. |
| DELETE | `/notes/{noteId}` | Deletes a note using its ID. |
| POST | `/documents` | Uploads a document to S3. |

### Health Check

The health endpoint is available at:

`https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com/health`

A successful response confirms that the backend is running.

Example response:

```json
{
  "message": "Welcome to CloudStudy",
  "project": "CloudStudy Student Notes Portal",
  "status": "running"
}
```

## 8. AWS Configuration

The project was configured in the AWS Europe (Stockholm) region (`eu-north-1`).

### AWS Lambda

- Function name: `CloudStudyNotesFunction`
- Runtime: Python 3.14
- Execution role: `CloudStudyLambdaRole`

Lambda processes API requests, validates input, manages study notes, and handles document uploads.

### Amazon API Gateway

- API name: `CloudStudyApi`
- API type: HTTP API
- Deployment stage: `$default`
- Automatic deployment: Enabled

The API connects the web frontend to the Lambda backend.

### Amazon DynamoDB

- Table name: `CloudStudyNotes`

DynamoDB stores the notes so that they remain available after the website is refreshed.

### Amazon S3

- Bucket name: `cloud-study-portal-docs-20261011`
- Document folder prefix: `study-documents/`
- Public access: Blocked
- Server-side encryption: SSE-S3

Uploaded documents are stored in the `study-documents/` prefix inside the private bucket.

### Lambda Environment Variables

The Lambda function uses these environment variables:

| Variable | Value |
|---|---|
| `TABLE_NAME` | `CloudStudyNotes` |
| `BUCKET_NAME` | `cloud-study-portal-docs-20261011` |

### CORS Configuration

The API is configured to allow browser requests from the local development origin:

`http://127.0.0.1:5500`

The configured methods are GET, POST, and DELETE, and the allowed request header includes `content-type`.

When the frontend is hosted elsewhere, the permitted origin must be updated to match the deployed website.

## 9. Security Considerations

The project includes the following security measures:

- S3 Block Public Access is enabled.
- Uploaded documents are stored in a private S3 bucket.
- S3 server-side encryption uses S3-managed keys (SSE-S3).
- The backend checks document extensions, content types, and file sizes.
- IAM permissions restrict the Lambda function's access to the resources it needs.
- The Lambda function uses a dedicated execution role named `CloudStudyLambdaRole`.
- The role allows CloudWatch logging, access to the `CloudStudyNotes` DynamoDB table, and document uploads to the S3 `study-documents/` prefix.

The dedicated Lambda role was tested after it was assigned to the function. The health check worked, notes remained saved after refreshing the website, and document uploads succeeded.

### Current Security Limitations

User authentication and per-user access control have not been implemented. The application is therefore a learning project and should not be used to store private student information in a multi-user production environment.

File extension and content-type checks alone cannot guarantee that a file is safe. Additional security measures would be needed before accepting untrusted uploads in a production system.

## 10. Testing and Verification

The project includes automated backend unit tests.

### Run the Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

### Automated Test Coverage

The 20 backend unit tests previously passed successfully.

The tests cover:

- Lambda response status codes, headers, and JSON responses.
- Health endpoint behaviour.
- Retrieving and creating notes.
- Generating unique note IDs.
- Saving notes through the backend.
- Handling missing fields and invalid JSON.
- Rejecting unsupported document types.
- Rejecting mismatched content types.
- Handling missing document content and invalid Base64 data.
- Successful TXT document uploads.
- Checking the S3 bucket, object key, content type, and server-side encryption settings.

AWS services are mocked during the automated unit tests so that application logic can be tested without making real AWS requests.

### Manual Verification

The following behaviours have also been checked:

- The health endpoint returns a successful response.
- Notes can be created and displayed.
- Notes remain saved after refreshing the website.
- Documents can be uploaded through the website.
- Uploaded document objects appear in the S3 `study-documents/` prefix.
- The application continues working after switching the Lambda function to its dedicated execution role.

## 11. Project Structure

The repository contains the frontend, backend, documentation, and automated tests.

```
cloud-study-portal/
├── backend/
│   └── lambda_function.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── docs/
│   ├── aws-setup.md
│   └── cloud-storage-test.txt
├── screenshots/
├── tests/
└── README.md
```

The structure above describes the intended organisation of the project. Confirm that the files in your GitHub repository match these paths before submitting.

## 12. Current Limitations and Future Improvements

### Current Limitations

- User authentication has not been implemented.
- Notes are not associated with individual student accounts.
- The website does not yet provide a complete document listing and download interface.
- The frontend is currently intended for local development rather than public hosting.
- The document upload size is limited to 3 MB.

### Future Improvements

- Add user authentication and authorisation.
- Associate notes and documents with individual users.
- Add document listing and secure download functionality.
- Expand automated tests and error handling.
- Host the frontend on an appropriate AWS hosting service.
- Add further security and monitoring improvements.

## 13. Conclusion

CloudStudy demonstrates how a simple student application can use AWS serverless services to manage notes and uploaded documents. The project combines a web frontend, a Python Lambda backend, API Gateway, DynamoDB, S3, IAM permissions, and CloudWatch logging.

The project provides practical experience with cloud architecture, API integration, persistent storage, access control, and automated testing.

## GitHub Repository

[CloudStudy — GitHub Repository](https://github.com/Nondu-dev/cloud-study-portal)
