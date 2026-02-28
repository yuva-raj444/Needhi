import React, { useState } from 'react';
import { generateComplaint, downloadComplaintPDF } from '../services/api';

const INITIAL_FORM = {
  complainant_name: '',
  complainant_address: '',
  opponent_name: '',
  issue_description: '',
  location: '',
  date: '',
};

export default function ComplaintForm({ language }) {
  const [form, setForm] = useState({ ...INITIAL_FORM });
  const [draft, setDraft] = useState('');
  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const isFormValid = () =>
    form.complainant_name.trim() &&
    form.complainant_address.trim() &&
    form.opponent_name.trim() &&
    form.issue_description.trim() &&
    form.location.trim() &&
    form.date.trim();

  const handleGenerate = async () => {
    if (!isFormValid() || loading) return;
    setLoading(true);
    setError('');
    setDraft('');

    try {
      const data = await generateComplaint({ ...form, language });
      setDraft(data.draft_text);
    } catch (err) {
      setError(
        language === 'ta'
          ? 'புகார் உருவாக்குவதில் பிழை. மீண்டும் முயற்சிக்கவும்.'
          : 'Error generating complaint. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!isFormValid()) return;
    setPdfLoading(true);
    try {
      await downloadComplaintPDF({ ...form, language });
    } catch (err) {
      setError(
        language === 'ta'
          ? 'PDF பதிவிறக்கத்தில் பிழை.'
          : 'Error downloading PDF.'
      );
    } finally {
      setPdfLoading(false);
    }
  };

  const labels = {
    en: {
      title: 'Legal Complaint Drafter',
      name: 'Your Full Name',
      address: 'Your Address',
      opponent: 'Opponent / Respondent Name',
      issue: 'Issue Description',
      location: 'Incident Location',
      date: 'Date of Incident',
      generate: '📝 Generate Draft',
      pdf: '📄 Download PDF',
      generating: '⏳ Generating...',
      downloading: '⏳ Downloading...',
      preview: 'Complaint Preview',
    },
    ta: {
      title: 'சட்ட புகார் வரைவாளர்',
      name: 'உங்கள் முழு பெயர்',
      address: 'உங்கள் முகவரி',
      opponent: 'எதிர்கட்சி பெயர்',
      issue: 'சிக்கல் விவரம்',
      location: 'சம்பவ இடம்',
      date: 'சம்பவ தேதி',
      generate: '📝 வரைவு உருவாக்கு',
      pdf: '📄 PDF பதிவிறக்கம்',
      generating: '⏳ உருவாக்குகிறது...',
      downloading: '⏳ பதிவிறக்குகிறது...',
      preview: 'புகார் முன்னோட்டம்',
    },
  };

  const l = labels[language] || labels.en;

  return (
    <div className="card">
      <div className="card-header">
        <span>📝</span>
        <h2>{l.title}</h2>
      </div>
      <div className="card-body">
        <div className="form-grid">
          <div className="form-group">
            <label>{l.name}</label>
            <input name="complainant_name" value={form.complainant_name} onChange={handleChange} placeholder="e.g., Rajesh Kumar" />
          </div>
          <div className="form-group">
            <label>{l.opponent}</label>
            <input name="opponent_name" value={form.opponent_name} onChange={handleChange} placeholder="e.g., ABC Pvt. Ltd." />
          </div>
          <div className="form-group full-width">
            <label>{l.address}</label>
            <input name="complainant_address" value={form.complainant_address} onChange={handleChange} placeholder="e.g., 12, Gandhi Street, Chennai - 600001" />
          </div>
          <div className="form-group">
            <label>{l.location}</label>
            <input name="location" value={form.location} onChange={handleChange} placeholder="e.g., Chennai, Tamil Nadu" />
          </div>
          <div className="form-group">
            <label>{l.date}</label>
            <input name="date" type="date" value={form.date} onChange={handleChange} />
          </div>
          <div className="form-group full-width">
            <label>{l.issue}</label>
            <textarea
              name="issue_description"
              value={form.issue_description}
              onChange={handleChange}
              placeholder={
                language === 'ta'
                  ? 'உங்கள் சிக்கலை விரிவாக விவரிக்கவும்...'
                  : 'Describe your legal issue in detail...'
              }
              rows={5}
            />
          </div>
        </div>

        <div className="btn-group">
          <button className="btn-primary" onClick={handleGenerate} disabled={loading || !isFormValid()}>
            {loading ? l.generating : l.generate}
          </button>
          {draft && (
            <button className="btn-secondary" onClick={handleDownloadPDF} disabled={pdfLoading}>
              {pdfLoading ? l.downloading : l.pdf}
            </button>
          )}
        </div>

        {error && <div className="upload-status error" style={{ marginTop: '1rem' }}>{error}</div>}

        {draft && (
          <>
            <h3 style={{ marginTop: '1.5rem', color: 'var(--primary)', fontSize: '1rem' }}>
              {l.preview}
            </h3>
            <div className="complaint-preview">{draft}</div>
          </>
        )}
      </div>
    </div>
  );
}
