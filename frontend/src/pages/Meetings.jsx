import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client.js'
import { SentimentBadge, Card, SectionHeader } from '../components/ui.jsx'

export default function Meetings() {
  const [meetings, setMeetings] = useState([])
  const [source, setSource] = useState('')
  const [language, setLanguage] = useState('english')
  const [status, setStatus] = useState(null)

  const load = () => api.getMeetings().then(setMeetings)
  useEffect(() => { load() }, [])

  const submit = async (e) => {
    e.preventDefault()
    if (!source.trim()) return
    setStatus('Submitting to pipeline (Zoom/Teams/Meet recording → Whisper/Sarvam → summary → tasks)...')
    const res = await api.processMeeting(source, language)
    setStatus(res.message || 'Processing started.')
    setSource('')
    setTimeout(load, 1500)
  }

  return (
    <div className="space-y-8">
      <SectionHeader eyebrow="Recordings" title="Meetings" />

      <Card className="p-5">
        <form onSubmit={submit} className="flex flex-col md:flex-row gap-3">
          <input
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Paste a Zoom/Teams/Meet recording link, YouTube URL, or local file path"
            className="flex-1 bg-panelLight border border-line rounded-lg px-3 py-2.5 text-sm placeholder:text-mist outline-none focus:border-signal/50"
          />
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-panelLight border border-line rounded-lg px-3 py-2.5 text-sm outline-none focus:border-signal/50"
          >
            <option value="english">English</option>
            <option value="hinglish">Hinglish</option>
          </select>
          <button type="submit" className="bg-signal text-ink font-medium px-5 py-2.5 rounded-lg text-sm hover:brightness-110 transition-all">
            Process meeting
          </button>
        </form>
        {status && <div className="text-mist text-xs font-mono mt-3">{status}</div>}
      </Card>

      <div className="space-y-3">
        {meetings.map(m => (
          <Link to={`/meetings/${m.id}`} key={m.id}>
            <Card className="p-5 hover:border-signal/40 transition-colors flex items-center justify-between gap-4">
              <div className="min-w-0">
                <div className="flex items-center gap-3 mb-1">
                  <h3 className="font-display font-medium text-paper truncate">{m.title}</h3>
                  <SentimentBadge sentiment={m.sentiment} confidence={m.sentiment_confidence} />
                </div>
                <p className="text-mist text-sm truncate">{m.summary}</p>
              </div>
              <div className="text-right shrink-0">
                <div className="text-xs font-mono text-mist">{new Date(m.date).toLocaleDateString()}</div>
                <div className="text-xs font-mono text-signal">{m.task_count} tasks</div>
              </div>
            </Card>
          </Link>
        ))}
        {meetings.length === 0 && <p className="text-mist text-sm">No meetings yet — process your first recording above.</p>}
      </div>
    </div>
  )
}
