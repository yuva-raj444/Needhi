import React from 'react';

export default function Header({ language, setLanguage }) {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="header-brand">
          <span className="header-logo">⚖️</span>
          <div>
            <div className="header-title">Needhi</div>
            <div className="header-subtitle">
              {language === 'ta'
                ? 'AI சட்ட உதவியாளர் — இந்திய குடிமக்களுக்கு'
                : 'AI Legal Assistant — For Indian Citizens'}
            </div>
          </div>
        </div>

        <div className="header-controls">
          <div className="lang-toggle">
            <button
              className={`lang-btn ${language === 'en' ? 'active' : ''}`}
              onClick={() => setLanguage('en')}
            >
              English
            </button>
            <button
              className={`lang-btn ${language === 'ta' ? 'active' : ''}`}
              onClick={() => setLanguage('ta')}
            >
              தமிழ்
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
