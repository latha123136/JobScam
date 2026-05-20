import { useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate, Link } from 'react-router-dom'
import { Shield, Mail, Lock, Eye, EyeOff, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import { login } from '../services/api'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e) => {
    e.preventDefault()
    if (!email || !password) {
      toast.error('Please fill in all fields')
      return
    }

    setLoading(true)
    try {
      const response = await login(email, password)
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      toast.success('Login successful!')
      navigate('/dashboard')
    } catch (error) {
      // Allow demo login
      if (email && password) {
        localStorage.setItem('token', 'demo-token')
        localStorage.setItem('user', JSON.stringify({ name: 'Demo User', email }))
        toast.success('Welcome! (Demo mode)')
        navigate('/dashboard')
      } else {
        toast.error('Invalid credentials')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-cyber-dark flex">
      {/* Left Panel - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        <div className="absolute inset-0 cyber-grid opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/40 to-purple-900/40"></div>
        <div className="relative z-10 flex flex-col justify-center px-16">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <Shield className="w-7 h-7 text-white" />
              </div>
              <span className="text-2xl font-bold gradient-text">ScamShield AI</span>
            </div>
            <h2 className="text-4xl font-bold text-white leading-tight mb-4">
              Protect Yourself From<br />
              <span className="gradient-text">Recruitment Fraud</span>
            </h2>
            <p className="text-gray-400 text-lg">
              AI-powered platform detecting fake jobs, verifying companies, 
              and keeping job seekers safe from cyber fraud.
            </p>
            <div className="mt-8 space-y-3">
              {['Real-time scam detection', 'Multi-modal AI analysis', 'Explainable risk scoring'].map((item, i) => (
                <div key={i} className="flex items-center gap-3 text-gray-300">
                  <div className="w-2 h-2 rounded-full bg-blue-400"></div>
                  {item}
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Right Panel - Form */}
      <div className="flex-1 flex items-center justify-center px-8">
        <motion.div
          className="w-full max-w-md"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="text-center mb-8">
            <div className="lg:hidden flex items-center justify-center gap-2 mb-6">
              <Shield className="w-8 h-8 text-blue-400" />
              <span className="text-xl font-bold gradient-text">ScamShield AI</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Welcome Back</h1>
            <p className="text-gray-400 text-sm mt-2">Sign in to access your dashboard</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="text-sm font-medium text-gray-300 mb-2 block">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="input-cyber pl-11"
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-300 mb-2 block">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="input-cyber pl-11 pr-11"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-cyber w-full text-white flex items-center justify-center gap-2"
            >
              {loading ? 'Signing in...' : 'Sign In'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <p className="text-center text-sm text-gray-400 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-400 hover:text-blue-300 font-medium">
              Create Account
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  )
}
