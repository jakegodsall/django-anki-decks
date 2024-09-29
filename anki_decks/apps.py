from pathlib import Path
import platform

from django.apps import AppConfig
from django.conf import settings


class AnkiDecksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anki_decks'
    verbose_name = 'Anki Flashcard Application'

    def ready(self):
        if not hasattr(settings, 'ANKI_USER'):
            settings.ANKI_USER = 'User 1'

        if not hasattr(settings, 'ANKI_COLLECTION_PATH'):
            if platform.system() == 'Darwin':
                settings.ANKI_COLLECTION_PATH = (
                        Path('~/Library/Application Support/Anki2')
                        .expanduser() / settings.ANKI_USER / 'collection.anki2'
                )
            elif platform.system() == 'Windows':
                settings.ANKI_COLLECTION_PATH = (
                        Path('~/AppData/Roaming/Anki2')
                        .expanduser() / settings.ANKI_USER / 'collection.anki2'
                )
            elif platform.system() == 'Linux':
                settings.ANKI_COLLECTION_PATH = (
                        Path('~/.local/share/Anki2')
                        .expanduser() / settings.ANKI_USER / 'collection.anki2'
                )
            else:
                settings.ANKI_COLLECTION_PATH = None

        if not hasattr(settings, 'ANKI_DECKS'):
            settings.ANKI_DECKS = ['*']
