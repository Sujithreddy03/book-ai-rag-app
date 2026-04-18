from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from books.models import Book
from books.serializers import BookSerializer
from .scraper import scrape_books
from .rag_utils import get_relevant_context
from .ai_utils import generate_summary, generate_answer
from rest_framework import status



@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_book(request, pk):
    book = Book.objects.get(id=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def scrape_books_api(request):
    scrape_books()
    return Response({"message": "Books scraped and saved successfully"})

@api_view(['GET'])
def book_summary(request, pk):
    book = Book.objects.get(id=pk)
    summary = generate_summary(book.description)
    return Response({"summary": summary})

@api_view(['POST'])
def ask_question(request):
    question = request.data.get("question")

    # simple context (all book descriptions)
    books = Book.objects.all()
    context = " ".join([book.description for book in books])
    answer = generate_answer(question)

    return Response({"answer": answer})


@api_view(['POST'])
def ask_rag(request):
    try:
        question = request.data.get("question")

        if not question:
            return Response(
                {"error": "Question is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        answer = generate_answer(question)

        return Response({
            "question": question,
            "answer": answer
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )