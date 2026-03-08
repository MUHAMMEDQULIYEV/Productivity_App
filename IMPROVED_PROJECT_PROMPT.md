# 🚀 Complete Productivity & Language Learning Platform - Project Specification

## **Project Vision**
Build a self-hosted, local productivity & language learning platform that combines task management, flashcard study, AI-powered analytics, and language pattern recognition from YouTube videos. Run entirely locally with Docker containerization, with optional ngrok tunneling for external access.

---

## **1. CORE FEATURES** ⭐

### **1.1 Task & Time Management**
- **Task Creation**: Add tasks with title, description, category (Work/Study/Learning/Personal)
- **Timeline Management**: Set deadlines, estimated duration, priority levels (High/Medium/Low)
- **Task Status Tracking**: Not Started → In Progress → Completed → Archived
- **Calendar Integration**: Connect to Google Calendar via MCP server to sync tasks bidirectionally
- **Time Blocking**: Visual calendar view showing task timelines and deadlines

### **1.2 Notes System**
- **Rich Text Notes**: Create, edit, delete notes with formatting (bold, italic, headers, lists)
- **Tagging System**: Organize notes with custom tags and categories
- **Search & Filter**: Full-text search across all notes
- **Note Templates**: Pre-built templates for different note types

### **1.3 Flashcard System**
- **Flashcard Creation**: Create decks, add cards with front/back content
- **Spaced Repetition**: Algorithm-based review scheduling (SM-2 algorithm)
- **Study Modes**: Flip cards, multiple choice, fill-in-the-blank
- **Progress Tracking**: Track cards learned, in-progress, need-review
- **Language-Specific Decks**: Dedicated decks for English & Korean vocabulary

### **1.4 Email Notification System**
- **Multiple Notification Types**:
  - Upcoming task alerts (1 hour before deadline)
  - Daily summary email with today's tasks
  - Task reminders (customizable: 24h, 12h, 1h before)
  - Weekly progress reports (completed tasks, learning achievements)
  - Language milestone notifications (new vocabulary learned)
- **Configurable Settings**: Users can enable/disable notification types per task
- **Email Integration**: SMTP configuration for sending emails (Gmail, Outlook, custom)

---

## **2. MACHINE LEARNING & ANALYTICS** 🤖

### **2.1 Productivity Pattern Analysis**
- **Task Frequency Analytics**: Which categories/subjects you work on most
- **Completion Rate Tracking**: Success rate by category and time period
- **Productivity Patterns**:
  - Best time of day for completing tasks
  - Days with highest task completion
  - Average time spent per task type
  - Procrastination detection (overdue task analysis)
- **Recommendations**: Suggest optimal task scheduling based on historical patterns

### **2.2 Language Learning Analytics**
- **Vocabulary Growth Tracker**:
  - New words learned per week/month
  - Retention rate (how many learned words are still remembered)
  - Difficulty distribution (easy → medium → hard words)
- **Learning Progress Dashboard**:
  - Words mastered vs. in-progress vs. new
  - Time spent learning per language
  - Flashcard accuracy by language and category
- **Grammar Pattern Analysis**: Track grammar concepts learned, weak areas

### **2.3 ML Implementation**
- **Algorithm**: Use scikit-learn for:
  - Time-series analysis for productivity patterns
  - Clustering for task similarity
  - Recommendation engine for optimal study schedule
- **Data Collection**: Track user behavior (tasks completed, time spent, flashcard reviews)
- **Visualization**: Charts showing trends over time (weekly, monthly, yearly)

---

## **3. LANGUAGE LEARNING FEATURE** 📚🌐

### **3.1 YouTube Content Integration**
- **Multiple Input Methods**:
  - **Auto-Fetch**: Paste YouTube video URL → auto-extract subtitle/transcript
  - **Manual Upload**: Upload .srt (subtitle) or .txt (transcript) files
  - **Manual Entry**: Directly type or paste text content
- **Automatic Parsing**: Extract unique words, phrases, and grammar patterns from content

### **3.2 Language Pattern Recognition**
- **Word Extraction**:
  - Extract all unique words from text
  - Show word frequency (most common words highlighted)
  - Filter by part of speech (nouns, verbs, adjectives, etc.)
- **Grammar Pattern Detection**:
  - Identify common sentence structures
  - Flag complex grammar patterns for study
  - Group by grammar concept (tenses, conditionals, etc.)
- **Language Support**: English & Korean with language-specific NLP processing

### **3.3 Vocabulary Management**
- **Auto-Create Flashcards**: Generate flashcards from extracted vocabulary
  - Front: English word/phrase
  - Back: Translation + example sentence from source
  - Tag: Source video/document
- **Intelligent Filtering**:
  - Filter by difficulty level
  - Hide common words (top 1000 most common)
  - Show only "interesting" or "challenging" vocabulary

### **3.4 Language-Specific Tools**
- **English Learning**:
  - Pronunciation guide (phonetic transcription)
  - Word definitions from multiple sources
  - Synonyms & antonyms
  - Example sentences from YouTube context
