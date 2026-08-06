import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Shell from './components/Shell.jsx'
import ExecutiveDashboard from './pages/ExecutiveDashboard.jsx'
import Meetings from './pages/Meetings.jsx'
import MeetingDetail from './pages/MeetingDetail.jsx'
import Search from './pages/Search.jsx'
import VoiceSearch from './pages/VoiceSearch.jsx'
import Tasks from './pages/Tasks.jsx'
import Analytics from './pages/Analytics.jsx'
import Employees from './pages/Employees.jsx'

export default function App() {
  return (
    <Shell>
      <Routes>
        <Route path="/" element={<ExecutiveDashboard />} />
        <Route path="/meetings" element={<Meetings />} />
        <Route path="/meetings/:id" element={<MeetingDetail />} />
        <Route path="/search" element={<Search />} />
        <Route path="/voice-search" element={<VoiceSearch />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/employees" element={<Employees />} />
      </Routes>
    </Shell>
  )
}
