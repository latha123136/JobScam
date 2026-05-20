import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Bot, Send, User, Sparkles, MessageCircle } from 'lucide-react'
import { sendChatMessage } from '../services/api'

const SUGGESTIONS = [
  "What are common job scam red flags?",
  "Is it safe if a company asks for registration fee?",
  "How to identify fake offer letters?",
  "How to report a job scam in India?",
]

export default function ChatAssistant() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "👋 Hi! I'm your **AI Job Safety Assistant**. I can help you identify scams, verify companies, and stay safe during your job search.\n\nAsk me anything about job fraud prevention!",
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async (text = null) => {
    const message = text || input.trim()
    if (!message) return

    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setInput('')
    setLoading(true)

    try {
      const response = await sendChatMessage(message)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.response,
        suggestions: response.data.suggestions
      }])
    } catch (error) {
      // Fallback response if API is down
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "I'm having trouble connecting to the server. Here's a general tip: **Never pay money to get a job.** Legitimate companies don't charge registration fees, training fees, or security deposits from candidates.",
        suggestions: SUGGESTIONS
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
          <Bot className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-white">AI Safety Assistant</h1>
          <p className="text-xs text-gray-400">Powered by Fraud Intelligence Engine</p>
        </div>
        <div className="ml-auto flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 border border-green-500/20">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
          <span className="text-xs text-green-400">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : ''}`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shrink-0">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}
              <div className={`max-w-[80%] ${
                msg.role === 'user'
                  ? 'bg-blue-600/20 border border-blue-500/30 rounded-2xl rounded-tr-sm px-4 py-3'
                  : 'glass-card px-4 py-3 rounded-2xl rounded-tl-sm'
              }`}>
                <div className="text-sm text-gray-200 whitespace-pre-wrap leading-relaxed">
                  {msg.content.split('**').map((part, idx) =>
                    idx % 2 === 1 ? <strong key={idx} className="text-white">{part}</strong> : part
                  )}
                </div>
                {/* Suggestions */}
                {msg.suggestions && (
                  <div className="mt-3 flex flex-wrap gap-2">
                    {msg.suggestions.map((suggestion, si) => (
                      <button
                        key={si}
                        onClick={() => handleSend(suggestion)}
                        className="text-xs px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 hover:bg-blue-500/20 transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>
              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-lg bg-gray-700 flex items-center justify-center shrink-0">
                  <User className="w-4 h-4 text-gray-300" />
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Typing Indicator */}
        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-3"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="glass-card px-4 py-3 rounded-2xl rounded-tl-sm">
              <div className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <motion.div
                    key={i}
                    className="w-2 h-2 rounded-full bg-blue-400"
                    animate={{ opacity: [0.3, 1, 0.3] }}
                    transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
                  />
                ))}
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions (shown when no messages) */}
      {messages.length <= 1 && (
        <div className="py-4">
          <p className="text-xs text-gray-500 mb-2 flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> Suggested questions
          </p>
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map((suggestion, i) => (
              <button
                key={i}
                onClick={() => handleSend(suggestion)}
                className="text-sm px-4 py-2 rounded-lg bg-gray-800/50 border border-gray-700 text-gray-300 hover:border-blue-500/50 hover:text-white transition-all"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="mt-4 glass-card p-3 flex items-center gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about job safety, scam detection, or fraud prevention..."
          className="flex-1 bg-transparent text-white placeholder-gray-500 focus:outline-none text-sm"
          disabled={loading}
        />
        <button
          onClick={() => handleSend()}
          disabled={loading || !input.trim()}
          className="p-2 rounded-lg bg-blue-500 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Send className="w-4 h-4 text-white" />
        </button>
      </div>
    </div>
  )
}
