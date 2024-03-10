# forms.py
from django import forms

class FavoriteBookForm(forms.Form):
    book_id = forms.CharField(widget=forms.HiddenInput())
