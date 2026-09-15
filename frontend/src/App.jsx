import { useState } from "react";
import DocumentUpload from "./components/DocumentUpload";
import VoiceRecorder from "./components/VoiceRecorder";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [audioUrl, setAudioUrl] = useState("");

  const clearConversation = () => {
    setQuestion("");
    setAnswer("");
    setSources([]);
    setAudioUrl("");
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <header className="navbar">
        <div className="navbar-inner">

          <div className="brand">
            <div className="brand-mark">V</div>
            <span>Voice RAG</span>
          </div>

          <div className="nav-status">
            <span className="status-dot"></span>
            Local AI
          </div>

        </div>
      </header>


      {/* HERO */}
      <section className="hero">
        <div className="hero-content">

          <div className="eyebrow">
            VOICE-POWERED DOCUMENT INTELLIGENCE
          </div>

          <h1>
            Ask your documents.
            <br />
            <span>Get intelligent answers.</span>
          </h1>

          <p>
            Upload a document, ask a question using your voice,
            and get an answer based on your documents.
          </p>

        </div>
      </section>


      {/* MAIN */}
      <main className="container">

        {/* STEP 01 */}
        <section className="section-card">

          <div className="section-header">

            <div className="section-number">
              01
            </div>

            <div>
              <h2>Upload document</h2>

              <p>
                Add a PDF to create your knowledge base.
              </p>
            </div>

          </div>

          <DocumentUpload />

        </section>


        {/* STEP 02 */}
        <section className="section-card">

          <div className="section-header">

            <div className="section-number">
              02
            </div>

            <div>
              <h2>Ask with your voice</h2>

              <p>
                Speak naturally and ask questions about your document.
              </p>
            </div>

          </div>

          <VoiceRecorder
            setQuestion={setQuestion}
            setAnswer={setAnswer}
            setSources={setSources}
            setAudioUrl={setAudioUrl}
          />

        </section>


        {/* QUESTION */}
        {question && (
          <section className="result-card">

            <div className="result-header">

              <div className="result-icon question-icon">
                Q
              </div>

              <div>
                <span className="result-label">
                  YOUR QUESTION
                </span>

                <h3>Voice transcription</h3>
              </div>

            </div>

            <div className="question-text">
              {question}
            </div>

          </section>
        )}


        {/* ANSWER */}
        {answer && (
          <section className="result-card answer-card">

            <div className="result-header">

              <div className="result-icon answer-icon">
                AI
              </div>

              <div>
                <span className="result-label">
                  AI RESPONSE
                </span>

                <h3>Answer</h3>
              </div>

            </div>

            <div className="answer-text">
              {answer}
            </div>


            {/* SOURCES */}
            {sources && sources.length > 0 && (
              <div className="sources">

                <div className="subsection-title">
                  Sources
                </div>

                <div className="source-list">

                  {sources.map((source, index) => (
                    <div
                      className="source"
                      key={index}
                    >

                      <div className="source-file">
                        PDF
                      </div>

                      <span>
                        {typeof source === "string"
                          ? source
                          : source?.source ||
                            source?.filename ||
                            `Source ${index + 1}`}
                      </span>

                    </div>
                  ))}

                </div>

              </div>
            )}


            {/* AUDIO */}
            {audioUrl && (
              <div className="audio-player">

                <div className="subsection-title">
                  Voice response
                </div>

                <audio
                  controls
                  src={audioUrl}
                />

              </div>
            )}


            {/* CLEAR */}
            <div className="result-actions">

              <button
                className="clear-button"
                onClick={clearConversation}
              >
                Clear conversation
              </button>

            </div>

          </section>
        )}

      </main>


      {/* FOOTER */}
      <footer className="footer">

        <div className="footer-inner">

          <span>Voice RAG</span>

          <span>Powered by local AI</span>

        </div>

      </footer>

    </div>
  );
}

export default App;