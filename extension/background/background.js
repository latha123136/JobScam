/**
 * ScamShield AI - Background Service Worker
 * Handles extension lifecycle and communication
 */

// Listen for installation
chrome.runtime.onInstalled.addListener(() => {
  console.log('ScamShield AI extension installed');
  
  // Set default settings
  chrome.storage.local.set({
    autoScan: true,
    apiUrl: 'https://YOUR_RENDER_URL/api',
    scanCount: 0,
    scamsDetected: 0
  });
});

// Listen for messages from content scripts or popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'SCAN_RESULT') {
    // Update scan statistics
    chrome.storage.local.get(['scanCount', 'scamsDetected'], (data) => {
      const newCount = (data.scanCount || 0) + 1;
      const newScams = (data.scamsDetected || 0) + (message.isScam ? 1 : 0);
      chrome.storage.local.set({ scanCount: newCount, scamsDetected: newScams });
    });
  }

  if (message.type === 'GET_STATS') {
    chrome.storage.local.get(['scanCount', 'scamsDetected'], (data) => {
      sendResponse(data);
    });
    return true; // Keep message channel open for async response
  }
});
