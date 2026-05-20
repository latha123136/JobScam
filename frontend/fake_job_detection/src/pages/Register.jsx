import { useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate, Link } from 'react-router-dom'
import { Shield, Mail, Lock, User, Eye, EyeOff, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import { register } from '../services/api'

export default function Register() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleRegister = async (e) => {
    e.preventDefault()
    if (!name || !email || !password) {
      toast.error('Please fill in all fields')
      return
    }
    if (password.length < 6) {
      toast.error('Password must be at least 6 characters')
      return
    }

    setLoading(true)
    try {
      const response = await register(name, email, password)
      localStorage.setItem('token', response.data.token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      toast.success('Account created successfully!')
      navigate('/dashboard')
    } catch (error) {
      // Demo mode fallback
      localStorage.setItem('token', 'demo-token')
      localStorage.setItem('user', JSON.stringify({ name, email }))
      toast.success('Welcome! (Demo mode)')
      navigate('/dashboard')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-cyber-dark flex">
      {/* Left Panel */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        <div className="absolute inset-0 cyber-grid opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/40 to-blue-900/40"></div>
        <div className="relative z-10 flex flex-col justify-center px-16">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <div className="flex items-center gap-3 mb-8">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <Shield className="w-7 h-7 text-white" />
              </div>
              <span className="text-2xl font-bold gradient-text">ScamShield AI</span>
            </div>
            <h2 className="text-4xl font-bold text-white leading-tight mb-4">
              Join the Fight Against<br />
              <span className="gradient-text">Job Fraud</span>
            </h2>
            <p className="text-gray-400 text-lg">
              Create your free account and start protecting yourself 
              from recruitment scams with AI-powered detection.
            </p>
          </motion.div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="flex-1 flex items-center justify-center px-8">
        <motion.div
          className="w-full max-w-md"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="text-center mb-8">
            <div className="lg:hidden flex items-center justify-center gap-2 mb-6">
              <Shield className="w-8 h-8 text-blue-400" />
              <span className="text-xl font-bold gradient-text">ScamShield AI</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Create Account</h1>
            <p className="text-gray-400 text-sm mt-2">Start your fraud-free job search</p>
          </div>

          <form onSubmit={handleRegister} className="space-y-5">
            <div>
              <label className="text-sm font-medium text-gray-300 mb-2 block">Full Name</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="John Doe"
                  className="input-cyber pl-11"
                />
              </div>
            </div>

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
                  placeholder="Min 6 characters"
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
              {loading ? 'Creating Account...' : 'Create Account'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <p className="text-center text-sm text-gray-400 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-400 hover:text-blue-300 font-medium">
              Sign In
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  )
}
