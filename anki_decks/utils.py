import time
import os
import shutil
from pathlib import Path
import boto3
from django.conf import settings


def download_anki_db_from_s3():
    """Download the database file from S3 for processing decks"""

    s3_client = boto3.client('s3')

    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = 'anki_decks/database/collection.anki2'

    # Log the bucket and key to ensure they are correct
    print(f"Downloading from bucket: {s3_bucket}, key: {s3_key}")

    local_db_dir = settings.ANKI_COLLECTION_PATH
    local_db_filename = settings.ANKI_COLLECTION_FILE_NAME

    local_db_path = Path(local_db_dir) / local_db_filename
    local_db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        s3_client.download_file(s3_bucket, s3_key, str(local_db_path))
        print(f"Anki database downloaded to {local_db_path}")
    except s3_client.exceptions.NoSuchKey:
        print(f"Error: The object with key {s3_key} was not found in bucket {s3_bucket}.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    retries = 5
    while not Path(local_db_path).is_file() and retries > 0:
        print(f"Waiting for the file to be accessible... ({retries} retries left)")
        time.sleep(1)
        retries -= 1

    if not Path(local_db_path).is_file():
        print(f"Error: File {local_db_path} not accessible after downloading.")
        return None

    # Change permissions on the database file
    os.chmod(local_db_path, 0o644)

    return local_db_dir, local_db_filename


def remove_anki_db_from_s3():
    """Delete the database file from S3 after processing"""
    s3_client = boto3.client('s3')

    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME
    s3_key = 'anki_decks/database/collection.anki2'

    s3_client.delete_object(Bucket=s3_bucket, Key=s3_key)
    print(f"The file at {s3_key} has been deleted from the {s3_key} bucket")


def delete_directory(dir_path):
    dir_path = Path(dir_path)

    if dir_path.exists() and dir_path.is_dir():
        shutil.rmtree(dir_path)
        print(f"Deleted the local database directory: {dir_path}")
    else:
        print(f"Error: Could not find the local directory to delete: {dir_path}")