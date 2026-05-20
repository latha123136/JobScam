/**
 * ScamShield AI - Content Script
 * Automatically detects job pages and provides scam warnings
 */

const API_URL = 'http://localhost:8000/api';

// Auto-detect job pages and show warning badge
(function() {
  // Check if we're on a job page
  const isJobPage = detectJobPage();
  if (!isJobPage) return;

  // Extract job content
  const jobContent = extractJobContent();
  if (!jobContent || jobContent.length < 50) return;

  // Analyze the job
  analyzeJob(jobContent);
})();

function detectJobPage() {
  const url = window.location.href;
  const jobPatterns = [
    /linkedin\.com\/jobs/,
    /internshala\.com\/(internship|job)/,
    /naukri\.com\/job-listings/,
    /indeed\.com\/viewjob/,
    /glassdoor\.com\/job-listing/
  ];
  return jobPatterns.some(pattern => pattern.test(url));
}

function extractJobContent() {
  const selectors = [
    '.jobs-description__content',
    '.detail_job_description',
    '.job-desc',
    '.jobsearch-jobDescriptionText',
    '.job-description',
    '[data-testid="job-description"]',
    'article'
  ];

  for (const selector of selectors) {
    const el = document.querySelector(selector);
    if (el && el.innerText.trim().length > 50) {
      return el.innerText.trim();
    }
  }
  return null;
}

async function analyzeJob(text) {
  try {
    const response = await fetch(`${API_URL}/quick-scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text.substring(0, 3000), source: 'extension' })
    });

    if (!response.ok) return;
    const data = await response.json();

    if (data.risk_score > 50) {
      showWarningBadge(data);
    }
  } catch (error) {
    // Silently fail - don't disrupt user experience
    console.log('ScamShield: API unavailable, using local analysis');
  }
}

function showWarningBadge(data) {
  // Create warning overlay
  const badge = document.createElement('div');
  badge.id = 'scamshield-warning';
  badge.innerHTML = `
    <div style="
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 99999;
      background: #1e1e2e;
      border: 1px solid ${data.risk_score > 70 ? '#ef4444' : '#f59e0b'};
      border-radius: 12px;
      padding: 16px;
      max-width: 320px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      font-family: system-ui, sans-serif;
      color: #e2e8f0;
    ">
      <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
        <span style="font-size: 20px;">🛡️</span>
        <strong style="font-size: 14px;">ScamShield AI Warning</strong>
        <button onclick="this.closest('#scamshield-warning').remove()" style="
          margin-left: auto; background: none; border: none; color: #64748b; 
          cursor: pointer; font-size: 18px; line-height: 1;
        ">×</button>
      </div>
      <div style="
        text-align: center; padding: 10px; border-radius: 8px;
        background: ${data.risk_score > 70 ? 'rgba(239,68,68,0.1)' : 'rgba(245,158,11,0.1)'};
        margin-bottom: 10px;
      ">
        <div style="font-size: 28px; font-weight: 800; color: ${data.risk_score > 70 ? '#ef4444' : '#f59e0b'};">
          ${data.risk_score}%
        </div>
        <div style="font-size: 11px; color: #94a3b8;">Scam Risk Score</div>
      </div>
      <div style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">
        <strong style="color: ${data.risk_score > 70 ? '#ef4444' : '#f59e0b'};">${data.risk_level}</strong>
      </div>
      <div style="font-size: 11px; color: #64748b;">
        ${data.top_reasons ? data.top_reasons.slice(0, 2).join(' • ') : 'Suspicious patterns detected'}
      </div>
    </div>
  `;

  document.body.appendChild(badge);

  // Auto-dismiss after 15 seconds
  setTimeout(() => {
    const el = document.getElementById('scamshield-warning');
    if (el) el.remove();
  }, 15000);
}
