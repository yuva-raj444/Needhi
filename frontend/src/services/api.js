/**
 * NyayaSahaya — API service layer.
 * All backend HTTP calls in one place.
 */

import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000, // 60s for LLM calls
  headers: { 'Content-Type': 'application/json' },
});

/* ── RAG Q&A ───────────────────────────────────────────────── */
export async function askQuestion(question, language = null) {
  const { data } = await api.post('/api/query/', { question, language });
  return data;
}

/* ── Classifier ────────────────────────────────────────────── */
export async function classifyIssue(description) {
  const { data } = await api.post('/api/classify/', { description });
  return data;
}

/* ── Complaint Draft ───────────────────────────────────────── */
export async function generateComplaint(formData) {
  const { data } = await api.post('/api/complaint/draft', formData);
  return data;
}

/* ── Complaint PDF ─────────────────────────────────────────── */
export async function downloadComplaintPDF(formData) {
  const response = await api.post('/api/complaint/pdf', formData, {
    responseType: 'blob',
  });
  // Trigger download
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `complaint_${formData.complainant_name.replace(/\s+/g, '_')}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

/* ── Document Upload ───────────────────────────────────────── */
export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append('file', file);
  const { data } = await api.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  });
  return data;
}

export async function indexAllDocuments() {
  const { data } = await api.post('/api/documents/index-all');
  return data;
}

export async function getIndexStatus() {
  const { data } = await api.get('/api/documents/status');
  return data;
}

/* ── Health ─────────────────────────────────────────────────── */
export async function checkHealth() {
  const { data } = await api.get('/health');
  return data;
}

export default api;
