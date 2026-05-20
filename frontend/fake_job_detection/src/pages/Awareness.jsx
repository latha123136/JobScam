import { motion } from 'framer-motion'
import { 
  BookOpen, AlertTriangle, Shield, CheckCircle, 
  XCircle, Phone, Globe, Mail, MessageCircle
} from 'lucide-react'

const scamTypes = [
  {
    title: "Registration Fee Scams",
    description: "Scammers ask candidates to pay fees for registration, training, or security deposits before joining.",
    redFlags: ["Pay ₹999 for training", "Security deposit required", "Processing fee needed"],
    icon: "💰",
    severity: "Critical"
  },
  {
    title: "Fake BPO/Call Center Jobs",
    description: "Fraudulent BPO companies that collect personal data and money, then disappear.",
    redFlags: ["No interview process", "Immediate joining", "Work from home with high salary"],
    icon: "📞",
    severity: "High"
  },
  {
    title: "WhatsApp/Telegram Scams",
    description: "Scammers reach out via messaging apps with too-good-to-be-true job offers.",
    redFlags: ["HR contacts via WhatsApp", "No official email", "Crypto/trading tasks"],
    icon: "📱",
    severity: "High"
  },
  {
    title: "Fake Internship Certificates",
    description: "Organizations selling internship certificates without any real work or learning.",
    redFlags: ["Pay for certificate", "No actual work", "Bulk WhatsApp promotions"],
    icon: "📜",
    severity: "Medium"
  },
  {
    title: "Captcha/Data Entry Scams",
    description: "Jobs promising high income for simple tasks like typing captchas or data entry.",
    redFlags: ["Earn ₹500 daily", "Simple typing work", "No skills required"],
    icon: "⌨️",
    severity: "High"
  },
  {
    title: "Phishing Job Portals",
    description: "Fake websites mimicking legitimate job portals to steal personal information.",
    redFlags: ["Misspelled URLs", "No HTTPS", "Asks for Aadhaar/PAN upfront"],
    icon: "🌐",
    severity: "Critical"
  }
]

const safetyTips = [
  "Never pay money to get a job - legitimate companies don't charge candidates",
  "Verify company registration on MCA portal before accepting offers",
  "Check recruiter's LinkedIn profile and corporate email domain",
  "Be suspicious of jobs with unrealistic salary promises",
  "Never share Aadhaar, PAN, or bank details before official joining",
  "Research company reviews on Glassdoor and AmbitionBox",
  "Verify offer letters by calling the company's official number",
  "Be cautious of jobs communicated only through WhatsApp/Telegram"
]

export default function Awareness() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <BookOpen className="w-7 h-7 text-blue-400" />
          Scam Awareness Center
        </h1>
        <p className="text-gray-400 text-sm mt-1">
          Learn to identify and protect yourself from recruitment fraud
        </p>
      </div>

      {/* Alert Banner */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-5 border-l-4 border-l-yellow-500"
      >
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-6 h-6 text-yellow-400 shrink-0" />
          <div>
            <h3 className="text-white font-semibold">Important Notice</h3>
            <p className="text-sm text-gray-300 mt-1">
              Job scams in India have increased by 300% in the last 2 years. Students and fresh graduates 
              are the primary targets. Always verify before you trust.
            </p>
          </div>
        </div>
      </motion.div>

      {/* Scam Types Grid */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">Common Job Scam Types</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {scamTypes.map((scam, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * i }}
              className="glass-card p-5 hover:border-blue-500/20 transition-all"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-2xl">{scam.icon}</span>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  scam.severity === 'Critical' ? 'bg-red-500/10 text-red-400' :
                  scam.severity === 'High' ? 'bg-orange-500/10 text-orange-400' :
                  'bg-yellow-500/10 text-yellow-400'
                }`}>
                  {scam.severity}
                </span>
              </div>
              <h3 className="text-white font-semibold mb-2">{scam.title}</h3>
              <p className="text-sm text-gray-400 mb-3">{scam.description}</p>
              <div className="space-y-1">
                {scam.redFlags.map((flag, fi) => (
                  <div key={fi} className="flex items-center gap-2 text-xs text-red-400">
                    <XCircle className="w-3 h-3" />
                    {flag}
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Safety Tips */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
          <Shield className="w-6 h-6 text-green-400" />
          Safety Tips
        </h2>
        <div className="grid md:grid-cols-2 gap-3">
          {safetyTips.map((tip, i) => (
            <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-green-500/5 border border-green-500/10">
              <CheckCircle className="w-4 h-4 text-green-400 mt-0.5 shrink-0" />
              <span className="text-sm text-gray-300">{tip}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Report Section */}
      <div className="glass-card p-6">
        <h2 className="text-xl font-bold text-white mb-4">How to Report Scams</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-gray-900/50 border border-gray-800">
            <Globe className="w-8 h-8 text-blue-400 mb-3" />
            <h3 className="text-white font-semibold mb-1">Cyber Crime Portal</h3>
            <p className="text-sm text-gray-400">cybercrime.gov.in</p>
          </div>
          <div className="p-4 rounded-lg bg-gray-900/50 border border-gray-800">
            <Phone className="w-8 h-8 text-green-400 mb-3" />
            <h3 className="text-white font-semibold mb-1">Helpline</h3>
            <p className="text-sm text-gray-400">Call 1930</p>
          </div>
          <div className="p-4 rounded-lg bg-gray-900/50 border border-gray-800">
            <Mail className="w-8 h-8 text-purple-400 mb-3" />
            <h3 className="text-white font-semibold mb-1">Platform Report</h3>
            <p className="text-sm text-gray-400">Report on LinkedIn/Naukri</p>
          </div>
        </div>
      </div>
    </div>
  )
}
