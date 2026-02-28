import React, { useState, useEffect, useCallback } from 'react';
import { uploadDocument, indexAllDocuments, getIndexStatus } from '../services/api';

export default function DocumentUpload({ language }) {
  const [status, setStatus] = useState(null);
  const [uploadMsg, setUploadMsg] = useState(null);
  const [loading, setLoading] = useState(false);
  const [indexing, setIndexing] = useState(false);
  const [dragging, setDragging] = useState(false);

  const fetchStatus = useCallback(async () => {
    try {
      const data = await getIndexStatus();
      setStatus(data);
    } catch {
      // API might not be ready
    }
  }, []);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  const handleUpload = async (file) => {
    if (!file) return;
    setLoading(true);
    setUploadMsg(null);

    try {
      const data = await uploadDocument(file);
      setUploadMsg({ type: 'success', text: `✅ ${data.message} (${data.chunks_created} chunks)` });
      fetchStatus();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Upload failed';
      setUploadMsg({ type: 'error', text: `❌ ${msg}` });
    } finally {
      setLoading(false);
    }
  };

  const handleIndexAll = async () => {
    setIndexing(true);
    setUploadMsg(null);
    try {
      const data = await indexAllDocuments();
      setUploadMsg({
        type: 'success',
        text: `✅ ${data.message}: ${data.documents_processed} docs, ${data.total_chunks} chunks`,
      });
      fetchStatus();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Indexing failed';
      setUploadMsg({ type: 'error', text: `❌ ${msg}` });
    } finally {
      setIndexing(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleUpload(file);
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) handleUpload(file);
  };

  const l = language === 'ta';

  return (
    <div className="card">
      <div className="card-header">
        <span>📄</span>
        <h2>{l ? 'சட்ட ஆவணங்களை பதிவேற்றம்' : 'Upload Legal Documents'}</h2>
      </div>
      <div className="card-body">
        {/* Upload Zone */}
        <div
          className={`upload-zone ${dragging ? 'dragging' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input').click()}
        >
          <div className="upload-icon">📁</div>
          <h3>{l ? 'சட்ட ஆவணங்களை இங்கே இழுக்கவும்' : 'Drag & Drop Legal Documents Here'}</h3>
          <p>{l ? '.txt அல்லது .pdf கோப்புகள் (IPC, CrPC, DV Act, போன்றவை)' : '.txt or .pdf files (IPC, CrPC, DV Act, Consumer Protection Act, etc.)'}</p>
          <input
            id="file-input"
            type="file"
            accept=".txt,.pdf"
            style={{ display: 'none' }}
            onChange={handleFileInput}
          />
        </div>

        {loading && (
          <div style={{ textAlign: 'center', padding: '1rem', color: 'var(--primary)' }}>
            ⏳ {l ? 'பதிவேற்றம் மற்றும் அட்டவணைப்படுத்துதல்...' : 'Uploading and indexing...'}
          </div>
        )}

        {uploadMsg && (
          <div className={`upload-status ${uploadMsg.type}`}>{uploadMsg.text}</div>
        )}

        {/* Index All Button */}
        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          <button className="btn-primary" onClick={handleIndexAll} disabled={indexing}>
            {indexing
              ? l ? '⏳ அட்டவணைப்படுத்துகிறது...' : '⏳ Indexing...'
              : l ? '🔄 அனைத்து ஆவணங்களையும் மீண்டும் அட்டவணைப்படுத்து' : '🔄 Re-index All Documents'}
          </button>
        </div>

        {/* Index Status */}
        {status && (
          <div className="index-status">
            <h3>📊 {l ? 'குறியீட்டு நிலை' : 'Index Status'}</h3>
            <div className="status-grid">
              <div className="status-item">
                <div className="value">{status.total_vectors}</div>
                <div className="label">{l ? 'வெக்டர்கள்' : 'Vectors'}</div>
              </div>
              <div className="status-item">
                <div className="value">{status.documents_on_disk?.length || 0}</div>
                <div className="label">{l ? 'ஆவணங்கள்' : 'Documents'}</div>
              </div>
              <div className="status-item">
                <div className="value">{status.index_loaded ? '✅' : '❌'}</div>
                <div className="label">{l ? 'குறியீடு தயார்' : 'Index Ready'}</div>
              </div>
            </div>
            {status.documents_on_disk?.length > 0 && (
              <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--text-light)' }}>
                <strong>{l ? 'கோப்புகள்' : 'Files'}:</strong> {status.documents_on_disk.join(', ')}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
