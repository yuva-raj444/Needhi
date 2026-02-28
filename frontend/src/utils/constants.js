/**
 * NyayaSahaya — Frontend constants.
 */

export const LEGAL_CATEGORIES = [
  { key: 'Criminal', emoji: '🔴', color: '#e74c3c' },
  { key: 'Civil', emoji: '🔵', color: '#3498db' },
  { key: 'Family', emoji: '💜', color: '#9b59b6' },
  { key: 'Consumer', emoji: '🟢', color: '#27ae60' },
  { key: 'Land', emoji: '🟤', color: '#8B4513' },
  { key: 'Welfare', emoji: '🟠', color: '#f39c12' },
];

export const DISCLAIMER =
  '⚠️ This AI provides general legal information and is not a substitute for professional legal advice. Please consult a qualified lawyer for specific legal matters.';

export const SAMPLE_QUESTIONS = {
  en: [
    'What are my rights if my landlord refuses to return my security deposit?',
    'How do I file an FIR online in Tamil Nadu?',
    'What is Section 498A of IPC?',
    'Can a consumer file a complaint for a defective product?',
    'What are the grounds for divorce under Hindu Marriage Act?',
  ],
  ta: [
    'என் வீட்டு உரிமையாளர் என் பாதுகாப்புத் தொகையை திருப்பி தர மறுத்தால் என் உரிமைகள் என்ன?',
    'தமிழ்நாட்டில் ஆன்லைனில் FIR எப்படி பதிவு செய்வது?',
    'IPC பிரிவு 498A என்றால் என்ன?',
  ],
};

export const TABS = [
  { id: 'chat', label: 'Ask Legal Question', labelTa: 'சட்ட கேள்வி', icon: '💬' },
  { id: 'classifier', label: 'Classify Issue', labelTa: 'வகைப்படுத்து', icon: '🏷️' },
  { id: 'complaint', label: 'Draft Complaint', labelTa: 'புகார் வரைவு', icon: '📝' },
  { id: 'upload', label: 'Upload Documents', labelTa: 'ஆவணங்கள்', icon: '📄' },
];
