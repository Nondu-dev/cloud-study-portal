# CloudStudy AWS Setup

## API Gateway

- API name:  CloudStudyApi
- API type:  HTTP API
- Region:  Europe (Stockholm) — eu-north-1
- Route:  GET /health
- Stage:  $default
- Status:  Successfully tested

### Invoke URL

https://q4mgnyvz5j.execute-api.eu-north-1.amazonaws.com

### Health Check

To test the API, add `/health` to the end of the Invoke URL and open it in a browser.

Expected response:

```json
{
  "message": "Welcome to CloudStudy",
  "project": "CloudStudy Student Notes Portal",
  "status": "running"
}
```