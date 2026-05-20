import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, TrendingUp, Shield, AlertTriangle, 
  Users, Scan, Activity, Globe
} from 'lucide-react'
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts'

// Mock data (replace with API calls in production)
const trendData = [
  { month: 'Jan', scams: 320, safe: 890 },
  { month: 'Feb', scams: 410, safe: 920 },
  { month: 'Mar', scams: 380, safe: 1050 },
  { month: 'Apr', scams: 520, safe: 980 },
  { month: 'May', scams: 610, safe: 1100 },
  { month: 'Jun', scams: 480, safe: 1200 },
  { month: 'Jul', scams: 550, safe: 1150 },
  { month: 'Aug', scams: 690, safe: 1300 },
  { month: 'Sep', scams: 720, safe: 1250 },
  { month: 'Oct', scams: 580, safe: 1400 },
  { month: 'Nov', scams: 640, safe: 1350 },
  { month: 'Dec', scams: 530, safe: 1280 },
]

const riskDistribution = [
  { name: 'Safe', value: 40.5, color: '#10b981' },
  { name: 'Low Risk', value: 20.1, color: '#3b82f6' },
  { name: 'Medium Risk', value: 17.9, color: '#f59e0b' },
  { name: 'High Risk', value: 13.6, color: '#f97316' },
  { name: 'Critical', value: 7.9, color: '#ef4444' },
]

const scamTypes = [
  { type: 'Registration Fee', count: 1240 },
  { type: 'Fake BPO', count: 890 },
  { type: 'WhatsApp Scams', count: 720 },
  { type: 'Fake Internship', count: 580 },
  { type: 'Phishing', count: 450 },
  { type: 'Crypto/MLM', count: 351 },
]

const threats = [
  { id: 1, title: 'Fake TCS Recruitment Drive', severity: 'Critical', date: '2024-12-15' },
  { id: 2, title: 'Internshala Certificate Scam', severity: 'High', date: '2024-12-14' },
  { id: 3, title: 'Amazon WFH Data Entry Scam', severity: 'High', date: '2024-12-13' },
  { id: 4, title: 'Crypto Trading Job Scam', severity: 'Medium', date: '2024-12-12' },
  { id: 5, title: 'Government Job Portal Phishing', severity: 'Critical', date: '2024-12-11' },
]

const statCards = [
  { icon: Scan, label: 'Total Scans', value: '15,847', change: '+12%', color: 'blue' },
  { icon: AlertTriangle, label: 'Scams Detected', value: '4,231', change: '+8%', color: 'red' },
  { icon: Shield, label: 'Accuracy', value: '96.7%', change: '+0.3%', color: 'green' },
  { icon: Users, label: 'Users Protected', value: '12,450', change: '+15%', color: 'purple' },
]

export default function Analytics() {
  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <BarChart3 className="w-7 h-7 text-blue-400" />
          Fraud Intelligence Dashboard
        </h1>
        <p className="text-gray-400 text-sm mt-1">Real-time analytics and threat intelligence</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, i) => (
          <motion.div
            key={i}
            className="glass-card p-5"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * i }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs text-gray-400 uppercase tracking-wider">{stat.label}</p>
                <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                <p className={`text-xs mt-1 text-${stat.color}-400`}>
                  <TrendingUp className="w-3 h-3 inline mr-1" />
                  {stat.change} this month
                </p>
              </div>
              <div className={`w-12 h-12 rounded-lg bg-${stat.color}-500/10 flex items-center justify-center`}>
                <stat.icon className={`w-6 h-6 text-${stat.color}-400`} />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Trend Chart */}
        <div className="lg:col-span-2 glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-400" />
            Scam Detection Trends
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="colorScams" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorSafe" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="month" stroke="#64748b" fontSize={12} />
              <YAxis stroke="#64748b" fontSize={12} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                labelStyle={{ color: '#e2e8f0' }}
              />
              <Legend />
              <Area type="monotone" dataKey="safe" stroke="#10b981" fill="url(#colorSafe)" name="Safe Jobs" />
              <Area type="monotone" dataKey="scams" stroke="#ef4444" fill="url(#colorScams)" name="Scams Detected" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Distribution */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Risk Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={3}
                dataKey="value"
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-2 mt-2">
            {riskDistribution.map((item, i) => (
              <div key={i} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></div>
                  <span className="text-gray-400">{item.name}</span>
                </div>
                <span className="text-gray-300">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid lg:grid-cols-2 gap-6">
        {/* Scam Types */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Top Scam Categories</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={scamTypes} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis type="number" stroke="#64748b" fontSize={12} />
              <YAxis dataKey="type" type="category" stroke="#64748b" fontSize={11} width={120} />
              <Tooltip
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
              />
              <Bar dataKey="count" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Live Threat Feed */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Globe className="w-5 h-5 text-red-400" />
            Live Threat Feed
          </h3>
          <div className="space-y-3">
            {threats.map((threat) => (
              <div key={threat.id} className="flex items-center justify-between p-3 rounded-lg bg-gray-900/50 border border-gray-800">
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${
                    threat.severity === 'Critical' ? 'bg-red-500 animate-pulse' :
                    threat.severity === 'High' ? 'bg-orange-500' : 'bg-yellow-500'
                  }`}></div>
                  <div>
                    <p className="text-sm text-white">{threat.title}</p>
                    <p className="text-xs text-gray-500">{threat.date}</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${
                  threat.severity === 'Critical' ? 'bg-red-500/10 text-red-400' :
                  threat.severity === 'High' ? 'bg-orange-500/10 text-orange-400' :
                  'bg-yellow-500/10 text-yellow-400'
                }`}>
                  {threat.severity}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
