import { motion } from 'framer-motion'
import { Shield, Scan } from 'lucide-react'

export default function LoadingAnimation({ text = "Analyzing..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      {/* Animated Shield */}
      <div className="relative">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          className="w-20 h-20 rounded-full border-2 border-dashed border-blue-500/30"
        />
        <motion.div
          animate={{ scale: [1, 1.2, 1] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="absolute inset-0 flex items-center justify-center"
        >
          <Shield className="w-8 h-8 text-blue-400" />
        </motion.div>
      </div>

      {/* Scanning Text */}
      <motion.div
        className="mt-6 flex items-center gap-2"
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
      >
        <Scan className="w-4 h-4 text-blue-400" />
        <span className="text-sm text-blue-400 font-medium">{text}</span>
      </motion.div>

      {/* Progress Dots */}
      <div className="flex gap-1 mt-4">
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="w-2 h-2 rounded-full bg-blue-500"
            animate={{ opacity: [0.3, 1, 0.3] }}
            transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
          />
        ))}
      </div>
    </div>
  )
}
