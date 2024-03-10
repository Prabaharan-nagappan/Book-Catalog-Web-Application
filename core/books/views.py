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


def book_details(request, book_id):
    # Construct the URL for fetching details of the book using its ID
    api_url = f'https://www.googleapis.com/books/v1/volumes/{book_id}'
    
    # Make a request to the Google Books API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        book_data = response.json()
        
        # Render the details template with the book data
        return render(request, 'books/details.html', {'book': book_data})
    else:
        # If the request was not successful, handle the error accordingly
        error_message = f"Failed to fetch book details from the Google Books API. Status code: {response.status_code}"
        return render(request, 'books/error.html', {'error_message': error_message})