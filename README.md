# CloudStudy — Student Notes and Document Portal

## 1. Project Overview

CloudStudy is a cloud-based student notes and document portal developed as a solo Cloud Computing project.

The application allows students to create, view, and delete study notes and upload study documents through a web interface. It uses AWS serverless services, a managed database, and cloud object storage to process and store information.

## 2. Project Objectives

- Build a web application connected to cloud services.
- Use serverless computing to process application requests.
- Store study notes in a managed cloud database.
- Store uploaded study documents in private cloud storage.
- Apply input validation and access permissions.
- Demonstrate cloud architecture, testing, and version control.

## 3. Implemented Features

- **Create study notes:** Save a subject, title, and content.
- **View study notes:** Retrieve saved notes from DynamoDB.
- **Delete study notes:** Remove notes through the website.
- **Upload study documents:** Upload PDF, TXT, and DOCX files.
- **File validation:** Check document extensions, content types, and file sizes.
- **Cloud storage:** Store uploaded documents in Amazon S3.
- **Serverless processing:** Handle requests using AWS Lambda.
- **HTTP API:** Connect the frontend and backend using Amazon API Gateway.
- **Error handling:** Display status messages when operations succeed or fail.

Document uploads are limited to 3 MB per file.

## 4. Technologies and Services

| Technology or service | Purpose |
|---|---|
| HTML5 | Frontend structure |
| CSS3 | Frontend styling |
| JavaScript | User interaction and API requests |
| Python | Backend application logic |
| AWS Lambda | Serverless request processing |
| Amazon API Gateway | HTTP API endpoints |
| Amazon DynamoDB | Study notes storage |
| Amazon S3 | Study document storage |
| AWS IAM | AWS access and permissions |
| Amazon CloudWatch | Logging and troubleshooting |
| Git and GitHub | Version control and source code hosting |

## 5. System Architecture

The frontend sends HTTP requests to Amazon API Gateway. API Gateway forwards the requests to AWS Lambda, which validates and processes them. Lambda then interacts with DynamoDB for study notes or Amazon S3 for uploaded documents.

```text
                 Student
                    |
                    v
            CloudStudy Frontend
                    |
                    v
           Amazon API Gateway
                    |
                    v
               AWS Lambda
                    |
             +------+------+
             |             |
             v             v
      Amazon DynamoDB   Amazon S3
       Study Notes    Study Documents
```

### Study Notes Workflow

1. The student enters a subject, title, and note content.
2. The frontend sends the information to the API.
3. Lambda validates the information.
4. The note is saved in DynamoDB.
5. The frontend retrieves and displays saved notes.
6. The student can delete a note through the application.

### Document Upload Workflow

1. The student selects a supported document.
2. The frontend validates the file type and size.
3. The file content is sent to the API.
4. Lambda validates the request and decodes the file content.
5. Lambda uploads the file to the private S3 bucket.
6. The frontend displays the upload result.

## 6. API Endpoints

| HTTP method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks backend availability |
| GET | `/notes` | Retrieves study notes |
| POST | `/notes` | Creates a study note |
| DELETE | `/notes/{noteId}` | Deletes a study note |
| POST | `/documents` | Uploads a study document |

## 7. Project Structure

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

## 8. AWS Configuration

The application is deployed using AWS resources in the `eu-north-1` region.

| Resource | Purpose |
|---|---|
| CloudStudyNotesFunction | Lambda backend |
| CloudStudyApi | HTTP API |
| CloudStudyNotes | DynamoDB table |
| S3 document bucket | Stores uploaded documents |

The Lambda function uses these environment variables:

- `TABLE_NAME` — identifies the DynamoDB table.
- `BUCKET_NAME` — identifies the S3 bucket.

The API uses an automatically deployed `$default` stage.

AWS IAM permissions control access to the required resources. AWS configuration and resource names may need to be adjusted when reproducing the project in another account.

## 9. Security Considerations

The project applies several basic cloud security measures:

- The S3 bucket has Block Public Access enabled.
- Uploaded documents are stored without making them publicly accessible.
- S3 objects use server-side encryption with Amazon S3-managed keys (SSE-S3).
- The backend validates document extensions, content types, and file sizes.
- IAM policies control access to AWS resources.
- API Gateway CORS settings restrict permitted browser origins.

**Further security improvements:** Replace broad permissions on the Lambda execution role with least-privilege permissions. Add user authentication and authorization before supporting multiple students with private individual accounts. File extension and content-type checks alone do not guarantee that a file is safe.

### 10. Testing and Verification

### Automated Tests

The backend has 20 automated unit tests, all of which passed.

Run the tests from the project root using:

```
python -m unittest discover -s tests -v
```

The tests cover:

- Lambda response status codes, headers, and JSON formatting.
- Health endpoint availability and project information.
- Retrieving study notes.
- Creating notes, generating unique IDs, and saving data.
- Validation of missing note fields and invalid JSON.
- Document upload validation, including unsupported file types, mismatched content types, missing content, and invalid Base64 data.
- Successful TXT upload handling, including the S3 bucket, object key, content type, and server-side encryption settings.

The automated tests use mocks for AWS services, so they test application logic without performing real AWS operations.

### Manual Verification

The following checks were completed through the live application and AWS Console:

- The health endpoint reports that the backend is running.
- Study notes can be created and displayed.
- Saved notes remain available after refreshing the page.
- Study notes can be deleted.
- A TXT document can be uploaded through the website.
- The uploaded document was verified in the S3 bucket's `study-documents/` folder.

## 11. Current Limitations

- User registration and login are not implemented.
- Uploaded documents can be stored, but the website does not yet provide a document listing or download interface.
- The frontend is not yet documented as a publicly hosted website.
- Document uploads are limited to 3 MB per file.
- Per-user ownership and access control are not implemented.

## 12. Future Improvements

- Implement secure user authentication and authorization.
- Associate notes and documents with individual users.
- Add a document listing and secure download functionality.
- Expand automated testing.
- Deploy the frontend to a suitable hosting service.

## 13. Repository

Source code and project documentation:

[CloudStudy — GitHub Repository](https://github.com/Nondu-dev/cloud-study-portal)
