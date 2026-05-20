import { motion } from 'framer-motion'

export default function RiskMeter({ score = 0, size = 200 }) {
  const radius = (size - 20) / 2
  const circumference = 2 * Math.PI * radius
  const progress = (score / 100) * circumference

  const getColor = (score) => {
    if (score <= 20) return '#10b981'
    if (score <= 40) return '#3b82f6'
    if (score <= 60) return '#f59e0b'
    if (score <= 80) return '#f97316'
    return '#ef4444'
  }

  const getLabel = (score) => {
    if (score <= 20) return 'Safe'
    if (score <= 40) return 'Low Risk'
    if (score <= 60) return 'Medium Risk'
    if (score <= 80) return 'High Risk'
    return 'Critical'
  }

  const color = getColor(score)

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="#1e293b"
            strokeWidth="12"
          />
          {/* Progress circle */}
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: circumference - progress }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            style={{
              filter: `drop-shadow(0 0 8px ${color})`
            }}
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            className="text-4xl font-bold"
            style={{ color }}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5, duration: 0.5 }}
          >
            {score}
          </motion.span>
          <span className="text-sm text-gray-400 mt-1">Risk Score</span>
        </div>
      </div>
      <motion.div
        className="mt-3 px-4 py-1.5 rounded-full text-sm font-semibold"
        style={{ 
          backgroundColor: `${color}20`,
          color: color,
          border: `1px solid ${color}40`
        }}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1 }}
      >
        {getLabel(score)}
      </motion.div>
    </div>
  )
}
