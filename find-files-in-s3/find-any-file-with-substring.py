import boto3


def find_files_with_substring_in_name(bucket_name, substring, s3_client=None):

    """
    This function searches the files in a specified S3 bucket for those that
    contain a specific substring in their name.

    It always assumes no boto3 client has been used before and it creates
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

    try:

        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name):
            for obj in page.get('Contents', []):
                key = obj['Key']
                if substring.lower() in key.lower():  # Case-insensitive search
                    matching_files.append(key)
    except s3_client.exceptions.NoSuchBucket:
        print(f"Error: Bucket '{bucket_name}' not found.")
        return []  # Return an empty list if the bucket doesn't exist
    except Exception as e:  # Catch other potential errors (e.g., permissions)
        print(f"Error accessing bucket '{bucket_name}': {e}")
        return []

    return matching_files


def main():
    """
        This is the main function of the program. It continuously runs in a loop, presenting
        users with a menu of options for interacting with the system. The loop continues
        until the user selects the "quit" option.

        The function does not take any arguments and does not return any values.

        During each loop iteration, the function:
        - Displays a menu of options to the user bucket_name and substring to search for.
        - Waits for the user to select an option.
        - Executes the action associated with the selected option.

        If the "quit" option is selected, the function breaks the loop and the program ends.
        """

    s3 = boto3.client('s3')
    while True:
        bucket_name = input("Enter S3 bucket name (or 'q' to quit): ")
        if bucket_name.lower() == 'q':
            break

        substring = input("Enter substring to search for in file names: ")

        matching_files = find_files_with_substring_in_name(bucket_name, substring, s3)

        if matching_files:
            print("Files containing the substring in their names:")
            for file in matching_files:
                print(file)
        else:
            print("No matching files found.")


if __name__ == "__main__":
    main()
