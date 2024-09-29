# django-anki-decks

## Introduction
`django-anki-decks` is a reusable Django application designed to host Anki flashcard decks.

It allows the user to export specified decks from the SQLite `collection.anki2` database used locally by the Anki desktop application,
and host them along with metadata in a Django application. 

## Motivation
This project provides a solution for hosting and sharing Anki decks with other users, bypassing the manual process of exporting from the Anki desktop app.
By utilizing a combination of Django, cloud storage, and crontab, users can sync and access their Anki decks as needed.
The application enables timely syncing of decks, according to user-defined schedules and requirements.

## How it Works

The application interfaces with directly with Anki’s SQLite database file, extracting relevant data using the official [anki](https://pypi.org/project/anki/) Python package.
Through customizable settings, users can configure:

- Location of the Anki database file
- Anki user
- Specific decks to export and host

### Example of `settings.py` Configuration:

```python
# settings.py

ANKI_COLLECTION_PATH = '/path/to/local/anki/database/'
ANKI_COLLECTION_FILE_NAME = 'collection.anki2'
ANKI_USER = "User 1"
ANKI_DECKS = ["Deck1", "Deck2"]
```
The application uses the `anki` package to export the decks defined in `settings.py` into temporary files in the local file system,
then creates or updates rows in the `FlashcardDeck` table to represent those decks. The actual file is stored in `MEDIA_ROOT`.
The temporary file is then deleted from the file system.

The main entry point to the application is the `update_decks` management command, that can be run with:

```shell
python manage.py update_decks
```

## Quick-Start Guide

### Local Development

1. Add `django-anki-decks` to your Django project by installing it via pip:
    ```shell
    pip install django-anki-decks
    ```

2. Add to Installed Apps:

    In your `settings.py`, add `'anki_decks'` to your `INSTALLED_APPS`:
    
    ```python
    INSTALLED_APPS = [
        ...
        'anki_decks',
    ]
    ```
3. Configure Anki Settings:

    Set up the required Anki configurations in `settings.py`:

    ```python
    ANKI_COLLECTION_PATH = '/path/to/local/anki/database/'
    ANKI_COLLECTION_FILE_NAME = 'collection.anki2'
    ANKI_USER = "User 1"
    ANKI_DECKS = ["Deck1", "Deck2"]
    ```
   
4. Run Migrations to create the necessary database tables:
    ```shell
    python manage.py migrate
    ```

5. Export and Host Decks:

    Use the provided management command to extract and export decks:
    ```shell
    python manage.py update_decks
    ```

6. Access the Decks:

    Your exported decks will be available in the configured media folder, ready to be served to your users.

### Running in Docker

When running the Django project in a Docker container, it is necessary to create a Docker volume that points to the location of the Anki SQLite database file on your local filesystem.

This ensures that the application can access the database within the Docker container.

## Deployment

For deployment, S3 storage has been implemented for handling the SQLite database file.

The process includes downloading the database from S3, exporting the decks from the file, creating model instances, and saving the decks as media files before deleting the local copy of the database.

All of this is handled through the `update_decks` command directly.

This requires an additional setting to be provided:

```python
AWS_STORAGE_BUCKET_NAME = "BUCKET_NAME"
```

## Contributing

We welcome contributions to this project, especially to support additional cloud providers for storage. The goal is to make the cloud integration more extensible, so feel free to contribute by adding new features, fixing bugs, or suggesting improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) for more details.