from django.contrib import admin
from .models import FlashcardDeck


class FlashcardDeckAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'deck', 'most_recent_upload', 'number_of_uploads']


admin.site.register(FlashcardDeck, FlashcardDeckAdmin)
