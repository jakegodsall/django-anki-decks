from pathlib import Path
from anki.storage import Collection
from anki.exporting import AnkiPackageExporter
from django.core.files.temp import NamedTemporaryFile

class AnkiDeckExporter:
    def __init__(self, collection_path):
        # Initialize the Anki collection
        self.collection_path = Path(collection_path)
        self.col = Collection(str(self.collection_path))

    def get_decks(self):
        # Get all decks
        return self.col.decks.all()

    def get_decks_by_prefix(self, prefix):
        # Get all decks and filter by a prefix
        decks = self.col.decks.all()
        return [deck for deck in decks if deck['name'].startswith(prefix)]

    def get_decks_by_array(self, deck_names):
        # Get decks by an array of deck names
        decks = self.col.decks.all()
        return [deck for deck in decks if deck['name'] in deck_names]

    def get_deck_names(self):
        # Get names of all decks
        decks = self.col.decks.all()
        deck_names = [deck['name'] for deck in decks]
        return deck_names

    def get_deck_names_by_prefix(self, prefix):
        # Get names of decks that match the prefix
        filtered_decks = self.get_decks_by_prefix(prefix)
        return [deck['name'] for deck in filtered_decks]

    def get_cards_from_deck(self, deck_id):
        # Get all cards from a specific deck by deck_id
        return self.col.db.all(f'SELECT * FROM cards WHERE did={deck_id}')

    def export_deck(self, deck_name):
        # Export a deck by name to a temporary file
        deck_id = self.col.decks.id(deck_name)

        # Create an AnkiPackageExporter and set it to export the specific deck
        exporter = AnkiPackageExporter(self.col)

        # Set the deck ID to export the desired deck
        exporter.did = deck_id

        # Exclude scheduling data if desired
        exporter.includeSched = False

        # Create a temporary file for the export
        with NamedTemporaryFile(suffix='.apkg', delete=False) as tmp:
            export_file_path = tmp.name
            exporter.exportInto(export_file_path)

        return export_file_path



