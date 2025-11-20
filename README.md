# 🎓 EduAssist AI - Multi-Agent Educational Support System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-blue.svg)](https://google.github.io/adk-docs/)
[![Kaggle Competition](https://img.shields.io/badge/Kaggle-Capstone-orange.svg)](https://www.kaggle.com/competitions/agents-intensive-capstone-project)

> **A sophisticated multi-agent AI system leveraging Google's Agent Development Kit (ADK) to provide comprehensive educational support through intelligent, collaborative agents.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Development](#development)
- [Deployment](#deployment)
- [Evaluation](#evaluation)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## 🎯 Overview

**EduAssist AI** is a capstone project for the [Google 5-Day AI Agents Intensive Course](https://www.kaggle.com/learn-guide/5-day-agents), submitted under the **"Agents for Good - Education"** track. 

The system uses a multi-agent architecture powered by Google's Agent Development Kit (ADK) and Gemini models to provide:
- 🧠 **Personalized Learning Assistance**
- 📅 **Intelligent Study Planning**
- 💚 **Mental Wellness Support**
- 📚 **Smart Resource Discovery**

---

## 🔴 The Problem

Students worldwide face critical challenges:

1. **Fragmented Learning Support**: Educational tools operate in silos
2. **Generic Guidance**: One-size-fits-all approaches fail individual needs
3. **Mental Health Crisis**: Limited accessible wellness support for students
4. **Information Overload**: Difficulty finding relevant, quality resources
5. **Planning Inefficiency**: Poor study schedule management leads to burnout

**Impact**: Lower academic performance, increased stress, and educational inequality.

---

## ✅ The Solution

**EduAssist AI** employs a **multi-agent system** where specialized AI agents collaborate to provide holistic educational support:

### Why Multi-Agent?

- **Specialization**: Each agent masters one domain (learning, planning, wellness, resources)
- **Scalability**: Add new agents without redesigning the system
- **Resilience**: If one agent fails, others continue functioning
- **Personalization**: Agents learn from interactions and adapt
- **Efficiency**: Parallel processing for faster responses

### How It Works

```
Student Query → Coordinator Agent → Route to Specialist(s) → Coordinated Response
```

The **Coordinator Agent** intelligently routes requests to:
1. **Learning Assistant Agent**: Explains concepts, generates practice problems
2. **Study Planner Agent**: Creates personalized schedules
3. **Wellness Coach Agent**: Provides mental health support
4. **Resource Finder Agent**: Discovers curated learning materials

---

## 🏗️ Architecture

### High-Level System Design

```
┌──────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                            │
│           (CLI / Web API / Future: Mobile App)               │
└────────────────────┬─────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────┐
│              COORDINATOR AGENT (Root LLM Agent)              │
│  • Analyzes user intent                                      │
│  • Routes to appropriate specialist agent(s)                 │
│  • Synthesizes multi-agent responses                         │
└──┬─────────┬─────────┬─────────┬──────────────────────────────┘
   │         │         │         │
   ▼         ▼         ▼         ▼
┌─────┐  ┌─────┐  ┌─────┐  ┌──────────┐
│Learn│  │Study│  │Well.│  │Resource  │  ← Specialized Sub-Agents
│Asst │  │Plan │  │Coach│  │Finder    │
└──┬──┘  └──┬──┘  └──┬──┘  └────┬─────┘
   │        │        │          │
   └────────┴────────┴──────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────┐
│                   SHARED INFRASTRUCTURE                       │
│  • Session Management (InMemorySessionService)               │
│  • State Persistence (User prefs, progress, history)         │
│  • Memory Bank (Long-term knowledge storage)                 │
│  • Logging & Observability (Event tracking, metrics)         │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│                        TOOLS LAYER                            │
│  • Google Search (Built-in)                                  │
│  • Code Execution (Built-in)                                 │
│  • Study Schedule Creator (Custom)                           │
│  • Progress Tracker (Custom)                                 │
│  • Wellness Assessment (Custom)                              │
│  • Resource Recommender (Custom)                             │
└──────────────────────────────────────────────────────────────┘
```

### Agent Hierarchy

```
root_agent (Coordinator)
│
├── learning_assistant_agent (Sequential Workflow)
│   ├── concept_explainer (LLM Agent)
│   └── practice_generator (LLM Agent + Code Execution)
│
├── study_planner_agent (LLM Agent)
│   └── Tools: schedule_creator, progress_tracker
│
├── wellness_coach_agent (LLM Agent)
│   └── Tools: wellness_check, mood_tracker
│
└── resource_finder_agent (Parallel Workflow)
    ├── academic_search (LLM Agent + Google Search)
    └── video_search (LLM Agent + Google Search)
```

---

## ✨ Features

### 🎓 Core Capabilities

1. **Intelligent Concept Explanation**
   - Adaptive difficulty levels
   - Multiple explanation styles (visual, textual, examples)
   - Follow-up clarifications

2. **Personalized Study Planning**
   - AI-generated schedules based on goals and availability
   - Deadline-aware task prioritization
   - Pomodoro technique integration

3. **Mental Wellness Support**
   - Stress level assessment
   - Coping strategies and mindfulness exercises
   - Study-life balance recommendations

4. **Smart Resource Discovery**
   - Curated educational content
   - Multi-source aggregation (articles, videos, tutorials)
   - Quality-ranked results

### 🔧 Technical Features

#### Multi-Agent System
- ✅ **Hierarchical agent structure** (1 coordinator + 4 specialists)
- ✅ **Sequential workflows** (Learning Assistant pipeline)
- ✅ **Parallel workflows** (Resource Finder concurrent searches)
- ✅ **Loop agents** (Iterative problem-solving)

#### Tools Integration
- ✅ **Built-in Google Search** for web information
- ✅ **Code Execution** for generating/testing code examples
- ✅ **4 Custom Function Tools** for specialized tasks
- ✅ **MCP-ready architecture** for future integrations

#### Memory & State Management
- ✅ **Session Management** via InMemorySessionService
- ✅ **Persistent State** for user preferences and progress
- ✅ **Memory Bank** for long-term knowledge storage
- ✅ **Context Engineering** for efficient token usage

#### Observability
- ✅ **Structured Logging** at all agent levels
- ✅ **Event Tracking** for all interactions
- ✅ **Performance Metrics** (latency, token usage)
- ✅ **Error Monitoring** with detailed traces

#### Evaluation & Testing
- ✅ **Automated Agent Evaluation** framework
- ✅ **Response Quality Tests** with ground truth
- ✅ **Tool Usage Validation**
- ✅ **Multi-Agent Coordination Tests**

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- Google Cloud account (for Gemini API)
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/eduassist-ai.git
cd eduassist-ai
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Set Up API Keys

Create a `.env` file in the project root:

```bash
# .env
GOOGLE_API_KEY=your_gemini_api_key_here
PROJECT_ID=your_google_cloud_project_id
```

To get your Gemini API key:
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create or select a project
4. Copy the API key

---

## ⚡ Quick Start

### Running the Interactive CLI

```bash
# Start the interactive agent
python src/main.py

# Or using the ADK web interface
adk web --agent src/agents/coordinator_agent.py
```

### Example Interaction

```
You: Explain binary search trees in simple terms

Agent: [Learning Assistant] A Binary Search Tree (BST) is like an organized 
filing cabinet for numbers...
[Provides detailed explanation with examples]

You: Create a 2-week study plan for data structures

Agent: [Study Planner] I've created a comprehensive 2-week plan:
Week 1: Arrays, Linked Lists, Stacks, Queues
Week 2: Trees, Graphs, Hash Tables
[Detailed schedule with daily goals]

You: I'm feeling stressed about exams

Agent: [Wellness Coach] I understand exam stress can be overwhelming. 
Let's try a few techniques...
[Provides breathing exercises and stress management tips]
```

---

## 📖 Usage Examples

### Example 1: Learning Assistance

```python
from src.agents import coordinator_agent
from google.adk.orchestration import Runner
from google.generativeai.types import content_types

runner = Runner(root_agent=coordinator_agent)

message = content_types.Content(
    role="user",
    parts=["Explain recursion with examples and generate practice problems"]
)

response = runner.run(
    user_id="student_123",
    session_id="session_456",
    content=message
)

# Agent explains recursion, provides examples, and generates 3 practice problems
```

### Example 2: Study Planning

```python
query = "Create a study plan for GATE 2026 CS preparation, 4 hours daily, 6 months timeline"

response = runner.run(
    user_id="student_123",
    session_id="session_456",
    content=content_types.Content(role="user", parts=[query])
)

# Agent generates detailed 6-month schedule with weekly breakdown
```

### Example 3: Multi-Agent Collaboration

```python
query = """
I need help with:
1. Understanding dynamic programming
2. Planning my study for this week
3. Finding good DP tutorials
"""

# Coordinator routes to multiple agents in parallel
# Returns coordinated response combining all specialist outputs
```

---

## 📁 Project Structure

```
eduassist-ai/
│
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── coordinator_agent.py       # Root coordinator agent
│   │   ├── learning_assistant.py      # Learning specialist
│   │   ├── study_planner.py          # Study planning agent
│   │   ├── wellness_coach.py         # Wellness support agent
│   │   └── resource_finder.py        # Resource discovery agent
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── schedule_creator.py       # Custom study schedule tool
│   │   ├── progress_tracker.py       # Progress tracking tool
│   │   ├── wellness_check.py         # Wellness assessment tool
│   │   └── resource_recommender.py   # Resource recommendation tool
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── session_service.py        # Session management
│   │   └── memory_service.py         # Memory bank integration
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py                 # Logging configuration
│   │   └── config.py                 # Configuration management
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── evaluator.py              # Agent evaluation framework
│   │   └── test_cases.py             # Evaluation test cases
│   │
│   └── main.py                        # Main entry point
│
├── tests/
│   ├── test_agents.py                 # Agent unit tests
│   ├── test_tools.py                  # Tool unit tests
│   └── test_integration.py            # Integration tests
│
├── deployment/
│   ├── Dockerfile                     # Container configuration
│   ├── cloudbuild.yaml               # Cloud Build config
│   └── service.yaml                  # Cloud Run service config
│
├── docs/
│   ├── ARCHITECTURE.md               # Detailed architecture
│   ├── API_DOCUMENTATION.md          # API reference
│   ├── DEPLOYMENT_GUIDE.md           # Deployment instructions
│   └── DEMO_SCRIPT.md                # Video demo script
│
├── .env.example                       # Environment variables template
├── .gitignore
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── LICENSE
└── pyproject.toml                    # Project metadata
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=          # Gemini API key from Google AI Studio
PROJECT_ID=              # Google Cloud Project ID (optional)

# Optional
LOG_LEVEL=INFO           # Logging level (DEBUG, INFO, WARNING, ERROR)
SESSION_TIMEOUT=3600     # Session timeout in seconds
MAX_RETRIES=3           # Max retries for API calls
```

### Agent Configuration

Edit `src/utils/config.py` to customize:

```python
# Model selection
MODEL_NAME = "gemini-2.0-flash-exp"

# Agent behavior
MAX_TOKENS = 2048
TEMPERATURE = 0.7

# Session settings
SESSION_EXPIRY_HOURS = 24
```

---

## 🛠️ Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agents.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Adding a New Agent

1. Create agent file in `src/agents/`
2. Implement using ADK Agent class
3. Register in coordinator_agent.py sub_agents list
4. Add tests in `tests/test_agents.py`

Example:

```python
from google.adk.agents import Agent

new_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="new_specialist_agent",
    description="Handles X domain",
    instruction="You are an expert in X...",
    tools=[tool1, tool2]
)
```

---

## 🚢 Deployment

### Local Deployment

```bash
# Run locally
python src/main.py

# Or use ADK web UI
adk web --agent src/agents/coordinator_agent.py --port 8000
```

### Cloud Run Deployment

```bash
# Build container
gcloud builds submit --config=deployment/cloudbuild.yaml

# Deploy to Cloud Run
gcloud run deploy eduassist-ai \
  --image gcr.io/YOUR_PROJECT_ID/eduassist-ai:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY
```

### Using Docker

```bash
# Build image
docker build -t eduassist-ai -f deployment/Dockerfile .

# Run container
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  eduassist-ai
```

For detailed deployment instructions, see [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md).

---

## 📊 Evaluation

### Running Evaluation Framework

```bash
# Run automated evaluation
python src/evaluation/evaluator.py

# Generate evaluation report
python src/evaluation/evaluator.py --report
```

### Evaluation Metrics

The system evaluates:
- **Response Quality**: Accuracy, relevance, completeness
- **Tool Usage**: Appropriate tool selection and execution
- **Multi-Agent Coordination**: Effective collaboration
- **Performance**: Latency, token efficiency

### Example Results

```
Evaluation Report
=================
Total Test Cases: 50
Passed: 47 (94%)
Failed: 3 (6%)

Average Response Time: 2.3s
Average Token Usage: 450 tokens/response
Tool Success Rate: 96%
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- Tests pass (`pytest`)
- Documentation is updated

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google's 5-Day AI Agents Intensive Course** for excellent training and inspiration
- **Kaggle Community** for support and collaboration
- **Google Agent Development Kit (ADK)** team for the powerful framework
- **Open-source contributors** whose tools made this possible

---

## 📞 Contact & Links

- **Developer**: Your Name
- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn Profile]
- **Project Demo**: [YouTube Video Link]
- **Live Demo**: [Cloud Run URL]

---

## 📚 Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Gemini API Guide](https://ai.google.dev/gemini-api/docs)
- [Kaggle Competition](https://www.kaggle.com/competitions/agents-intensive-capstone-project)
- [Course Materials](https://www.kaggle.com/learn-guide/5-day-agents)

---

## 🎬 Demo Video

Watch the 3-minute demo: [YouTube Link - Coming Soon]

### Demo Highlights:
- System architecture walkthrough
- Live agent interactions
- Multi-agent collaboration demo
- Real-world use case scenarios

---

## 📈 Roadmap

### Phase 1 (Current - v1.0)
- ✅ Multi-agent system architecture
- ✅ 4 specialized agents
- ✅ Custom tools integration
- ✅ Session & memory management
- ✅ Evaluation framework

### Phase 2 (v2.0 - Q1 2026)
- 🔄 A2A protocol integration
- 🔄 PostgreSQL memory persistence
- 🔄 RESTful API endpoints
- 🔄 Enhanced observability (Grafana/Prometheus)

### Phase 3 (v3.0 - Q2 2026)
- 📅 Mobile applications (iOS/Android)
- 📅 Voice interface support
- 📅 Multilingual support (Hindi, Tamil, Telugu, Bengali)
- 📅 Advanced gamification

---

**Built with ❤️ for students worldwide | Powered by Google ADK & Gemini**
