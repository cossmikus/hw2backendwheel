import boto3


class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket = "kassymkhan.bolat-bucket"
        self.file_id_mapping = {}

    def upload_file_by_tweet(self, file, filename, file_id):
        filekey = f"tweets/{filename}"
        self.s3.upload_fileobj(file, self.bucket, filekey)
        # Add the mapping between file ID and file key
        self.file_id_mapping[file_id] = filekey 
        object_url = f"https://{self.bucket}/{filekey}"
        return object_url

    def get_file_by_tweet(self, file_id):
        filekey = self.file_id_mapping.get(file_id)
        if filekey is None:
            # Handle the case where the file ID does not exist
            return None

        try:
            file_path = f"tweets/{file_id}"  # Update the file path here
            self.s3.download_file(self.bucket, filekey, file_path)
            return file_path
        except self.s3.exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == "404":
                # File not found in S3
                return None
            else:
                # Handle other potential errors
                raise
