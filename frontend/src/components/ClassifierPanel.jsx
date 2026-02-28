import React, { useState } from 'react';
import { classifyIssue } from '../services/api';
import { LEGAL_CATEGORIES } from '../utils/constants';

export default function ClassifierPanel({ language }) {
  const [description, setDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleClassify = async () => {
    if (!description.trim() || loading) return;
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const data = await classifyIssue(description);
      setResult(data);
    } catch (err) {
      setError(
        language === 'ta'
          ? 'வகைப்படுத்துவதில் பிழை. மீண்டும் முயற்சிக்கவும்.'
          : 'Error classifying issue. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const getCategoryStyle = (category) => {
    const cat = LEGAL_CATEGORIES.find((c) => c.key === category);
    return cat ? { background: cat.color } : { background: '#888' };
  };

  const getCategoryEmoji = (category) => {
    const cat = LEGAL_CATEGORIES.find((c) => c.key === category);
    return cat ? cat.emoji : '⚪';
  };

  return (
    <div className="card">
      <div className="card-header">
        <span>🏷️</span>
        <h2>{language === 'ta' ? 'சட்ட சிக்கல் வகைப்படுத்தி' : 'Legal Issue Classifier'}</h2>
      </div>
      <div className="card-body">
        <div className="form-group">
          <label>
            {language === 'ta' ? 'உங்கள் சட்ட சிக்கலை விவரிக்கவும்' : 'Describe your legal issue'}
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder={
              language === 'ta'
                ? 'எடுத்துக்காட்டு: என் வீட்டு உரிமையாளர் என் பாதுகாப்புத் தொகையை திருப்பித் தர மறுக்கிறார்...'
                : 'Example: My landlord is refusing to return my security deposit after vacating the flat...'
            }
            rows={5}
          />
        </div>

        <div className="btn-group">
          <button className="btn-primary" onClick={handleClassify} disabled={loading || !description.trim()}>
            {loading
              ? language === 'ta'
                ? '⏳ பகுப்பாய்வு...'
                : '⏳ Analyzing...'
              : language === 'ta'
              ? '🏷️ வகைப்படுத்து'
              : '🏷️ Classify Issue'}
          </button>
        </div>

        {error && <div className="upload-status error" style={{ marginTop: '1rem' }}>{error}</div>}

        {result && (
          <div className="classifier-result">
            <div className="classifier-category">
              <span className="category-pill" style={getCategoryStyle(result.category)}>
                {getCategoryEmoji(result.category)} {result.category}
              </span>
              {result.confidence && (
                <span className="confidence-badge">
                  {language === 'ta' ? 'நம்பிக்கை' : 'Confidence'}: {result.confidence}
                </span>
              )}
            </div>
            <div className="classifier-explanation">{result.explanation}</div>
          </div>
        )}

        {/* Category Legend */}
        <div style={{ marginTop: '1.5rem', display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {LEGAL_CATEGORIES.map((cat) => (
            <span
              key={cat.key}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.3rem',
                padding: '0.3rem 0.7rem',
                borderRadius: '15px',
                background: `${cat.color}15`,
                color: cat.color,
                fontSize: '0.78rem',
                fontWeight: 600,
                border: `1px solid ${cat.color}30`,
              }}
            >
              {cat.emoji} {cat.key}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
