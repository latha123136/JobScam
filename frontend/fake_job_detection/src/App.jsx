import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './layouts/Layout'
import Landing from './pages/Landing'
import Dashboard from './pages/Dashboard'
import Analytics from './pages/Analytics'
import CompanyVerify from './pages/CompanyVerify'
import ChatAssistant from './pages/ChatAssistant'
import History from './pages/History'
import Login from './pages/Login'
import Register from './pages/Register'
import Awareness from './pages/Awareness'
import LiveScraping from './pages/LiveScraping'

function App() {
  return (
    <>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#1e293b',
            color: '#e2e8f0',
            border: '1px solid rgba(59, 130, 246, 0.2)',
          },
        }}
      />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/company-verify" element={<CompanyVerify />} />
          <Route path="/chat" element={<ChatAssistant />} />
          <Route path="/history" element={<History />} />
          <Route path="/awareness" element={<Awareness />} />
          <Route path="/live-scraping" element={<LiveScraping />} />
        </Route>
      </Routes>
    </>
  )
}

export default App
