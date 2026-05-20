import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Globe, Search, AlertTriangle, CheckCircle, XCircle,
  Loader2, ExternalLink, Shield, Zap, Filter
} from 'lucide-react'
import toast from 'react-hot-toast'
import ThreatBadge from '../components/ThreatBadge'
import { scrapeJobs } from '../services/api'

const PLATFORMS = [
  { id: 'all', name: 'All Platforms', icon: '🌐' },
  { id: 'indeed', name: 'Indeed India', icon: '🔍' },
  { id: 'internshala', name: 'Internshala', icon: '🎓' },
  { id: 'linkedin', name: 'LinkedIn', icon: '💼' },
]

const SAMPLE_QUERIES = [
  'work from home',
  'data entry',
  'part time jobs',
  'earn money online',
  'captcha typing',
  'customer support',
  'content writing',
  'digital marketing',
]

export default function LiveScraping() {
  const [query, setQuery] = useState('')
  const [platform, setPlatform] = useState('all')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const handleScrape = async () => {
    if (!query.trim()) {
      toast.error('Please enter a search query')
      return
    }

    setLoading(true)
    setResults(null)

    try {
      const response = await scrapeJobs(query, platform, 10)
      setResults(response.data)

      const scams = response.data.summary.scams_detected
      if (scams > 0) {
        toast.error(`⚠️ ${scams} suspicious job(s) detected!`)
      } else {
        toast.success('Scan complete - no obvious scams found')
      }
    } catch (error) {
      toast.error('Scraping failed. Make sure the backend server is running.')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <Globe className="w-7 h-7 text-blue-400" />
          Real-Time Job Scraping & Analysis
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Fetch live job postings from platforms and analyze them for scam indicators in real-time
        </p>
      </div>

      {/* Search Panel */}
      <div className="glass-card p-6">
        <div className="grid md:grid-cols-3 gap-4">
          {/* Query Input */}
          <div className="md:col-span-2">
            <label className="text-sm font-medium text-gray-300 mb-2 block">Search Query</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleScrape()}
                placeholder="e.g., work from home, data entry, earn money online..."
                className="input-cyber pl-11"
              />
            </div>
            {/* Quick Queries */}
            <div className="flex flex-wrap gap-2 mt-3">
              {SAMPLE_QUERIES.map((q) => (
                <button
                  key={q}
                  onClick={() => setQuery(q)}
                  className="text-xs px-3 py-1.5 rounded-full bg-gray-800/50 border border-gray-700 text-gray-400 hover:border-blue-500/50 hover:text-white transition-all"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>

          {/* Platform Selection */}
          <div>
            <label className="text-sm font-medium text-gray-300 mb-2 block">Platform</label>
            <div className="space-y-2">
              {PLATFORMS.map((p) => (
                <button
                  key={p.id}
                  onClick={() => setPlatform(p.id)}
                  className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all ${
                    platform === p.id
                      ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                      : 'text-gray-400 hover:text-white bg-gray-800/30 border border-gray-700'
                  }`}
                >
                  <span>{p.icon}</span>
                  {p.name}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Scrape Button */}
        <button
          onClick={handleScrape}
          disabled={loading}
          className="btn-cyber w-full mt-5 text-white flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Scraping & Analyzing Live Jobs...
            </>
          ) : (
            <>
              <Zap className="w-5 h-5" />
              Scrape & Analyze Live Jobs
            </>
          )}
        </button>
      </div>

      {/* Loading State */}
      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card p-8 text-center"
        >
          <div className="flex flex-col items-center">
            <Loader2 className="w-12 h-12 text-blue-400 animate-spin mb-4" />
            <p className="text-white font-medium">Scraping live job postings...</p>
            <p className="text-sm text-gray-400 mt-1">
              Fetching from {platform === 'all' ? 'Indeed, Internshala & LinkedIn' : platform}
            </p>
            <div className="flex gap-1 mt-4">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  className="w-2 h-2 rounded-full bg-blue-500"
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
                />
              ))}
            </div>
          </div>
        </motion.div>
      )}

      {/* Results */}
      <AnimatePresence>
        {results && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            {/* Summary Cards */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="glass-card p-4 text-center">
                <p className="text-2xl font-bold text-white">{results.summary.total_scraped}</p>
                <p className="text-xs text-gray-400">Jobs Scraped</p>
              </div>
              <div className="glass-card p-4 text-center">
                <p className="text-2xl font-bold text-blue-400">{results.summary.total_analyzed}</p>
                <p className="text-xs text-gray-400">Analyzed</p>
              </div>
              <div className="glass-card p-4 text-center">
                <p className="text-2xl font-bold text-red-400">{results.summary.scams_detected}</p>
                <p className="text-xs text-gray-400">Scams Found</p>
              </div>
              <div className="glass-card p-4 text-center">
                <p className="text-2xl font-bold text-green-400">{results.summary.safe_jobs}</p>
                <p className="text-xs text-gray-400">Safe Jobs</p>
              </div>
              <div className="glass-card p-4 text-center">
                <p className="text-2xl font-bold text-yellow-400">{results.summary.scam_rate}%</p>
                <p className="text-xs text-gray-400">Scam Rate</p>
              </div>
            </div>

            {/* Job Results List */}
            <div className="space-y-3">
              <h3 className="text-lg font-semibold text-white flex items-center gap-2">
                <Filter className="w-5 h-5 text-blue-400" />
                Scraped Jobs (sorted by risk)
              </h3>

              {results.jobs.length === 0 && (
                <div className="glass-card p-8 text-center">
                  <Globe className="w-12 h-12 text-gray-600 mx-auto mb-3" />
                  <p className="text-gray-400">No jobs found for this query. Try a different search term.</p>
                </div>
              )}

              {results.jobs.map((job, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 * i }}
                  className={`glass-card p-5 border-l-4 ${
                    job.risk_score > 60 ? 'border-l-red-500' :
                    job.risk_score > 30 ? 'border-l-yellow-500' : 'border-l-green-500'
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    {/* Job Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="text-white font-semibold truncate">{job.title}</h4>
                        {job.url && (
                          <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">
                            <ExternalLink className="w-4 h-4" />
                          </a>
                        )}
                      </div>
                      <p className="text-sm text-gray-400">{job.company} • {job.location}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        💰 {job.salary} • 📍 {job.platform}
                      </p>

                      {/* Reasons */}
                      {job.top_reasons && job.top_reasons.length > 0 && (
                        <div className="mt-3 space-y-1">
                          {job.top_reasons.map((reason, ri) => (
                            <div key={ri} className="flex items-start gap-2 text-xs text-gray-400">
                              {job.risk_score > 50 ? (
                                <XCircle className="w-3 h-3 text-red-400 mt-0.5 shrink-0" />
                              ) : (
                                <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 shrink-0" />
                              )}
                              <span>{reason}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    {/* Risk Score */}
                    <div className="text-center shrink-0">
                      <div className={`text-3xl font-bold ${
                        job.risk_score > 60 ? 'text-red-400' :
                        job.risk_score > 30 ? 'text-yellow-400' : 'text-green-400'
                      }`}>
                        {job.risk_score}
                      </div>
                      <p className="text-xs text-gray-500">Risk</p>
                      <div className="mt-2">
                        <ThreatBadge level={job.risk_level} />
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Errors */}
            {results.errors && results.errors.length > 0 && (
              <div className="glass-card p-4">
                <h4 className="text-sm font-semibold text-yellow-400 mb-2 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4" />
                  Platform Notices
                </h4>
                {results.errors.map((err, i) => (
                  <p key={i} className="text-xs text-gray-400">
                    {err.platform}: {err.error}
                  </p>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
