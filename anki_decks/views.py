from django.shortcuts import render
from .models import FlashcardDeck

def list_exported_decks(request):
    decks = FlashcardDeck.objects.all()

    return render(request, 'anki_decks/flashcard_decks.html', {'decks': decks})
