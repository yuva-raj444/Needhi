import React, { useState, useRef, useEffect } from 'react';
import { askQuestion } from '../services/api';
import { SAMPLE_QUESTIONS } from '../utils/constants';

function LoadingDots() {
  return (
    <div className="loading-dots">
      <span></span><span></span><span></span>
    </div>
  );
}

export default function ChatInterface({ language }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (question = null) => {
    const q = question || input.trim();
    if (!q || loading) return;

    const userMsg = { role: 'user', content: q };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const data = await askQuestion(q);
      const assistantMsg = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources || [],
        category: data.category,
        language: data.detected_language,
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg = {
        role: 'assistant',
        content:
          language === 'ta'
            ? '❌ பிழை ஏற்பட்டது. பின்னர் முயற்சிக்கவும்.'
            : '❌ Sorry, an error occurred. Please try again later.',
        sources: [],
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const samples = SAMPLE_QUESTIONS[language] || SAMPLE_QUESTIONS.en;

  return (
    <div className="card chat-container">
      {/* Messages */}
      <div className="chat-messages">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-light)' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚖️</div>
            <h3 style={{ color: 'var(--primary)', marginBottom: '0.5rem' }}>
              {language === 'ta' ? 'உங்கள் சட்ட கேள்வியை கேளுங்கள்' : 'Ask Your Legal Question'}
            </h3>
            <p style={{ fontSize: '0.9rem' }}>
              {language === 'ta'
                ? 'இந்திய சட்டங்கள் பற்றி தமிழ் அல்லது ஆங்கிலத்தில் கேளுங்கள்'
                : 'Ask about Indian laws in Tamil or English'}
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.category && (
              <div
                className="category-badge"
                style={{ background: 'var(--accent)', color: 'var(--primary-dark)' }}
              >
                {msg.category}
              </div>
            )}
            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
            {msg.sources && msg.sources.length > 0 && (
              <details className="sources">
                <summary>
                  📚 {language === 'ta' ? `${msg.sources.length} மூலங்கள்` : `${msg.sources.length} Sources`}
                </summary>
                {msg.sources.map((src, j) => (
                  <div key={j} className="source-item">
                    <strong>{src.source || 'Unknown'}</strong>
                    <p>{src.text}</p>
                  </div>
                ))}
              </details>
            )}
          </div>
        ))}

        {loading && (
          <div className="message assistant">
            <LoadingDots />
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Sample Questions */}
      {messages.length === 0 && (
        <div className="sample-questions">
          {samples.map((q, i) => (
            <button key={i} className="sample-q-btn" onClick={() => handleSend(q)}>
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="chat-input-area">
        <div className="chat-input-row">
          <input
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              language === 'ta'
                ? 'உங்கள் சட்ட கேள்வியை இங்கே தட்டச்சு செய்யவும்...'
                : 'Type your legal question here...'
            }
            disabled={loading}
          />
          <button className="send-btn" onClick={() => handleSend()} disabled={loading || !input.trim()}>
            {loading ? '...' : language === 'ta' ? 'அனுப்பு ➤' : 'Send ➤'}
          </button>
        </div>
      </div>
    </div>
  );
}
