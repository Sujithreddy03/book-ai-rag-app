from transformers import pipeline
from .rag_utils import get_relevant_context

# 🔥 Load model (balanced speed + quality)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)


# 📖 FUNCTION 1: Generate Summary
def generate_summary(text):
    if not text:
        return "No description available for this book."

    # 🔥 limit input
    text = text[:800]

    prompt = f"""
Summarize the following text in 2-3 complete sentences.
Make sure the answer is complete and does not cut off.

{text}

Summary:
"""

    try:
        result = generator(
            prompt,
            max_new_tokens=120,   # 🔥 increase slightly
            do_sample=True,
            temperature=0.5,      # 🔥 lower = more stable
            top_p=0.9,
            repetition_penalty=1.2
        )

        summary = result[0]["generated_text"].strip()

        # ✅ fix incomplete sentence
        if not summary.endswith((".", "!", "?")):
            summary += "."

        return summary

    except Exception as e:
        return f"Error generating summary: {str(e)}"


# 🤖 FUNCTION 2: Generate Answer using RAG
def generate_answer(question):
    if not question:
        return "Please ask a valid question."

    context = get_relevant_context(question)

    if not context:
        context = "No relevant book data found."

    # 🔥 limit context size
    context = context[:800]

    # ✅ IMPROVED PROMPT (CHANGE HERE)
    prompt = f"""
You are a helpful AI assistant.

Use ONLY the context below to answer the question.

Give a clear and meaningful answer in 2-3 sentences.
Write complete sentences with proper explanation (not just keywords).

Context:
{context}

Question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=180,   # 🔥 increase from 120 → 180
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        repetition_penalty=1.3
    )

    answer = result[0]["generated_text"].strip()
    return answer