- **Korean Learning**:
  - Romanization (how to read in Latin characters)
  - Pronunciation guide (IPA + Korean phonetics)
  - Character breakdown (Hangul decomposition)
  - Grammar pattern analysis for Korean syntax

---

## **4. TECHNICAL STACK** 💻

### **4.1 Frontend**
- **Framework**: HTML5 + JavaScript (Vanilla or lightweight framework)
- **Styling**: Tailwind CSS (utility-first, no custom CSS)
- **UI Components**: Responsive design, mobile-friendly
- **Features**: Real-time updates, smooth animations, dark mode support
- **State Management**: Simple client-side state or localStorage for persistence

### **4.2 Backend**
- **Framework**: Python (Flask/FastAPI) OR Node.js (Express)
- **API**: RESTful API with JSON responses
- **Endpoints**: Tasks, Notes, Flashcards, Analytics, Notifications, Settings
- **Authentication**: Simple token-based (for future expansion)

### **4.3 Database**
- **Primary**: PostgreSQL (structured data - tasks, notes, flashcards, user stats)
- **Caching**: Redis (for session management & real-time notifications)
- **Alternative**: SQLite for simpler local setup, migrate to PostgreSQL later

### **4.4 Machine Learning**
- **Libraries**: 
  - scikit-learn (pattern analysis, clustering)
  - pandas & numpy (data processing)
  - matplotlib & plotly (visualizations)
- **NLP for Language Learning**:
  - NLTK (English text processing)
  - KoNLPy (Korean text processing)
  - spaCy (advanced NLP features)
- **YouTube Integration**: youtube-transcript-api (Python library)

### **4.5 Email Service**
- **SMTP Integration**: Support Gmail, Outlook, custom SMTP servers
- **Email Templates**: HTML-based templates for notifications
- **Scheduling**: APScheduler (Python) or node-cron (Node.js) for scheduled emails
- **Alternative**: SendGrid API (if SMTP too complex)

### **4.6 Deployment**
- **Docker**: Containerize entire app (Frontend + Backend + Database)
- **Docker Compose**: Orchestrate multi-container setup
- **ngrok**: Tunneling for external access (optional, for mobile testing or sharing)
- **Port Configuration**: Frontend (3000), Backend (5000), Database (5432)

### **4.7 Google Calendar MCP Server**
- **Integration**: Connect via MCP protocol
- **Functionality**:
  - Read events from Google Calendar
  - Create/update events from tasks
  - Two-way sync (update task deadline → updates calendar event)
- **Authentication**: OAuth 2.0 for secure Google Calendar access

---

## **5. FEATURE BREAKDOWN BY PRIORITY** 🎯

### **PHASE 1 - MVP (Week 1-2)**
- ✅ Task management (create, view, update, delete, set deadlines)
- ✅ Basic notes system (CRUD)
- ✅ Simple database (PostgreSQL or SQLite)
- ✅ Web UI with Tailwind CSS
- ✅ Docker setup

### **PHASE 2 - Core Features (Week 3)**
- ✅ Flashcard system with spaced repetition
- ✅ Email notifications (basic reminders)
- ✅ Google Calendar MCP integration
- ✅ YouTube transcript extraction

### **PHASE 3 - AI & Analytics (Week 4)**
- ✅ ML analytics dashboard (productivity patterns)
- ✅ Language learning analytics
- ✅ Grammar pattern recognition
- ✅ Advanced email notifications (daily summaries, weekly reports)

### **PHASE 4 - Polish (Week 5+)**
- ✅ Dark mode, mobile optimization
- ✅ ngrok tunneling setup
- ✅ Advanced visualizations & recommendations
- ✅ User preferences & customization

---

## **6. DATABASE SCHEMA** 🗄️

### **Core Tables**
```
Users
├── id (PK)
├── email
├── created_at
└── preferences (JSON: notifications, theme, language)

Tasks
├── id (PK)
├── user_id (FK)
├── title
├── description
├── category (work/study/learning/personal)
├── deadline
├── priority (high/medium/low)
├── status (not_started/in_progress/completed/archived)
├── estimated_duration (minutes)
├── created_at
└── updated_at

Notes
├── id (PK)
├── user_id (FK)
├── title
├── content (rich text)
├── tags (JSON array)
├── created_at
└── updated_at

Flashcard_Decks
├── id (PK)
├── user_id (FK)
├── name
├── language (english/korean)
├── source_type (youtube/manual/upload)
├── created_at

Flashcards
├── id (PK)
├── deck_id (FK)
├── front (question/word)
├── back (answer/translation)
├── ease_factor (SM-2 algorithm)
├── interval (days until next review)
├── repetitions (how many times reviewed)
├── last_reviewed (timestamp)
└── next_review (timestamp)

Language_Vocabulary
├── id (PK)
├── user_id (FK)
├── word
├── language (english/korean)
├── translation
├── frequency_count
├── source_url (YouTube link)
├── learned (boolean)
└── date_learned

Productivity_Analytics
├── id (PK)
├── user_id (FK)
├── date
├── tasks_completed
├── tasks_total
├── category_breakdown (JSON)
├── time_spent (by category)
└── completion_rate

Language_Progress
├── id (PK)
├── user_id (FK)
├── language
├── date
├── words_learned
├── flashcard_accuracy
├── time_spent
└── topics_studied
```

