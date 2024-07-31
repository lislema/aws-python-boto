import boto3


def find_files_with_substring(bucket_name, substring, s3_client=None):
    if s3_client is None:
        s3_client = boto3.client('s3')

    matching_files = []

    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith(('.txt', '.csv', '.json')):  # Check for common text file types
                try:
                    response = s3_client.get_object(Bucket=bucket_name, Key=key)
                    content = response['Body'].read().decode('utf-8', errors='replace')
                    if substring in content:
                        matching_files.append(key)
                except Exception as e:
                    print(f"Error reading file {key}: {e}")

    return matching_files


def main():
    s3 = boto3.client('s3')
    while True:
        bucket_name = input("Enter S3 bucket name (or 'q' to quit): ")
        if bucket_name.lower() == 'q':
            break

        substring = input("Enter substring to search for: ")

        matching_files = find_files_with_substring(bucket_name, substring, s3)

        if matching_files:
            print("Files containing the substring:")
            for file in matching_files:
                print(file)
        else:
            print("No matching files found.")


if __name__ == "__main__":
    main()
