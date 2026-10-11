# CloudStudy — Student Notes and Document Portal

CloudStudy is a cloud-based student application built with AWS. It allows students to create, view, and delete study notes, with the notes stored in a cloud database.

## Project Features

- Create study notes with a subject, title, and content.
- Retrieve saved notes from the cloud.
- Delete notes that are no longer needed.
- Store note data in Amazon DynamoDB.
- Use AWS Lambda to process application requests.
- Use Amazon API Gateway to expose HTTP endpoints.
- Store study documents in a private Amazon S3 bucket.

## AWS Architecture

The notes application follows this request flow:

1. **Frontend:** HTML, CSS, and JavaScript provide the website interface.
2. **Amazon API Gateway:** Receives HTTP requests from the frontend.
3. **AWS Lambda:** Processes requests to create, retrieve, and delete notes.
4. **Amazon DynamoDB:** Stores the notes so they remain available after a page refresh.
5. **Amazon S3:** Stores study documents separately from the notes database.

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon API Gateway | Provides HTTP endpoints for the application |
| AWS Lambda | Runs the Python backend code without managing a server |
| Amazon DynamoDB | Stores study notes |
| Amazon S3 | Stores study documents |
| AWS IAM | Controls permissions for AWS resources |
| Amazon CloudWatch | Supports Lambda logging and troubleshooting |

## Current API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Checks the API health |
| GET | `/notes` | Retrieves saved notes |
| POST | `/notes` | Creates a study note |
| DELETE | `/notes/{noteId}` | Deletes a note by its ID |

## Amazon S3 Storage

A private S3 bucket was created with the following configuration:

- Bucket: `cloud-study-portal-docs-20261011`
- Region: `eu-north-1` (Europe — Stockholm)
- Object Ownership: Bucket owner enforced
- Block Public Access: Enabled
- Default encryption: Amazon S3 managed keys (SSE-S3)

A test document named `cloud-storage-test.txt` was uploaded to verify that document storage works.

The bucket remains private. Public access is not required for this storage test.

## Testing Completed

- Confirmed that the API health endpoint returns a running status.
- Confirmed that the notes endpoint can retrieve records from DynamoDB.
- Created a study note through the website.
- Refreshed the website and confirmed that the saved note remained visible.
- Deleted a duplicate note through the website.

## Security Considerations

- S3 public access is blocked.
- The Lambda function uses an IAM execution role to access AWS services.
- API CORS settings control which browser origins are permitted to make cross-origin requests.
- CORS is not authentication. The API currently has no user login, so it should not be treated as a private production service.
- The Lambda execution role still has broad permissions that should be reduced before a production deployment.

## What I Learned

This project helped me practise connecting a frontend to cloud services, creating API endpoints, using a serverless backend, storing records in DynamoDB, and storing documents in S3.

I also tested data persistence and deletion, explored IAM permissions, and learned why private storage and appropriate access controls matter in cloud applications.

## Project Structure

```text
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

## Future Improvements

- Add secure document uploads to Amazon S3 through the backend.
- Improve input validation and error handling.
- Introduce authentication and authorization.
- Add automated tests and deployment documentation.

## Project Repository

Source code: https://github.com/Nondu-dev/cloud-study-portal
