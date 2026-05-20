import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { 
  Shield, Zap, Brain, Globe, Lock, Eye, 
  ArrowRight, CheckCircle, Users, AlertTriangle,
  Scan, Database, Bot
} from 'lucide-react'

const features = [
  { icon: Brain, title: 'Multi-Modal AI', desc: 'NLP, Computer Vision, and Behavioral Analysis combined' },
  { icon: Zap, title: 'Real-Time Detection', desc: 'Instant scam analysis in under 2 seconds' },
  { icon: Globe, title: 'URL Intelligence', desc: 'Domain trust scoring and phishing detection' },
  { icon: Lock, title: 'Company Verification', desc: 'Authenticate companies through multiple signals' },
  { icon: Eye, title: 'Explainable AI', desc: 'Understand WHY a job is flagged as suspicious' },
  { icon: Bot, title: 'AI Safety Assistant', desc: 'Chat with AI for fraud prevention guidance' },
]

const stats = [
  { value: '15,847+', label: 'Jobs Analyzed' },
  { value: '96.7%', label: 'Detection Accuracy' },
  { value: '4,231', label: 'Scams Blocked' },
  { value: '12,450+', label: 'Users Protected' },
]

export default function Landing() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-cyber-dark overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 cyber-grid opacity-50"></div>
      <div className="fixed inset-0 bg-gradient-radial from-blue-900/20 via-transparent to-transparent"></div>

      {/* Navbar */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-5 border-b border-gray-800/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold gradient-text">ScamShield AI</span>
        </div>
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/login')} className="px-4 py-2 text-sm text-gray-300 hover:text-white transition-colors">
            Login
          </button>
          <button onClick={() => navigate('/register')} className="btn-cyber text-sm text-white">
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-8 pt-20 pb-32">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/20 mb-8">
              <Scan className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-blue-400 font-medium">AI-Powered Cyber Fraud Prevention</span>
            </div>
          </motion.div>

          <motion.h1
            className="text-5xl md:text-7xl font-bold leading-tight mb-6"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <span className="text-white">Real-Time Job Scam</span>
            <br />
            <span className="gradient-text">Detection & Prevention</span>
          </motion.h1>

          <motion.p
            className="text-lg text-gray-400 max-w-2xl mx-auto mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Enterprise-grade AI platform that protects job seekers from recruitment fraud 
            using multi-modal intelligence, behavioral analysis, and explainable AI.
          </motion.p>

          <motion.div
            className="flex items-center justify-center gap-4"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <button
              onClick={() => navigate('/dashboard')}
              className="btn-cyber text-white flex items-center gap-2"
            >
              <Shield className="w-5 h-5" />
              Analyze Job Now
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => navigate('/analytics')}
              className="px-6 py-3 rounded-lg border border-gray-600 text-gray-300 hover:border-blue-500 hover:text-white transition-all duration-300"
            >
              View Live Dashboard
            </button>
          </motion.div>
        </div>

        {/* Stats */}
        <motion.div
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
        >
          {stats.map((stat, i) => (
            <div key={i} className="glass-card p-6 text-center">
              <div className="text-3xl font-bold gradient-text">{stat.value}</div>
              <div className="text-sm text-gray-400 mt-1">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Multi-Modal AI Intelligence
          </h2>
          <p className="text-gray-400 max-w-xl mx-auto">
            Six layers of AI-powered analysis working together to detect even the most sophisticated scams
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={i}
              className="glass-card p-6 hover:border-blue-500/30 transition-all duration-300 group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.1 * i }}
              whileHover={{ y: -5 }}
            >
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center mb-4 group-hover:from-blue-500/30 group-hover:to-purple-500/30 transition-all">
                <feature.icon className="w-6 h-6 text-blue-400" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-sm text-gray-400">{feature.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="relative z-10 max-w-7xl mx-auto px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">How It Works</h2>
        </div>
        <div className="grid md:grid-cols-4 gap-8">
          {[
            { step: '01', title: 'Input', desc: 'Paste job description, URL, or upload document' },
            { step: '02', title: 'AI Analysis', desc: 'Multi-modal AI processes through 6 detection layers' },
            { step: '03', title: 'Risk Scoring', desc: 'Dynamic risk score generated with confidence level' },
            { step: '04', title: 'Explanation', desc: 'Explainable AI tells you WHY it\'s suspicious' },
          ].map((item, i) => (
            <motion.div
              key={i}
              className="text-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 * i }}
            >
              <div className="text-4xl font-bold gradient-text mb-3">{item.step}</div>
              <h3 className="text-lg font-semibold text-white mb-2">{item.title}</h3>
              <p className="text-sm text-gray-400">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="relative z-10 max-w-4xl mx-auto px-8 py-20 text-center">
        <div className="glass-card p-12">
          <AlertTriangle className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
          <h2 className="text-3xl font-bold text-white mb-4">
            Don't Fall Victim to Job Scams
          </h2>
          <p className="text-gray-400 mb-8">
            Every day, thousands of job seekers lose money to recruitment fraud. 
            Our AI platform helps you verify before you trust.
          </p>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn-cyber text-white text-lg"
          >
            Start Free Analysis →
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-gray-800 py-8 px-8">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-blue-400" />
            <span className="text-sm text-gray-400">ScamShield AI © 2024</span>
          </div>
          <p className="text-xs text-gray-500">AI-Powered Recruitment Fraud Prevention Platform</p>
        </div>
      </footer>
    </div>
  )
}
