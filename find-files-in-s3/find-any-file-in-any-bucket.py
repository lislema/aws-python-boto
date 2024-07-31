import boto3


def find_files_with_substring_in_named_bucket(bucket_name, substring, s3_client=None):

    """
    This function searches the files in a specified S3 bucket for those that
    contain a specific substring in their name.

    It always assumes no boto3 client has been used before, and it creates
    a new client.

    Args:
        bucket_name (str): The name of the S3 bucket to search in.
        substring (str): The substring to search for in the file names.
        s3_client=none (bool): defaults to none.

    Returns:
        List[str]: A list of file names in the specified S3 bucket that contain the substring.
    """

    if s3_client is None:
        s3_client = boto3.client('s3')

    matching_files = []

    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if substring.lower() in key.lower():
                matching_files.append(key)

    return matching_files


def list_buckets(s3_client):
    """
    This function returns a list of all bucket names in an AWS S3 instance.
    The function uses the provided boto3 client to interact with AWS.

    Args:
        s3_client (boto3.client): The boto3 client that you want to use to interact with AWS S3.

    Returns:
       list: A list of the names of all buckets in the given S3 instance.
    """

    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets


def main():
    """
        This is the main function of the program. It continuously runs in a loop, presenting
        users with a menu of options for interacting with the system. The loop continues
        until the user selects the "quit" option.

        The function does not take any arguments and does not return any values.

        During each loop iteration, the function:
        - Displays a list of buckets available to the user and substring to search for.
        - Waits for the user to select an option.
        - Executes the action associated with the selected option.

        If the "quit" option is selected, the function breaks the loop and the program ends.
        """

    s3 = boto3.client('s3')
    while True:
        print("\nAvailable S3 Buckets:")
        buckets = list_buckets(s3)
        for i, bucket in enumerate(buckets):
            print(f"{i + 1}. {bucket}")

        bucket_choice = input("Enter the number of the bucket to search (or 'q' to quit): ")
        if bucket_choice.lower() == 'q':
            break

        try:
            bucket_index = int(bucket_choice) - 1
            if 0 <= bucket_index < len(buckets):
                bucket_name = buckets[bucket_index]
            else:
                print("Invalid bucket number.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        substring = input("Enter substring to search for in file names: ")

        matching_files = find_files_with_substring_in_named_bucket(bucket_name, substring, s3)

        if matching_files:
            print("Files containing the substring in their names:")
            for file in matching_files:
                print(file)
        else:
            print("No matching files found.")

        input("Press Enter to continue to the search...")  # Wait for user input


if __name__ == "__main__":
    main()
