# Generated by Django 5.0.7 on 2024-09-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anki_decks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flashcarddeck',
            options={'verbose_name_plural': 'Flashcard Decks'},
        ),
        migrations.RemoveField(
            model_name='flashcarddeck',
            name='link_to_deck',
        ),
        migrations.AddField(
            model_name='flashcarddeck',
            name='deck',
            field=models.FileField(blank=True, null=True, upload_to='anki_decks/'),
        ),
    ]
