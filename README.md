# 🔍 ReviewBot — AI-Powered Code Review Assistant

> *Paste a GitHub PR. Get expert AI feedback in seconds.*

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![GitHub API](https://img.shields.io/badge/GitHub-API-181717?style=flat-square&logo=github)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple?style=flat-square)

---

## 🚀 What is ReviewBot?

ReviewBot is an AI agent that integrates with GitHub to review Pull Requests in real-time. Developers spend hours manually reviewing PRs — and still miss bugs, security holes, and performance issues. ReviewBot solves this instantly.

Paste any GitHub PR URL → get a full expert-level code review in seconds, powered by AI.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🐛 **Bug Detection** | Finds logic errors, edge cases, and incorrect behavior |
| 🔒 **Security Scanning** | Detects SQL injection, XSS, hardcoded secrets & more |
| ⚡ **Performance Analysis** | Identifies bottlenecks, inefficient loops, memory leaks |
| 🧹 **Code Quality** | Flags code smells, naming issues, missing error handling |
| ✅ **Good Practice Highlights** | Acknowledges what the developer did well |
| 📋 **Actionable Recommendations** | Numbered list of fixes before merging |
| 🏆 **Overall Score** | Rates the PR: Excellent / Good / Needs Work / Major Issues |
| 💬 **Auto-Post to GitHub** | Posts the review directly as a comment on the PR |

---

## 🎯 Problem Statement

Engineering teams waste hours reviewing pull requests manually — and critical bugs, security vulnerabilities, and performance issues still slip through. ReviewBot automates the entire review process using AI, giving developers instant, actionable feedback.

---

## 🛠️ Tech Stack

- **Backend** — Python + Flask
- **AI Engine** — OpenRouter API (LLM-powered review)
- **GitHub Integration** — GitHub REST API v3
- **Frontend** — HTML, CSS, Vanilla JavaScript
- **Environment** — python-dotenv for secure key management

---

## 📸 Demo

1. Paste a GitHub PR URL into ReviewBot
2. Toggle "Post to GitHub" to auto-comment on the PR
3. Click ⚡ Review This PR
4. Get a full structured AI review instantly

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Ayisha-2803/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Install dependencies
```bash
pip install flask requests python-dotenv
```

### 3. Set up environment variables
Create a `.env` file in the root folder:
```
GITHUB_TOKEN=your_github_personal_access_token
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://localhost:5000
```

---

## 🔑 Getting API Keys

- **GitHub Token** → [github.com/settings/tokens](https://github.com/settings/tokens) — select `repo` scope
- **OpenRouter API Key** → [openrouter.ai](https://openrouter.ai) — free tier available, no credit card needed

---

## 📁 Project Structure

```
ai-code-reviewer/
├── app.py              # Flask web server & API routes
├── reviewer.py         # GitHub API + AI review engine
├── templates/
│   └── index.html      # Frontend UI
├── .env                # API keys (never commit this!)
├── .gitignore          # Excludes .env from git
└── README.md
```

---

## 🏆 Hackathon — AI Agent Challenge

Built in 1 day for the AI Agent Hackathon (May 23, 2026).

**Problem:** Developers spend hours reviewing PRs manually, missing bugs and security issues.

**Solution:** An AI agent that connects to GitHub, analyzes code changes, and delivers expert-level reviews instantly.

---

## 👩‍💻 Author

**Ayisha** — [@Ayisha-2803](https://github.com/Ayisha-2803)

---

*Made with ❤️ and a lot of ☕*
