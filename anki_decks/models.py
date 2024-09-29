from django.db import models
from django.utils import timezone


class FlashcardDeck(models.Model):
    name = models.CharField(max_length=255)
    deck = models.FileField(upload_to='anki_decks/', null=True, blank=True)
    initial_upload = models.DateTimeField(auto_now_add=True)
    most_recent_upload = models.DateTimeField(null=True, blank=True)
    number_of_uploads = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Flashcard Decks'

    def __str__(self):
        return f"Deck: {self.name}"

    def update_upload(self, file_name, file_data):
        self.deck.save(file_name, file_data)
        self.most_recent_upload = timezone.now()
        self.number_of_uploads += 1
        self.save()
