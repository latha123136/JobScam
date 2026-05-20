/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0a0e1a',
          darker: '#060810',
          card: '#111827',
          border: '#1e293b',
          blue: '#3b82f6',
          purple: '#8b5cf6',
          cyan: '#06b6d4',
          green: '#10b981',
          red: '#ef4444',
          orange: '#f59e0b',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'cyber-gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'neon-gradient': 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'scan': 'scan 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 5px #3b82f6, 0 0 10px #3b82f6' },
          '100%': { boxShadow: '0 0 20px #8b5cf6, 0 0 40px #8b5cf6' },
        },
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' },
        }
      },
      boxShadow: {
        'neon': '0 0 5px theme("colors.cyber.blue"), 0 0 20px theme("colors.cyber.blue")',
        'neon-purple': '0 0 5px theme("colors.cyber.purple"), 0 0 20px theme("colors.cyber.purple")',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      }
    },
  },
  plugins: [],
}
