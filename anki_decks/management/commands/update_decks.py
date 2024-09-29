import os
from pathlib import Path
import shutil

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings

from anki_decks.models import FlashcardDeck
from anki_decks.anki_service import AnkiDeckExporter

from anki_decks.utils import download_anki_db_from_s3, delete_directory


class Command(BaseCommand):
    help = "Export anki decks and update the database"

    def handle(self, *args, **kwargs):
        database_dir = settings.ANKI_COLLECTION_PATH
        database_filename = settings.ANKI_COLLECTION_FILE_NAME
        database_path = Path(database_dir) / database_filename

        database_is_temp = False

        if not Path(database_path).is_file():
            self.stdout.write(f"File not found locally. Downloading from S3")
            database_dir, database_filename = download_anki_db_from_s3()
            database_is_temp = True
        else:
            self.stdout.write(f"Found local database at: {database_path}")

        # Instantiate the Anki deck exporter
        exporter = AnkiDeckExporter(database_path)

        print("Database Path", database_path)

        if len(settings.ANKI_DECKS) == 1 and settings.ANKI_DECKS[0] == '*':
            deck_names = exporter.get_deck_names()  # Process all decks
        else:
            deck_names = settings.ANKI_DECKS  # Process only the decks specified in settings

        # Loop through decks in the collection
        for deck_name in deck_names:
            if deck_name not in exporter.get_deck_names():
                self.stdout.write(f"{deck_name} deck was not found in the database.")
                continue

            new_deck_name = '-'.join(deck_name.split('::'))

            # Export the deck to a temporary file
            export_file_path = exporter.export_deck(deck_name)

            # Check if the deck exists in the database
            existing, created = FlashcardDeck.objects.get_or_create(name=new_deck_name)

            # Open the temporary file and save it to the FileField
            with open(export_file_path, 'rb') as f:
                file_data = File(f)

                output_file = new_deck_name + '.apkg'

                # Save the file, overwriting any existing files with the same name
                if created:
                    existing.deck.save(output_file, file_data)
                else:
                    # Delete the existing file first
                    if existing.deck:
                        existing.deck.delete(save=False)

                    existing.update_upload(output_file, file_data)

            self.stdout.write(f"{new_deck_name} deck has been exported")

        if database_is_temp:
            delete_directory(database_dir)
