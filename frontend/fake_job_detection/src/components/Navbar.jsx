import { Bell, Search, User, LogOut } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function Navbar() {
  const navigate = useNavigate()

  return (
    <header className="h-16 bg-cyber-darker/80 backdrop-blur-md border-b border-cyber-border flex items-center justify-between px-6">
      {/* Search */}
      <div className="flex items-center gap-3 flex-1 max-w-md">
        <div className="relative w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search scans, companies, threats..."
            className="w-full pl-10 pr-4 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition-colors"
          />
        </div>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        {/* Live Status */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/20">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
          <span className="text-xs font-medium text-green-400">AI Engine Active</span>
        </div>

        {/* Notifications */}
        <button className="relative p-2 rounded-lg hover:bg-gray-800 transition-colors">
          <Bell className="w-5 h-5 text-gray-400" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        {/* User Menu */}
        <div className="flex items-center gap-3 pl-4 border-l border-gray-700">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <User className="w-4 h-4 text-white" />
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium text-white">User</p>
            <p className="text-xs text-gray-500">Analyst</p>
          </div>
          <button 
            onClick={() => navigate('/login')}
            className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
          >
            <LogOut className="w-4 h-4 text-gray-400" />
          </button>
        </div>
      </div>
    </header>
  )
}
