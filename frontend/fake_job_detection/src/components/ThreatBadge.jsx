import { ShieldAlert, ShieldCheck, AlertTriangle, ShieldX, Shield } from 'lucide-react'

const configs = {
  'Safe': { icon: ShieldCheck, color: 'green', bg: 'bg-green-500/10', border: 'border-green-500/30', text: 'text-green-400' },
  'Low Risk': { icon: Shield, color: 'blue', bg: 'bg-blue-500/10', border: 'border-blue-500/30', text: 'text-blue-400' },
  'Medium Risk': { icon: AlertTriangle, color: 'yellow', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-400' },
  'High Risk': { icon: ShieldAlert, color: 'orange', bg: 'bg-orange-500/10', border: 'border-orange-500/30', text: 'text-orange-400' },
  'Critical Scam': { icon: ShieldX, color: 'red', bg: 'bg-red-500/10', border: 'border-red-500/30', text: 'text-red-400' },
}

export default function ThreatBadge({ level = 'Safe' }) {
  const config = configs[level] || configs['Safe']
  const Icon = config.icon

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full ${config.bg} border ${config.border}`}>
      <Icon className={`w-4 h-4 ${config.text}`} />
      <span className={`text-sm font-semibold ${config.text}`}>{level}</span>
    </div>
  )
}