---

## **7. API ENDPOINTS** 🔌

### **Tasks**
- `POST /api/tasks` - Create task
- `GET /api/tasks` - List all tasks (with filters)
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `GET /api/tasks/upcoming` - Get upcoming tasks (for notifications)

### **Notes**
- `POST /api/notes` - Create note
- `GET /api/notes` - List notes
- `GET /api/notes/search` - Search notes
- `PUT /api/notes/{id}` - Update note
- `DELETE /api/notes/{id}` - Delete note

### **Flashcards**
- `POST /api/decks` - Create flashcard deck
- `GET /api/decks` - List decks
- `POST /api/cards` - Create flashcard
- `GET /api/cards/review/{deck_id}` - Get cards for review
- `PUT /api/cards/{id}/review` - Submit review (quality 0-5)
- `DELETE /api/cards/{id}` - Delete card

### **Language Learning**
- `POST /api/language/extract-youtube` - Extract content from YouTube URL
- `POST /api/language/extract-upload` - Upload transcript file
- `GET /api/language/vocabulary` - Get vocabulary with filters
- `GET /api/language/analytics` - Language learning progress
- `POST /api/language/vocabulary/{id}/mark-learned` - Mark word as learned

### **Analytics**
- `GET /api/analytics/productivity` - Productivity insights & trends
- `GET /api/analytics/language` - Language learning progress
- `GET /api/analytics/dashboard` - Combined dashboard data
- `GET /api/analytics/recommendations` - Study recommendations

### **Notifications**
- `POST /api/notifications/settings` - Update notification preferences
- `GET /api/notifications/queue` - Get pending notifications
- `POST /api/notifications/send-email` - Trigger email send (admin)

### **Google Calendar (MCP)**
- `POST /api/calendar/sync` - Sync Google Calendar
- `POST /api/calendar/task-to-event` - Create calendar event from task
- `GET /api/calendar/events` - Get upcoming calendar events

---

## **8. DEPLOYMENT INSTRUCTIONS** 🐳

### **Docker Setup**
```dockerfile
# Multi-stage setup with:
- Frontend container (Nginx serving static files)
- Backend container (Python/Node API)
- Database container (PostgreSQL)
- Redis container (caching & notifications)
```

### **Docker Compose**
```yaml
# Orchestrate:
- frontend service
- backend service
- postgres service
- redis service
```

### **ngrok Tunneling**
- Optional: Expose local app to internet for mobile testing
- Command: `ngrok http 3000`
- Use case: Test notifications on mobile device

### **Local Setup (No Terminal)**
- Pre-built Docker Desktop GUI
- One-click start script
- Web-based dashboard for monitoring

---

## **9. USER WORKFLOW EXAMPLE** 📖

1. **Morning**: Open app → Dashboard shows today's tasks & language learning progress
2. **Create Task**: "Learn Spanish irregular verbs" with 1-week deadline
3. **YouTube Learning**: Paste Spanish learning video URL → App extracts vocabulary → Auto-creates flashcards
4. **Study**: Review flashcards using spaced repetition algorithm
5. **Notification**: Receive email reminder 1 hour before task deadline
6. **Analytics**: Weekly email with productivity report + language learning progress
7. **Google Calendar**: Task deadline automatically appears in Google Calendar
8. **Insights**: Dashboard shows patterns: "You learn best between 9-11 AM" or "Vocabulary retention is 85%"

---

## **10. SUCCESS METRICS** 📊

- ✅ All tasks sync with Google Calendar
- ✅ Email notifications arrive on time (0 false positives)
- ✅ Flashcard SM-2 algorithm improves retention by 30%
- ✅ YouTube vocabulary extraction works for English & Korean
- ✅ ML analytics correctly identify productivity patterns
- ✅ App runs entirely locally without terminal input
- ✅ Docker container starts with single command
- ✅ Mobile-responsive design works on all devices

---

## **11. TECH STACK SUMMARY** 🛠️

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, Tailwind CSS, JavaScript (Vanilla/Alpine.js) |
| **Backend** | Python FastAPI OR Node.js Express |
| **Database** | PostgreSQL + Redis |
| **ML/Analytics** | scikit-learn, pandas, matplotlib, plotly |
| **NLP** | NLTK, KoNLPy, spaCy |
| **YouTube** | youtube-transcript-api |
| **Email** | SMTP + APScheduler (Python) or node-cron |
| **Deployment** | Docker + Docker Compose |
| **Tunneling** | ngrok (optional) |
| **Calendar** | Google Calendar API + MCP |

---

## **12. NEXT STEPS** ✅

1. **Confirm priorities**: Which features matter most?
2. **Choose backend**: Python (Flask/FastAPI) or Node.js?
3. **Database decision**: PostgreSQL from start or SQLite → PostgreSQL migration?
4. **Timeline**: How many weeks can you dedicate?
5. **Email provider**: Gmail SMTP or SendGrid API?
6. **Notification frequency**: How often should reminders be sent?

---

**This specification is now READY FOR DEVELOPMENT!** 🚀

Would you like me to start building any specific component?
