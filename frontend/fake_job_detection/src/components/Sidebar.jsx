import { NavLink } from 'react-router-dom'
import { 
  Shield, BarChart3, Building2, MessageCircle, 
  History, Home, BookOpen, Globe
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


    </aside>
  )
}
