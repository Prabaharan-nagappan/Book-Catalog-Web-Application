from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="books"),
    path('book/<str:book_id>/', views.book_details, name='book_details'),

]
