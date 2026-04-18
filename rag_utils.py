from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from books.models import Book

embedding = HuggingFaceEmbeddings()

vector_db = None


def create_vector_db():
    global vector_db

    if vector_db is not None:
        return vector_db

    books = Book.objects.all()

    texts = [
        f"Book: {book.title}\nDescription: {book.description[:400]}"
        for book in books
        if book.description
    ]

    if not texts:
        return None

    # ✅ FIX: explicitly disable persistence
    vector_db = Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        collection_name="books_collection"  # 🔥 important
    )

    return vector_db


def get_relevant_context(question):
    db = create_vector_db()

    if db is None:
        return "No book data available."

    docs = db.similarity_search(question, k=2)

    context = "\n\n".join([doc.page_content for doc in docs])

    return context[:800]  # 🔥 limit size