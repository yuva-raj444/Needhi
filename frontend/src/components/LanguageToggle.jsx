import React from 'react';

export default function LanguageToggle({ language, setLanguage }) {
  return (
    <div className="lang-toggle">
      <button
        className={`lang-btn ${language === 'en' ? 'active' : ''}`}
        onClick={() => setLanguage('en')}
        aria-label="Switch to English"
      >
        🇬🇧 EN
      </button>
      <button
        className={`lang-btn ${language === 'ta' ? 'active' : ''}`}
        onClick={() => setLanguage('ta')}
        aria-label="Switch to Tamil"
      >
        🇮🇳 தமிழ்
      </button>
    </div>
  );
}
