import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [books, setBooks] = useState([]);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  // fetch books
  useEffect(() => {
  axios.get("http://127.0.0.1:8000/api/books/")
    .then(res => {
      console.log("BOOK DATA:", res.data); // 👈 ADD THIS
      setBooks(res.data);
    })
    .catch(err => console.log("ERROR:", err));
}, []);

  // get summary
  const getSummary = (id) => {
  axios.get(`http://127.0.0.1:8000/api/summary/${id}/`)
    .then(res => {
      console.log("SUMMARY RESPONSE:", res.data); // 👈 debug
      setSummary(res.data.summary); // 👈 IMPORTANT
    })
    .catch(err => console.log(err));
};

  // ask question (RAG)
  const askQuestion = () => {
  axios.post("http://127.0.0.1:8000/api/ask-rag/", {
    question: question
  })
  .then(res => {
    console.log("ANSWER:", res.data);
    setAnswer(res.data.answer);
  })
  .catch(err => console.log(err));
};
  return (
    <div style={{ padding: "20px" }}>
      <h1>📚 Book AI App</h1>

      <h2>Books</h2>
      {books.map(book => (
        <div key={book.id}>
          <p>{book.title}</p>
          <button onClick={() => getSummary(book.id)}>
            Get Summary
          </button>
        </div>
      ))}

      <h2>Summary</h2>
      <p>{summary}</p>

      <h2>Ask Question</h2>
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about books..."
      />
      <button onClick={askQuestion}>Ask</button>

      <h2>Answer</h2>
      <p>{answer}</p>
    </div>
  );
}

export default App;