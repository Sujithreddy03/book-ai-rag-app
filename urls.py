from django.urls import path
from books.views import get_book,get_books,scrape_books_api,book_summary,ask_question,ask_rag

urlpatterns = [
    path('books/', get_books),
    path('book/<int:pk>/',get_book),
    path('scrape/',scrape_books_api),
    path('summary/<int:pk>/',book_summary),
    path('ask/',ask_question),
    path('ask-rag/',ask_rag),
]