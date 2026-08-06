import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api/client.js'
import { SentimentBadge, PriorityBadge, StatusPill, Card, SectionHeader } from '../components/ui.jsx'

export default function MeetingDetail() {
  const { id } = useParams()
  const [meeting, setMeeting] = useState(null)

  useEffect(() => { api.getMeeting(id).then(setMeeting) }, [id])

  if (!meeting) return <p className="text-mist">Loading meeting...</p>

  return (
    <div className="space-y-8">
      <div>
        <div className="flex items-center gap-3 mb-2">
          <h1 className="font-display text-2xl font-semibold text-paper">{meeting.title}</h1>
          <SentimentBadge sentiment={meeting.sentiment} confidence={meeting.sentiment_confidence} />
        </div>
        <p className="text-mist text-sm font-mono">{new Date(meeting.date).toLocaleString()}</p>
      </div>

      <Card className="p-6">
        <SectionHeader eyebrow="AI Summary" title="What happened" />
        <p className="text-paper/90 leading-relaxed text-sm">{meeting.summary}</p>
      </Card>

      <div className="grid md:grid-cols-2 gap-6">
        <Card className="p-6">
          <SectionHeader eyebrow="Outcomes" title="Key decisions" />
          <p className="text-paper/80 text-sm whitespace-pre-wrap">{meeting.key_decisions}</p>
        </Card>
        <Card className="p-6">
          <SectionHeader eyebrow="Follow-ups" title="Open questions" />
          <p className="text-paper/80 text-sm whitespace-pre-wrap">{meeting.open_questions}</p>
        </Card>
      </div>

      <div>
        <SectionHeader eyebrow="Action Item Extraction" title="Tasks from this meeting" />
        <div className="space-y-2">
          {meeting.tasks.map(t => (
            <Card key={t.id} className="p-4 flex items-center justify-between gap-4">
              <div className="min-w-0">
                <p className="text-paper text-sm truncate">{t.task}</p>
                <div className="flex items-center gap-2 mt-1 text-xs font-mono text-mist">
                  <span>{t.owner}{t.owner_is_predicted && <span className="text-amber"> (auto)</span>}</span>
                  <span>·</span>
                  <span>{t.deadline}{t.deadline_is_predicted && <span className="text-amber"> (predicted)</span>}</span>
                </div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <PriorityBadge priority={t.priority} />
                <StatusPill status={t.status} />
              </div>
            </Card>
          ))}
          {meeting.tasks.length === 0 && <p className="text-mist text-sm">No action items detected.</p>}
        </div>
      </div>

      <Card className="p-6">
        <SectionHeader eyebrow="Raw Transcript" title="Full transcript" />
        <p className="text-mist text-xs leading-relaxed max-h-64 overflow-y-auto whitespace-pre-wrap font-mono">{meeting.transcript}</p>
      </Card>
    </div>
  )
}
