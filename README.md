# 🎙️ AI Meeting Intelligence Platform

An AI-powered meeting assistant that automatically transcribes meeting recordings, generates concise summaries, extracts action items, analyzes team sentiment, predicts deadlines, and provides an interactive dashboard for meeting analytics.

The platform helps organizations reduce manual note-taking, improve task tracking, and enable intelligent search across past meetings using Generative AI.

---

## 🚀 Problem Statement

In modern organizations, employees spend hours attending meetings but often struggle with:

- Missing important decisions
- Forgetting assigned tasks
- Manual note-taking
- Difficulty finding information from previous meetings
- Lack of productivity insights
- No centralized meeting knowledge base

This project automates the complete meeting documentation process using AI.
## 💡 Solution

The AI Meeting Intelligence Platform converts meeting recordings into structured business insights by automatically:

- Transcribing audio
- Generating meeting summaries
- Extracting action items
- Assigning tasks
- Predicting deadlines

  ## ✨ Features

### 🎤 Speech-to-Text
- Automatic meeting transcription
- Whisper/Sarvam integration

### 📝 AI Meeting Summary
- Executive summary
- Key discussion points
- Decisions taken

### ✅ Action Item Extraction
- Detects action items
- Extracts owners
- Predicts deadlines

### 😊 Sentiment Analysis
- Positive
- Neutral
- Negative

### 🔍 AI Meeting Search
- Natural language search
- Cross-meeting semantic search

### 📊 Dashboard Analytics
- Meeting statistics
- Productivity score
- Task completion tracking

### 👥 Employee Dashboard
- Assigned tasks
- Completion percentage
- Meeting participation
- Performing sentiment analysis
- Searching previous meetings using AI
- Tracking employee productivity
  ## 🛠 Tech Stack

### Frontend
- React.js
- Vite
- Tailwind CSS
- Recharts

### Backend
- FastAPI
- Python

### Database
- PostgreSQL
- SQLAlchemy

### AI / ML
- OpenAI / Gemini
- Whisper
- Sentence Transformers
- LangChain

### Tools
- Git
- GitHub
## 🏗 System Architecture

```text
                Meeting Recording
                       │
                       ▼
             Audio Preprocessing
                       │
                       ▼
            Speech-to-Text (Whisper)
                       │
                       ▼
         AI Summary & Decision Extraction
                       │
                       ▼
        Action Item & Task Extraction
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
 Sentiment AI   Deadline AI   Task Assignment
          │            │            │
          └────────────┼────────────┘
                       ▼
              PostgreSQL Database
                       │
                       ▼
               FastAPI REST APIs
                       │
                       ▼
          React Dashboard (Frontend)
```
## 🔄 Workflow

1. Upload a meeting recording.
2. Audio is preprocessed.
3. Whisper converts speech into text.
4. LLM generates meeting summary.
5. AI extracts:
   - Decisions
   - Action items
   - Owners
   - Deadlines
6. Sentiment analysis measures meeting tone.
7. Results are stored in PostgreSQL.
8. Dashboard visualizes analytics and productivity.
9. Users search previous meetings using natural language.

## 🚀 Future Enhancements

- Email reminders
- Calendar integration
- Microsoft Teams integration
- Real-time meeting assistant
- Multi-language transcription
