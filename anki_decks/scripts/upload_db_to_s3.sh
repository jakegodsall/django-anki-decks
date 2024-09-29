#!/bin/bash

# Define the path to your Anki database and S3 bucket
ANKI_DB_PATH="$HOME/Library/Application Support/Anki2/$ANKI_USER/collection.anki2"
S3_DB_PATH="anki_decks/database/collection.anki2"

# Ensure that AWS_STORAGE_BUCKET_NAME and ANKI_USER are set
if [[ -z "$AWS_STORAGE_BUCKET_NAME" || -z "$ANKI_USER" ]]; then
  echo "Error: AWS_STORAGE_BUCKET_NAME or ANKI_USER is not set."
  exit 1
fi

# Upload the Anki database to S3
aws s3 cp "$ANKI_DB_PATH" "s3://$AWS_STORAGE_BUCKET_NAME/$S3_DB_PATH"