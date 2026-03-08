# 🔀 LLM-Powered Prompt Router

> An intelligent AI routing system that classifies user intent and delegates requests to specialized expert personas for high-quality, context-aware responses.

**Built by Mohammad Riyaz** | Powered by Groq + Llama 3.3

---

## 🎯 What is this?

Instead of using one generic AI prompt for everything, this system uses a **two-step classify → respond** pattern:

1. **Classify** — A fast LLM call detects the user's intent
2. **Route** — The request is sent to a specialized expert persona
3. **Respond** — A focused, high-quality response is generated

This is the same pattern used by production AI tools like GitHub Copilot, Notion AI, and Intercom Fin.

---

## 🏗️ Architecture

```
User Message
     │
     ▼
┌─────────────────────┐
│  classify_intent()  │  ← Fast LLM call → {"intent": "code", "confidence": 0.97}
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  route_and_respond()│  ← Selects expert persona → generates response
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│   log_route()       │  ← Appends to route_log.jsonl
└─────────────────────┘
     │
     ▼
Final Response to User
```

---

## 🤖 Expert Domains (8 Total)

| Intent | Expert | Handles |
|--------|--------|---------|
| `code` | 🧑‍💻 Code Expert | Programming, debugging, SQL, algorithms |
| `data` | 📊 Data Analyst | Statistics, datasets, trends, visualization |
| `writing` | ✍️ Writing Coach | Grammar, tone, clarity, text feedback |
| `career` | 💼 Career Advisor | Jobs, resume, interviews, cover letters |
| `general` | 🌍 General Knowledge | History, science, geography, world facts |
| `chat` | 💬 Chat Assistant | Casual conversation, small talk |
| `math` | 🔢 Math Expert | Calculations, algebra, equations |
| `health` | 💪 Health Advisor | Fitness, nutrition, wellness |
| `unclear` | 🤔 Clarifier | Asks clarifying question |

---

## ✨ Features

- ✅ **Intent Classification** — Fast LLM call with JSON output
- ✅ **8 Expert Personas** — Specialized system prompts per domain
- ✅ **Confidence Threshold** — Low confidence → ask for clarification
- ✅ **Conversation Memory** — Remembers last 6 messages for context
- ✅ **Manual Override** — Prefix with `@code`, `@data`, etc.
- ✅ **Request Logging** — Every request logged to `route_log.jsonl`
- ✅ **Graceful Error Handling** — Never crashes on bad JSON
- ✅ **Web UI** — Beautiful dark-themed chat interface
- ✅ **CLI Interface** — Terminal-based interaction
- ✅ **Docker Support** — Fully containerized

---

## 📁 Project Structure

```
prompt-router/
├── prompts.py          # All 8 expert system prompts + classifier prompt
├── router.py           # classify_intent() + route_and_respond() + logging
├── main.py             # Interactive CLI
├── app.py              # Flask Web UI
├── test_router.py      # Full test suite (20 test cases)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker setup
├── docker-compose.yml  # Docker Compose setup
├── .env.example        # API key template
├── .gitignore          # Git ignore rules
└── templates/
    └── index.html      # Web UI template
```

---

## 🚀 Quick Start

### Option 1 — Local Python

**Step 1: Clone the repo**
```bash
git clone https://github.com/riyaz7799/prompt-router.git
cd prompt-router
```

**Step 2: Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Set up API key**
```bash
copy .env.example .env
```

Open `.env` and add your Groq API key:
```
GROQ_API_KEY=gsk_your-key-here
```

Get a free Groq API key at 👉 **console.groq.com**

**Step 5: Run the web app**
```bash
python app.py
```

Open 👉 **http://localhost:5000**

**Step 6: Or run CLI**
```bash
python main.py
```

---

### Option 2 — Docker

**Step 1: Build image**
```bash
docker build -t prompt-router .
```

**Step 2: Run web app**
```bash
docker run -it -p 5000:5000 -e GROQ_API_KEY=your-key-here prompt-router python app.py
```

**Step 3: Run tests**
```bash
docker run --rm -e GROQ_API_KEY=your-key-here prompt-router python test_router.py
```

**Or use Docker Compose:**
```bash
GROQ_API_KEY=your-key-here docker-compose up
```

---

## 🧪 Running Tests

```bash
python test_router.py
```

**Test Results: 18/20 passing ✅**

Test cases include:
- Clear intent messages (code, data, writing, career)
- Ambiguous and multi-intent messages
- Edge cases (empty input, single character, typos)
- Manual override tests
- Long paragraph inputs

---

## 💬 Usage Examples

### Web UI
Visit `http://localhost:5000` and type any message!

### CLI
```bash
python main.py
```

### Manual Override
Bypass the classifier by prefixing with `@intent`:
```
@code fix this bug: for i in range(10) print(i)
@career how do I negotiate my salary?
@math what is 25 times 48?
@health how many calories should I eat per day?
```

---

## 📊 Sample Interactions

| Input | Intent | Confidence |
|-------|--------|------------|
| `how do I sort a list in python?` | 🧑‍💻 code | 98% |
| `what is the average of 12, 45, 23?` | 📊 data | 99% |
| `my paragraph sounds awkward` | ✍️ writing | 96% |
| `tips for my job interview` | 💼 career | 96% |
| `who invented the telephone?` | 🌍 general | 97% |
| `hey how are you?` | 💬 chat | 99% |
| `what is 25 x 48?` | 🔢 math | 99% |
| `how many calories in an egg?` | 💪 health | 96% |
| `can you write me a poem?` | 🤔 unclear | 97% |

---

## 📝 Route Log

Every request is automatically logged to `route_log.jsonl`:

```bash
# View last entry
tail -1 route_log.jsonl

# Pretty print
tail -1 route_log.jsonl | python -m json.tool
```

**Example log entry:**
```json
{
  "timestamp": "2026-03-08T10:22:15Z",
  "user_message": "how do I sort a list in python?",
  "intent": "code",
  "confidence": 0.98,
  "final_response": "Here's how to sort a list..."
}
```

---

## ⚙️ Configuration

Edit these in `router.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `CLASSIFIER_MODEL` | `llama-3.3-70b-versatile` | Model for classification |
| `GENERATION_MODEL` | `llama-3.3-70b-versatile` | Model for responses |
| `CONFIDENCE_THRESHOLD` | `0.65` | Below this → unclear |
| `LOG_FILE` | `route_log.jsonl` | Log file path |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **LLM API:** Groq (Llama 3.3 70B) — Free tier
- **Web Framework:** Flask
- **Container:** Docker
- **Libraries:** openai, flask, python-dotenv

---

## 📋 Requirements Met

| Requirement | Status |
|-------------|--------|
| 4+ expert system prompts | ✅ (8 prompts) |
| `classify_intent()` with JSON output | ✅ |
| `route_and_respond()` routing | ✅ |
| Unclear intent asks clarification | ✅ |
| Logging to `route_log.jsonl` | ✅ |
| Graceful error handling | ✅ |
| Confidence threshold | ✅ |
| Manual `@intent` override | ✅ |
| Web UI | ✅ |
| Docker support | ✅ |
| 15+ test messages | ✅ (20 tests) |

---

## 👨‍💻 Author

**Mohammad Riyaz**
- GitHub: [@riyaz7799](https://github.com/riyaz7799)

---

## 📄 License

MIT License — feel free to use and modify!