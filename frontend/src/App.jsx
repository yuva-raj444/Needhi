import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import ClassifierPanel from './components/ClassifierPanel';
import ComplaintForm from './components/ComplaintForm';
import DocumentUpload from './components/DocumentUpload';
import Disclaimer from './components/Disclaimer';
import { TABS } from './utils/constants';

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [language, setLanguage] = useState('en');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'chat':
        return <ChatInterface language={language} />;
      case 'classifier':
        return <ClassifierPanel language={language} />;
      case 'complaint':
        return <ComplaintForm language={language} />;
      case 'upload':
        return <DocumentUpload language={language} />;
      default:
        return <ChatInterface language={language} />;
    }
  };

  return (
    <div className="app">
      <Header language={language} setLanguage={setLanguage} />

      {/* Tab Navigation */}
      <nav className="tab-nav">
        <div className="tab-nav-inner">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">
                {language === 'ta' ? tab.labelTa : tab.label}
              </span>
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <div className="content-container">
          {renderActiveTab()}
        </div>
      </main>

      <Disclaimer language={language} />
    </div>
  );
}

export default App;
