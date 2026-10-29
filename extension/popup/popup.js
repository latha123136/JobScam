const API_URL = 'https://YOUR_RENDER_URL/api';

// DOM Elements
const scanBtn = document.getElementById('scanBtn');
const scanPageBtn = document.getElementById('scanPageBtn');
const jobTextArea = document.getElementById('jobText');
const resultsDiv = document.getElementById('results');
const loadingDiv = document.getElementById('loading');
const riskScore = document.getElementById('riskScore');
const riskLabel = document.getElementById('riskLabel');
const riskLevel = document.getElementById('riskLevel');
const reasonsDiv = document.getElementById('reasons');

// Scan text input
scanBtn.addEventListener('click', async () => {
  const text = jobTextArea.value.trim();
  if (!text) {
    alert('Please paste a job description or message to analyze.');
    return;
  }
  await analyzeText(text);
});

// Scan current page
scanPageBtn.addEventListener('click', async () => {
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: extractPageContent
    });
    
    if (results && results[0] && results[0].result) {
      const pageText = results[0].result;
      jobTextArea.value = pageText.substring(0, 2000);
      await analyzeText(pageText);
    } else {
      alert('Could not extract content from this page.');
    }
  } catch (error) {
    alert('Cannot scan this page. Try pasting the job description manually.');
  }
});

// Extract page content
function extractPageContent() {
  // Try to find job description content
  const selectors = [
    '.jobs-description__content',           // LinkedIn
    '.detail_job_description',              // Internshala
    '.job-desc',                            // Naukri
    '.jobsearch-jobDescriptionText',        // Indeed
    '[data-testid="job-description"]',      // Generic
    '.job-description',                     // Generic
    'article',                              // Generic
    'main'                                  // Fallback
  ];

  for (const selector of selectors) {
    const el = document.querySelector(selector);
    if (el && el.innerText.trim().length > 50) {
      return el.innerText.trim();
    }
  }

  // Fallback: get body text
  return document.body.innerText.substring(0, 3000);
}

// Analyze text via API
async function analyzeText(text) {
  showLoading();
  
  try {
    const response = await fetch(`${API_URL}/quick-scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, source: 'extension' })
    });

    if (!response.ok) throw new Error('API error');
    
    const data = await response.json();
    displayResults(data);
  } catch (error) {
    // Fallback: local analysis
    const localResult = localAnalysis(text);
    displayResults(localResult);
  }
}

// Local fallback analysis (when API is unavailable)
function localAnalysis(text) {
  const textLower = text.toLowerCase();
  let score = 20;
  const reasons = [];

  // Scam phrase detection
  const scamPhrases = [
    'registration fee', 'pay fee', 'security deposit', 'training fee',
    'earn lakh', 'earn per month', 'no interview', 'instant joining',
    'guaranteed placement', 'captcha typing', 'work from home earn',
    'whatsapp interview', 'telegram job', 'no experience required earn'
  ];

  scamPhrases.forEach(phrase => {
    if (textLower.includes(phrase)) {
      score += 15;
      reasons.push(`Contains scam phrase: "${phrase}"`);
    }
  });

  // Urgency detection
  const urgencyPhrases = ['limited seats', 'hurry up', 'last date today', 'immediate joining', 'act now'];
  urgencyPhrases.forEach(phrase => {
    if (textLower.includes(phrase)) {
      score += 10;
      reasons.push(`Urgency tactic: "${phrase}"`);
    }
  });

  // Free email detection
  if (textLower.match(/hr.*@gmail|hr.*@yahoo|recruit.*@gmail/)) {
    score += 20;
    reasons.push('Recruiter using free email provider');
  }

  // Payment request
  if (textLower.match(/pay|fee|deposit/) && textLower.match(/register|join|apply/)) {
    score += 25;
    reasons.push('Payment requested from candidate');
  }

  score = Math.min(score, 100);

  let riskLevel;
  if (score <= 20) riskLevel = 'Safe';
  else if (score <= 40) riskLevel = 'Low Risk';
  else if (score <= 60) riskLevel = 'Medium Risk';
  else if (score <= 80) riskLevel = 'High Risk';
  else riskLevel = 'Critical Scam';

  if (reasons.length === 0) {
    reasons.push('No significant scam indicators detected');
  }

  return {
    risk_score: score,
    risk_level: riskLevel,
    confidence: Math.min(reasons.length * 20, 95),
    top_reasons: reasons.slice(0, 5),
    is_scam: score > 60
  };
}

// Display results
function displayResults(data) {
  hideLoading();
  resultsDiv.classList.remove('hidden');

  const score = data.risk_score;
  riskScore.textContent = score;
  riskLabel.textContent = 'Risk Score';

  // Color based on score
  let color, badgeClass;
  if (score <= 20) { color = '#10b981'; badgeClass = 'risk-safe'; }
  else if (score <= 40) { color = '#3b82f6'; badgeClass = 'risk-low'; }
  else if (score <= 60) { color = '#f59e0b'; badgeClass = 'risk-medium'; }
  else if (score <= 80) { color = '#f97316'; badgeClass = 'risk-high'; }
  else { color = '#ef4444'; badgeClass = 'risk-critical'; }

  riskScore.style.color = color;
  riskLevel.className = `risk-badge ${badgeClass}`;
  riskLevel.textContent = data.risk_level;

  // Display reasons
  reasonsDiv.innerHTML = '';
  const reasons = data.top_reasons || data.explanation || [];
  reasons.forEach(reason => {
    const item = document.createElement('div');
    item.className = 'reason-item';
    item.innerHTML = `
      <span class="reason-icon">${score > 50 ? '⚠️' : '✅'}</span>
      <span>${reason}</span>
    `;
    reasonsDiv.appendChild(item);
  });
}

function showLoading() {
  resultsDiv.classList.add('hidden');
  loadingDiv.classList.remove('hidden');
}

function hideLoading() {
  loadingDiv.classList.add('hidden');
}
