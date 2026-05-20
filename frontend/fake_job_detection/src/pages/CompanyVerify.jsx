import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Building2, Globe, Mail, Search, CheckCircle, XCircle,
  AlertTriangle, Shield, Clock, Lock, Calendar, MapPin,
  TrendingUp, Activity, ExternalLink, Linkedin
} from 'lucide-react'
import toast from 'react-hot-toast'
import LoadingAnimation from '../components/LoadingAnimation'
import { verifyCompany } from '../services/api'

export default function CompanyVerify() {
  const [companyName, setCompanyName] = useState('')
  const [website, setWebsite] = useState('')
  const [email, setEmail] = useState('')
  const [sourcePlatform, setSourcePlatform] = useState('')
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const handleVerify = async () => {
    if (!companyName.trim()) {
      toast.error('Please enter a company name')
      return
    }

    setLoading(true)
    setResults(null)

    try {
      const response = await verifyCompany(
        companyName,
        website || null,
        email || null,
        sourcePlatform || null
      )
      setResults(response.data)

      if (response.data.legitimacy_score >= 75) {
        toast.success('Company appears legitimate!')
      } else if (response.data.legitimacy_score >= 50) {
        toast('Exercise caution with this company', { icon: '⚠️' })
      } else {
        toast.error('High risk - company verification failed!')
      }
    } catch (error) {
      toast.error('Verification failed. Please check if the backend server is running.')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-400'
    if (score >= 50) return 'text-yellow-400'
    if (score >= 30) return 'text-orange-400'
    return 'text-red-400'
  }

  const getScoreBg = (score) => {
    if (score >= 75) return 'from-green-500/20 to-green-900/10 border-green-500/30'
    if (score >= 50) return 'from-yellow-500/20 to-yellow-900/10 border-yellow-500/30'
    if (score >= 30) return 'from-orange-500/20 to-orange-900/10 border-orange-500/30'
    return 'from-red-500/20 to-red-900/10 border-red-500/30'
  }

  const getTrustBadge = (level) => {
    const badges = {
      'Safe': { color: 'bg-green-500/10 text-green-400 border-green-500/30', icon: <Shield className="w-4 h-4" /> },
      'Moderate': { color: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30', icon: <AlertTriangle className="w-4 h-4" /> },
      'Suspicious': { color: 'bg-orange-500/10 text-orange-400 border-orange-500/30', icon: <AlertTriangle className="w-4 h-4" /> },
      'High Risk': { color: 'bg-red-500/10 text-red-400 border-red-500/30', icon: <XCircle className="w-4 h-4" /> },
    }
    return badges[level] || badges['Moderate']
  }

  const getStatusIcon = (status) => {
    if (status === 'verified') return <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
    if (status === 'failed') return <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
    if (status === 'warning') return <AlertTriangle className="w-4 h-4 text-yellow-400 flex-shrink-0" />
    if (status === 'unavailable') return <Clock className="w-4 h-4 text-gray-500 flex-shrink-0" />
    return <Shield className="w-4 h-4 text-blue-400 flex-shrink-0" />
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <Building2 className="w-7 h-7 text-blue-400" />
          Company Authenticity Engine
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Multi-signal company verification with domain intelligence, WHOIS analysis, and explainable risk scoring
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Input Form */}
        <div className="lg:col-span-1">
          <div className="glass-card p-6 space-y-4 sticky top-6">
            <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">Company Details</h3>

            <div>
              <label className="text-sm font-medium text-gray-300 mb-1.5 block">
                Company Name *
              </label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="e.g., Tata Consultancy Services"
                className="input-cyber"
                onKeyDown={(e) => e.key === 'Enter' && handleVerify()}
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-300 mb-1.5 block">
                <Globe className="w-3.5 h-3.5 inline mr-1 opacity-70" />
                Website URL
              </label>
              <input
                type="url"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
                placeholder="https://www.company.com"
                className="input-cyber"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-300 mb-1.5 block">
                <Mail className="w-3.5 h-3.5 inline mr-1 opacity-70" />
                Recruiter Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="hr@company.com"
                className="input-cyber"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-300 mb-1.5 block">
                <MapPin className="w-3.5 h-3.5 inline mr-1 opacity-70" />
                Job Source Platform
              </label>
              <input
                type="text"
                value={sourcePlatform}
                onChange={(e) => setSourcePlatform(e.target.value)}
                placeholder="e.g., LinkedIn, Naukri, Telegram"
                className="input-cyber"
              />
            </div>

            <button
              onClick={handleVerify}
              disabled={loading}
              className="btn-cyber w-full text-white flex items-center justify-center gap-2 mt-2"
            >
              {loading ? (
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <Search className="w-4 h-4" />
              )}
              {loading ? 'Analyzing...' : 'Verify Company'}
            </button>
          </div>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2">
          <AnimatePresence mode="wait">
            {loading && (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="glass-card p-12"
              >
                <LoadingAnimation text="Running company authenticity checks..." />
                <div className="mt-4 text-center">
                  <p className="text-xs text-gray-500">Checking DNS, WHOIS, SSL, email domain, and company database...</p>
                </div>
              </motion.div>
            )}

            {!loading && !results && (
              <motion.div
                key="empty"
                className="glass-card p-12 flex flex-col items-center justify-center text-center"
              >
                <div className="w-20 h-20 rounded-full bg-blue-500/10 flex items-center justify-center mb-4">
                  <Building2 className="w-10 h-10 text-blue-400/60" />
                </div>
                <h3 className="text-lg font-semibold text-gray-300">Enter Company Details</h3>
                <p className="text-sm text-gray-500 mt-2 max-w-md">
                  We'll verify through company database, domain WHOIS analysis, SSL certificates,
                  email validation, and pattern detection to generate a comprehensive trust score.
                </p>
                <div className="flex flex-wrap gap-2 mt-4 justify-center">
                  {['Domain Age', 'SSL Check', 'WHOIS', 'Email Match', 'Company DB'].map((tag) => (
                    <span key={tag} className="px-2.5 py-1 text-xs rounded-full bg-gray-800 text-gray-400 border border-gray-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}

            {!loading && results && (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                {/* Score Card */}
                <div className={`glass-card p-6 bg-gradient-to-br ${getScoreBg(results.legitimacy_score)} border`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-400">Legitimacy Score</p>
                      <p className={`text-5xl font-bold mt-1 ${getScoreColor(results.legitimacy_score)}`}>
                        {results.legitimacy_score}
                        <span className="text-lg text-gray-500 font-normal">/100</span>
                      </p>
                      <div className="mt-3">
                        {(() => {
                          const badge = getTrustBadge(results.trust_level)
                          return (
                            <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-semibold border ${badge.color}`}>
                              {badge.icon}
                              {results.trust_level}
                            </span>
                          )
                        })()}
                      </div>
                    </div>
                    <div className="text-right space-y-2">
                      <div>
                        <p className="text-xs text-gray-500">Scam Probability</p>
                        <p className={`text-2xl font-bold ${results.scam_probability > 50 ? 'text-red-400' : 'text-green-400'}`}>
                          {results.scam_probability}%
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Key Metrics */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <MetricCard
                    icon={<Clock className="w-4 h-4 text-blue-400" />}
                    label="Company Age"
                    value={results.company_existence_years ? `${results.company_existence_years} yrs` : 'Unknown'}
                    sub={results.company_founded_year ? `Founded ${results.company_founded_year}` : null}
                  />
                  <MetricCard
                    icon={<Calendar className="w-4 h-4 text-purple-400" />}
                    label="Domain Age"
                    value={results.domain_existence_years ? `${results.domain_existence_years} yrs` : 'Unknown'}
                    sub={results.domain_creation_date || null}
                  />
                  <MetricCard
                    icon={<Lock className="w-4 h-4 text-green-400" />}
                    label="Website Security"
                    value={results.ssl_valid === true ? 'Secure' : results.ssl_valid === false ? 'Insecure' : 'N/A'}
                    sub={results.website_security !== 'Not Checked' ? results.website_security : null}
                  />
                  <MetricCard
                    icon={<Mail className="w-4 h-4 text-yellow-400" />}
                    label="Email Check"
                    value={results.email_authenticity === 'Not Checked' ? 'N/A' :
                      results.email_authenticity.includes('Match') ? 'Valid' :
                      results.email_authenticity.includes('Free') ? 'Risky' : 'Mismatch'}
                    sub={results.email_authenticity !== 'Not Checked' ? results.email_authenticity : null}
                  />
                </div>

                {/* Risk Flags & Trust Signals */}
                <div className="grid sm:grid-cols-2 gap-4">
                  {/* Risk Flags */}
                  <div className="glass-card p-5">
                    <h4 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4" />
                      Risk Indicators ({results.risk_flags.length})
                    </h4>
                    {results.risk_flags.length === 0 ? (
                      <p className="text-sm text-gray-500 italic">No risk indicators detected</p>
                    ) : (
                      <div className="space-y-2 max-h-48 overflow-y-auto">
                        {results.risk_flags.map((flag, i) => (
                          <div key={i} className="flex items-start gap-2 text-sm">
                            <XCircle className="w-3.5 h-3.5 text-red-400 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-300">{flag}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Trust Signals */}
                  <div className="glass-card p-5">
                    <h4 className="text-sm font-semibold text-green-400 mb-3 flex items-center gap-2">
                      <CheckCircle className="w-4 h-4" />
                      Trust Signals ({results.trust_signals.length})
                    </h4>
                    {results.trust_signals.length === 0 ? (
                      <p className="text-sm text-gray-500 italic">No trust signals detected</p>
                    ) : (
                      <div className="space-y-2 max-h-48 overflow-y-auto">
                        {results.trust_signals.map((signal, i) => (
                          <div key={i} className="flex items-start gap-2 text-sm">
                            <CheckCircle className="w-3.5 h-3.5 text-green-400 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-300">{signal}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>

                {/* Verification Checks */}
                <div className="glass-card p-5">
                  <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                    <Activity className="w-4 h-4 text-blue-400" />
                    Verification Checks ({results.checks_performed.length})
                  </h4>
                  <div className="space-y-2">
                    {results.checks_performed.map((check, i) => (
                      <div key={i} className="flex items-start gap-3 p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/50">
                        {getStatusIcon(check.status)}
                        <div className="min-w-0 flex-1">
                          <p className="text-sm font-medium text-white">{check.check}</p>
                          <p className="text-xs text-gray-500 mt-0.5 break-words">{check.detail}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Summary & Recommendation */}
                <div className="glass-card p-5">
                  <h4 className="text-sm font-semibold text-white mb-2">Analysis Summary</h4>
                  <p className="text-sm text-gray-300 leading-relaxed">{results.analysis_summary}</p>
                  <div className={`mt-4 p-3 rounded-lg border ${
                    results.legitimacy_score >= 75 ? 'bg-green-500/5 border-green-500/20' :
                    results.legitimacy_score >= 50 ? 'bg-yellow-500/5 border-yellow-500/20' :
                    'bg-red-500/5 border-red-500/20'
                  }`}>
                    <p className="text-sm font-medium text-gray-200">
                      <Shield className="w-4 h-4 inline mr-1.5" />
                      Recommendation
                    </p>
                    <p className="text-sm text-gray-400 mt-1">{results.recommendation}</p>
                  </div>
                </div>

                {/* Domain Registrar Info */}
                {results.domain_registrar && (
                  <div className="glass-card p-4">
                    <p className="text-xs text-gray-500">
                      <Globe className="w-3 h-3 inline mr-1" />
                      Domain Registrar: <span className="text-gray-400">{results.domain_registrar}</span>
                    </p>
                  </div>
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}

// ─── Sub-components ─────────────────────────────────────────────────────────

function MetricCard({ icon, label, value, sub }) {
  return (
    <div className="glass-card p-3.5 text-center">
      <div className="flex justify-center mb-1.5">{icon}</div>
      <p className="text-xs text-gray-500">{label}</p>
      <p className="text-lg font-bold text-white mt-0.5">{value}</p>
      {sub && <p className="text-xs text-gray-500 mt-0.5 truncate">{sub}</p>}
    </div>
  )
}
