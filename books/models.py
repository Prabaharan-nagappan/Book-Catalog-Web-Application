from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class FavoriteBooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.CharField(max_length=100)  # Assuming book_id is a string

    class Meta:
        unique_together = ('user', 'book_id') 