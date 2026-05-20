import { NavLink } from 'react-router-dom'
import { 
  Shield, BarChart3, Building2, MessageCircle, 
  History, AlertTriangle, Home, BookOpen, Globe
} from 'lucide-react'

const navItems = [
  { path: '/dashboard', icon: Shield, label: 'Scam Detection' },
  { path: '/live-scraping', icon: Globe, label: 'Live Scraping' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/company-verify', icon: Building2, label: 'Company Verify' },
  { path: '/chat', icon: MessageCircle, label: 'AI Assistant' },
  { path: '/history', icon: History, label: 'Scan History' },
  { path: '/awareness', icon: BookOpen, label: 'Scam Awareness' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-cyber-darker border-r border-cyber-border flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-cyber-border">
        <NavLink to="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold gradient-text">ScamShield</h1>
            <p className="text-xs text-gray-500">AI Fraud Detection</p>
          </div>
        </NavLink>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                isActive
                  ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="text-sm font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Bottom Section */}
      <div className="p-4 border-t border-cyber-border">
        <div className="glass-card p-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-yellow-400" />
            <span className="text-xs font-semibold text-yellow-400">Threat Level</span>
          </div>
          <div className="w-full bg-gray-800 rounded-full h-2">
            <div className="bg-gradient-to-r from-yellow-400 to-red-500 h-2 rounded-full" style={{ width: '65%' }}></div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Moderate - 12 new threats today</p>
        </div>
      </div>
    </aside>
  )
}
