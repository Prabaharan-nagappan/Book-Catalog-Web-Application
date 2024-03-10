import requests
from django.shortcuts import render

def home(request):
    query = request.GET.get('q', 'science')  # Default query is 'science' if not provided
    api_url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    
    # Make a request to the Google Books API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract relevant information from the response
        books = data.get('items', [])
        
        # Render the template with the received data
        return render(request, 'books/home.html', {'books': books})
    else:
        # If the request was not successful, handle the error accordingly
        error_message = f"Failed to fetch data from the Google Books API. Status code: {response.status_code}"
        return render(request, 'books/home.html', {'error_message': error_message})


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FavoriteBookForm
from .models import FavoriteBooks

def book_details(request, book_id):
    api_url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        book_data = response.json()
        form = FavoriteBookForm(initial={'book_id': book_id})
        if request.method == 'POST':
            form = FavoriteBookForm(request.POST)
            if form.is_valid():
                book_id = form.cleaned_data['book_id']  # Retrieve the book_id from the form data
                # Check if the book is already favorited by the user
                if not FavoriteBooks.objects.filter(user=request.user, book_id=book_id).exists():
                    # If the book is not already favorited, create a new FavoriteBooks instance
                    favorite_book = FavoriteBooks(user=request.user, book_id=book_id)
                    favorite_book.save()
                    messages.success(request, 'Book added to favorites.')
                else:
                    messages.warning(request, 'Book is already in your favorites.')
                return redirect('book_details', book_id=book_id)
        return render(request, 'books/details.html', {'book': book_data, 'form': form})
    else:
        error_message = f"Failed to fetch book details from the Google Books API. Status code: {response.status_code}"
        return render(request, 'books/error.html', {'error_message': error_message})