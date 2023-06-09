from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()
    isbn_number = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            MinLengthValidator(10, 'ISBN must be 10 or 13 digits long.'),
            MaxLengthValidator(13, 'ISBN must be 10 or 13 digits long.')
        ]
    )
    number_of_pages = models.IntegerField()
    cover_link = models.URLField()
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('ka', 'Georgian'),
        ('zh', 'Chinese'),
        ('ar', 'Arabic'),
        ('ja', 'Japanese'),
        ('ru', 'Russian'),
        ('hi', 'Hindi'),
        ('pt', 'Portuguese'),
        ('it', 'Italian'),
    ]
    publication_language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.title
