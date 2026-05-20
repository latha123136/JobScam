import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// API Functions
export const predictScam = (text, url = null, email = null) =>
  api.post('/predict', { text, url, email })

export const quickScan = (text) =>
  api.post('/quick-scan', { text, source: 'web' })

export const analyzeUrl = (url) =>
  api.post('/analyze-url', { url })

export const analyzeEmail = (email) =>
  api.post('/analyze-email', { email })

export const verifyCompany = (company_name, website = null, email = null, source_platform = null) =>
  api.post('/verify-company', { company_name, website, email, source_platform })

export const analyzeImage = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/analyze-image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const sendChatMessage = (message) =>
  api.post('/chatbot', { message })

export const getChatSuggestions = () =>
  api.get('/chatbot/suggestions')

export const getHistory = (limit = 20, skip = 0) =>
  api.get(`/history?limit=${limit}&skip=${skip}`)

export const getAnalytics = () =>
  api.get('/analytics/full')

export const getAnalyticsOverview = () =>
  api.get('/analytics/overview')

export const scrapeJobs = (query, platform = 'all', max_results = 5) =>
  api.post('/scrape-jobs', { query, platform, max_results })

export const getSupportedPlatforms = () =>
  api.get('/scrape-jobs/platforms')

export const submitFeedback = (data) =>
  api.post('/feedback', data)

export const reportScam = (data) =>
  api.post('/report-scam', data)

// Auth
export const login = (email, password) =>
  api.post('/auth/login', { email, password })

export const register = (name, email, password) =>
  api.post('/auth/register', { name, email, password })

export const getProfile = () =>
  api.get('/auth/profile')

export default api
