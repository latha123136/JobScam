import { useState } from 'react'
import { motion } from 'framer-motion'
import { History as HistoryIcon, Search, Filter, Shield, AlertTriangle, CheckCircle } from 'lucide-react'
import ThreatBadge from '../components/ThreatBadge'

// Mock history data
const mockHistory = [
  { id: 1, text: "Software Developer at TechCorp...", risk_score: 15, risk_level: "Safe", source: "LinkedIn", date: "2024-12-15 14:30" },
  { id: 2, text: "Earn ₹1 lakh per month from home...", risk_score: 92, risk_level: "Critical Scam", source: "WhatsApp", date: "2024-12-15 12:15" },
  { id: 3, text: "Data Entry Operator - No experience...", risk_score: 78, risk_level: "High Risk", source: "Telegram", date: "2024-12-14 18:45" },
  { id: 4, text: "Full Stack Developer at Infosys...", risk_score: 8, risk_level: "Safe", source: "Naukri", date: "2024-12-14 10:20" },
  { id: 5, text: "Pay ₹999 registration fee for placement...", risk_score: 95, risk_level: "Critical Scam", source: "Email", date: "2024-12-13 16:00" },
  { id: 6, text: "Marketing Intern at StartupXYZ...", risk_score: 35, risk_level: "Low Risk", source: "Internshala", date: "2024-12-13 09:30" },
  { id: 7, text: "Captcha typing job - earn ₹500 daily...", risk_score: 88, risk_level: "Critical Scam", source: "Telegram", date: "2024-12-12 20:10" },
  { id: 8, text: "Senior Analyst at Deloitte...", risk_score: 12, risk_level: "Safe", source: "LinkedIn", date: "2024-12-12 11:45" },
]

export default function History() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterLevel, setFilterLevel] = useState('all')

  const filteredHistory = mockHistory.filter(item => {
    const matchesSearch = item.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          item.source.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterLevel === 'all' || item.risk_level === filterLevel
    return matchesSearch && matchesFilter
  })

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <HistoryIcon className="w-7 h-7 text-blue-400" />
            Scan History
          </h1>
          <p className="text-gray-400 text-sm mt-1">View all previous scam analysis results</p>
        </div>
        <div className="text-sm text-gray-400">
          {filteredHistory.length} scans found
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card p-4 flex flex-col md:flex-row gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search scans..."
            className="input-cyber pl-10"
          />
        </div>
        <div className="flex gap-2">
          {['all', 'Safe', 'Low Risk', 'High Risk', 'Critical Scam'].map((level) => (
            <button
              key={level}
              onClick={() => setFilterLevel(level)}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                filterLevel === level
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : 'text-gray-400 hover:text-white bg-gray-800/50'
              }`}
            >
              {level === 'all' ? 'All' : level}
            </button>
          ))}
        </div>
      </div>

      {/* History List */}
      <div className="space-y-3">
        {filteredHistory.map((item, i) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 * i }}
            className="glass-card p-4 flex items-center gap-4 hover:border-blue-500/20 transition-all cursor-pointer"
          >
            {/* Risk Indicator */}
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
              item.risk_score > 70 ? 'bg-red-500/10' :
              item.risk_score > 40 ? 'bg-yellow-500/10' : 'bg-green-500/10'
            }`}>
              {item.risk_score > 70 ? (
                <AlertTriangle className="w-6 h-6 text-red-400" />
              ) : item.risk_score > 40 ? (
                <Shield className="w-6 h-6 text-yellow-400" />
              ) : (
                <CheckCircle className="w-6 h-6 text-green-400" />
              )}
            </div>

            {/* Content */}
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white truncate">{item.text}</p>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-xs text-gray-500">{item.date}</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-gray-800 text-gray-400">
                  {item.source}
                </span>
              </div>
            </div>

            {/* Score & Badge */}
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className={`text-lg font-bold ${
                  item.risk_score > 70 ? 'text-red-400' :
                  item.risk_score > 40 ? 'text-yellow-400' : 'text-green-400'
                }`}>
                  {item.risk_score}%
                </p>
                <p className="text-xs text-gray-500">Risk</p>
              </div>
              <ThreatBadge level={item.risk_level} />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
