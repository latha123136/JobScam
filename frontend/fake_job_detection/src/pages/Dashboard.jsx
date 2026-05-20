import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Shield, Send, Link, Mail, Upload, AlertTriangle,
  CheckCircle, XCircle, Info, Zap, FileText, Image
} from 'lucide-react'
import toast from 'react-hot-toast'
import RiskMeter from '../components/RiskMeter'
import ThreatBadge from '../components/ThreatBadge'
import LoadingAnimation from '../components/LoadingAnimation'
import { predictScam, analyzeUrl, analyzeEmail, analyzeImage } from '../services/api'

export default function Dashboard() {
  const [jobText, setJobText] = useState('')
  const [jobUrl, setJobUrl] = useState('')
  const [recruiterEmail, setRecruiterEmail] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [activeTab, setActiveTab] = useState('text')

  const handleAnalyze = async () => {
    if (!jobText && !jobUrl && !recruiterEmail && !imageFile) {
      toast.error('Please provide at least one input for analysis')
      return
    }

    setLoading(true)
    setResults(null)

    try {
      // Primary text analysis
      let mainResult = null
      if (jobText) {
        const response = await predictScam(jobText, jobUrl, recruiterEmail)
        mainResult = response.data
      }

      // URL analysis
      let urlResult = null
      if (jobUrl) {
        try {
          const urlResponse = await analyzeUrl(jobUrl)
          urlResult = urlResponse.data
        } catch (e) { /* URL analysis optional */ }
      }

      // Email analysis
      let emailResult = null
      if (recruiterEmail) {
        try {
          const emailResponse = await analyzeEmail(recruiterEmail)
          emailResult = emailResponse.data
        } catch (e) { /* Email analysis optional */ }
      }

      // Image analysis
      let imageResult = null
      if (imageFile) {
        try {
          const imageResponse = await analyzeImage(imageFile)
          imageResult = imageResponse.data
        } catch (e) { /* Image analysis optional */ }
      }

      setResults({ main: mainResult, url: urlResult, email: emailResult, image: imageResult })
      
      if (mainResult?.risk_score > 60) {
        toast.error('⚠️ High scam risk detected!')
      } else if (mainResult?.risk_score > 30) {
        toast('⚡ Moderate risk - exercise caution', { icon: '⚠️' })
      } else if (imageResult) {
        if (imageResult.trust_score < 40) {
          toast.error('⚠️ Image appears suspicious!')
        } else {
          toast.success('Image analysis complete')
        }
      } else {
        toast.success('✅ This job appears safe')
      }
    } catch (error) {
      toast.error('Analysis failed. Please check if the backend server is running.')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Shield className="w-7 h-7 text-blue-400" />
            Scam Detection Engine
          </h1>
          <p className="text-gray-400 text-sm mt-1">Multi-modal AI analysis for job fraud detection</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/20">
          <Zap className="w-4 h-4 text-green-400" />
          <span className="text-xs text-green-400 font-medium">All Systems Active</span>
        </div>
      </div>

      <div className="grid lg:grid-cols-5 gap-6">
        {/* Input Panel */}
        <div className="lg:col-span-3 space-y-4">
          {/* Tabs */}
          <div className="glass-card p-1 flex gap-1">
            {[
              { id: 'text', icon: FileText, label: 'Job Text' },
              { id: 'url', icon: Link, label: 'URL' },
              { id: 'email', icon: Mail, label: 'Email' },
              { id: 'image', icon: Image, label: 'Image/Logo' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  activeTab === tab.id
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                {tab.label}
              </button>
            ))}
          </div>

          {/* Input Area */}
          <div className="glass-card p-6">
            {activeTab === 'text' && (
              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">
                  Paste Job Description
                </label>
                <textarea
                  value={jobText}
                  onChange={(e) => setJobText(e.target.value)}
                  placeholder="Paste the complete job posting, offer letter content, or recruiter message here..."
                  className="input-cyber h-48 resize-none"
                />
                <p className="text-xs text-gray-500 mt-2">
                  Tip: Include salary, requirements, and company details for better analysis
                </p>
              </div>
            )}

            {activeTab === 'url' && (
              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">
                  Job Posting URL
                </label>
                <input
                  type="url"
                  value={jobUrl}
                  onChange={(e) => setJobUrl(e.target.value)}
                  placeholder="https://example.com/job-posting"
                  className="input-cyber"
                />
                <p className="text-xs text-gray-500 mt-2">
                  Supports: LinkedIn, Internshala, Naukri, Indeed, and any website
                </p>
              </div>
            )}

            {activeTab === 'email' && (
              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">
                  Recruiter Email Address
                </label>
                <input
                  type="email"
                  value={recruiterEmail}
                  onChange={(e) => setRecruiterEmail(e.target.value)}
                  placeholder="hr.company@example.com"
                  className="input-cyber"
                />
                <p className="text-xs text-gray-500 mt-2">
                  We'll check for fake domains, free providers, and spoofing patterns
                </p>
              </div>
            )}

            {activeTab === 'image' && (
              <div>
                <label className="text-sm font-medium text-gray-300 mb-2 block">
                  Upload Company Logo / Offer Letter / Recruitment Poster
                </label>
                <div className="border-2 border-dashed border-gray-700 rounded-lg p-8 text-center hover:border-blue-500/50 transition-colors">
                  <Upload className="w-10 h-10 text-gray-500 mx-auto mb-3" />
                  <p className="text-sm text-gray-400 mb-2">
                    {imageFile ? imageFile.name : 'Drag & drop or click to upload'}
                  </p>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => setImageFile(e.target.files[0])}
                    className="w-full opacity-0 absolute inset-0 cursor-pointer"
                    style={{ position: 'relative', opacity: 1, marginTop: '8px' }}
                  />
                  <p className="text-xs text-gray-500 mt-2">
                    Supports: JPEG, PNG, WebP (max 10MB)
                  </p>
                </div>
                {imageFile && (
                  <div className="mt-3 p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center gap-2">
                    <Image className="w-4 h-4 text-blue-400" />
                    <span className="text-sm text-blue-300">{imageFile.name}</span>
                    <button onClick={() => setImageFile(null)} className="ml-auto text-gray-400 hover:text-red-400">
                      <XCircle className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="btn-cyber w-full mt-4 text-white flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>Analyzing...</>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  Run AI Analysis
                </>
              )}
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
                className="glass-card p-8"
              >
                <LoadingAnimation text="AI Engine Processing..." />
              </motion.div>
            )}

            {!loading && !results && (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="glass-card p-8 text-center"
              >
                <Shield className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-400">Ready to Analyze</h3>
                <p className="text-sm text-gray-500 mt-2">
                  Enter a job description, URL, or email to start the AI analysis
                </p>
              </motion.div>
            )}

            {!loading && results?.main && (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                {/* Risk Score */}
                <div className="glass-card p-6 text-center">
                  <RiskMeter score={results.main.risk_score} />
                  <div className="mt-4">
                    <ThreatBadge level={results.main.risk_level} />
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    Confidence: {results.main.confidence}%
                  </p>
                </div>

                {/* Explanation */}
                <div className="glass-card p-5">
                  <h4 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                    <Info className="w-4 h-4 text-blue-400" />
                    AI Explanation — Why is this job Real/Fake?
                  </h4>
                  <div className="space-y-2">
                    {results.main.explanation.map((reason, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm p-2 rounded-lg bg-gray-900/30">
                        <span className="text-gray-300">{reason}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Red Flags */}
                {results.main.red_flags.length > 0 && (
                  <div className="glass-card p-5">
                    <h4 className="text-sm font-semibold text-red-400 mb-3 flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4" />
                      Red Flags Detected
                    </h4>
                    <div className="space-y-2">
                      {results.main.red_flags.map((flag, i) => (
                        <div key={i} className="flex items-start gap-2 text-sm text-gray-300">
                          <span className="text-red-400">•</span>
                          {flag}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Score Breakdown */}
                <div className="glass-card p-5">
                  <h4 className="text-sm font-semibold text-white mb-3">Score Breakdown</h4>
                  <div className="space-y-3">
                    {[
                      { label: 'ML Model', score: results.main.ml_confidence, color: 'blue' },
                      { label: 'Scam Phrases', score: results.main.scam_phrase_score, color: 'red' },
                      { label: 'Urgency Tactics', score: results.main.urgency_score, color: 'orange' },
                      { label: 'Salary Risk', score: results.main.salary_risk_score, color: 'yellow' },
                      { label: 'Behavioral', score: results.main.behavioral_score, color: 'purple' },
                    ].map((item, i) => (
                      <div key={i}>
                        <div className="flex justify-between text-xs mb-1">
                          <span className="text-gray-400">{item.label}</span>
                          <span className="text-gray-300">{item.score}%</span>
                        </div>
                        <div className="w-full bg-gray-800 rounded-full h-1.5">
                          <motion.div
                            className={`h-1.5 rounded-full bg-${item.color}-500`}
                            initial={{ width: 0 }}
                            animate={{ width: `${item.score}%` }}
                            transition={{ duration: 1, delay: 0.1 * i }}
                            style={{ backgroundColor: `var(--tw-${item.color}-500, #3b82f6)` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* Image Analysis Results */}
            {!loading && results?.image && !results?.main && (
              <motion.div
                key="image-results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                <div className="glass-card p-6 text-center">
                  <p className="text-sm text-gray-400 mb-2">Image Trust Score</p>
                  <p className={`text-5xl font-bold ${
                    results.image.trust_score >= 70 ? 'text-green-400' :
                    results.image.trust_score >= 40 ? 'text-yellow-400' : 'text-red-400'
                  }`}>
                    {results.image.trust_score}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">/100</p>
                  <div className={`mt-3 inline-block px-4 py-1.5 rounded-full text-sm font-semibold ${
                    results.image.trust_score >= 70 ? 'bg-green-500/10 text-green-400' :
                    results.image.trust_score >= 40 ? 'bg-yellow-500/10 text-yellow-400' :
                    'bg-red-500/10 text-red-400'
                  }`}>
                    {results.image.verdict}
                  </div>
                </div>

                <div className="glass-card p-5">
                  <h4 className="text-sm font-semibold text-white mb-3">Image Details</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span className="text-gray-400">File</span><span className="text-white">{results.image.filename}</span></div>
                    <div className="flex justify-between"><span className="text-gray-400">Dimensions</span><span className="text-white">{results.image.dimensions}</span></div>
                    <div className="flex justify-between"><span className="text-gray-400">Format</span><span className="text-white">{results.image.format}</span></div>
                    <div className="flex justify-between"><span className="text-gray-400">Size</span><span className="text-white">{results.image.file_size_kb} KB</span></div>
                  </div>
                </div>

                {results.image.risk_indicators.length > 0 && (
                  <div className="glass-card p-5">
                    <h4 className="text-sm font-semibold text-red-400 mb-3">Risk Indicators</h4>
                    {results.image.risk_indicators.map((r, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm text-gray-300 mb-1">
                        <XCircle className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
                        {r}
                      </div>
                    ))}
                  </div>
                )}

                {results.image.trust_indicators.length > 0 && (
                  <div className="glass-card p-5">
                    <h4 className="text-sm font-semibold text-green-400 mb-3">Trust Indicators</h4>
                    {results.image.trust_indicators.map((t, i) => (
                      <div key={i} className="flex items-start gap-2 text-sm text-gray-300 mb-1">
                        <CheckCircle className="w-4 h-4 text-green-400 mt-0.5 shrink-0" />
                        {t}
                      </div>
                    ))}
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
