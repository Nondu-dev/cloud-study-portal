# cloud-study-portal

A cloud-based student notes and document storage application built with AWS.

## AWS S3 Storage

CloudStudy uses Amazon S3 to store study documents in the AWS cloud.

### Completed

- Created a private S3 bucket named `cloud-study-portal-docs-20261011`.
- Uploaded a test document named `cloud-storage-test.txt`.
- Verified that the uploaded object appears in the bucket.
- Kept public access blocked and used Bucket owner enforced for Object Ownership.

### What I learned

An Amazon S3 bucket stores objects such as documents and images. The bucket can remain private while authorized applications access its contents through appropriate AWS permissions.