# 🚀 Quick Start Guide
## EduAssist AI - From Zero to Running in 15 Minutes

This guide will get you up and running with EduAssist AI quickly.

---

## ⚡ Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.10 or higher installed
- [ ] Git installed
- [ ] Google account (for Gemini API)
- [ ] Terminal/Command prompt access
- [ ] Text editor or IDE (VS Code recommended)

---

## 📦 Installation Steps

### Step 1: Get the Code (2 minutes)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/eduassist-ai-capstone.git
cd eduassist-ai-capstone
```

### Step 2: Set Up Python Environment (3 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Dependencies (5 minutes)

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note**: This will install:
- Google ADK and AI libraries
- Python utilities and tools
- Testing and development tools

### Step 4: Get Your API Key (3 minutes)

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key" button
3. Create a new project or select existing
4. Copy your API key

### Step 5: Configure Environment (2 minutes)

```bash
# Create .env file from template
cp .env.example .env

# Edit .env file and add your API key
# On macOS/Linux:
nano .env
# On Windows:
notepad .env
```

Add your API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

Save and close the file.

---

## ▶️ Running the Application

### Option 1: Interactive CLI (Recommended for Testing)

```bash
# Run the complete implementation
python complete_implementation.py
```

You should see:
```
🎓 Welcome to EduAssist AI - Multi-Agent Educational Support System
════════════════════════════════════════════════════════════════════

I'm here to help you with:
  📚 Learning assistance and concept explanations
  📅 Study planning and time management
  💚 Mental wellness and stress management
  🔍 Finding quality educational resources

Type 'exit' or 'quit' to end the session
Type 'help' for example questions
════════════════════════════════════════════════════════════════════

🧑 You: _
```

### Option 2: ADK Web Interface (Recommended for Demo)

```bash
# Navigate to src directory
cd src

# Start ADK web server
adk web --agent agents/coordinator_agent.py --port 8000
```

Then open browser to: `http://localhost:8000`

---

## 🎮 Try These Example Queries

Once running, try these to test all agents:

### Learning Assistant Examples:
```
Explain binary search trees in simple terms

How does recursion work? Give me examples

Generate practice problems for sorting algorithms
```

### Study Planner Examples:
```
Create a 2-week study plan for data structures, 3 hours daily

Help me prepare for GATE 2026, I have 6 months

Track my progress on learning Python
```

### Wellness Coach Examples:
```
I'm feeling stressed about upcoming exams

How can I avoid burnout while studying?

Assess my wellness: stress level 7, sleeping 5 hours, rarely exercise
```

### Resource Finder Examples:
```
Find good resources for learning machine learning

Best tutorials for beginner Python programmers

Recommend intermediate level algorithms courses
```

### Multi-Agent Examples:
```
I need to learn graph algorithms, create a study plan, and find resources

Explain dynamic programming, help me schedule practice, and find good tutorials
```

---

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] No errors during installation
- [ ] Application starts without errors
- [ ] Can interact with the system
- [ ] Learning Assistant responds appropriately
- [ ] Study Planner can create schedules
- [ ] Wellness Coach provides support
- [ ] Resource Finder discovers materials
- [ ] Multi-agent queries work
- [ ] Session maintains context

---

## 🐛 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"

**Solution**:
```bash
# Verify .env file exists
ls -la .env

# Check contents (API key should be there)
cat .env

# Ensure no spaces around = sign
GOOGLE_API_KEY=your_key_here  # ✅ Correct
GOOGLE_API_KEY = your_key_here  # ❌ Wrong
```

### Issue: "Module not found" errors

**Solution**:
```bash
# Ensure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall requirements
pip install -r requirements.txt

# Verify ADK is installed
pip show google-adk
```

### Issue: "Rate limit exceeded"

**Solution**:
- You're making too many requests
- Wait a few minutes and try again
- Check your API quota at [Google AI Studio](https://aistudio.google.com/)

### Issue: Slow responses

**Solution**:
- This is normal for first request (model initialization)
- Subsequent requests should be faster
- Check your internet connection

### Issue: Import errors in complete_implementation.py

**Solution**:
```bash
# Make sure you're in the project root directory
pwd  # Should show /path/to/eduassist-ai-capstone

# Run from project root
python complete_implementation.py
```

---

## 📊 Testing the System

### Basic Functionality Test

```python
# Save this as test_basic.py
from complete_implementation import coordinator_agent
from google.adk.orchestration import Runner
from google.adk.orchestration.session import InMemorySessionService
from google.generativeai.types import content_types
import uuid

# Setup
session_service = InMemorySessionService()
runner = Runner(root_agent=coordinator_agent, session_service=session_service)

# Create session
user_id = "test_user"
session_id = "test_session"
session_service.create_session(
    app_name="eduassist_ai",
    user_id=user_id,
    session_id=session_id,
    state={}
)

# Test query
message = content_types.Content(
    role="user",
    parts=["Explain binary search in simple terms"]
)

response = runner.run(
    user_id=user_id,
    session_id=session_id,
    content=message
)

# Check response
for event in response.events:
    if event.type == "content" and event.content.role == "agent":
        print("✅ System working! Response:", event.content.parts[0].text[:100] + "...")
```

Run test:
```bash
python test_basic.py
```

---

## 🎯 Next Steps

Once you have the system running:

1. **Explore All Agents**: Try queries for each specialist agent
2. **Test Multi-Agent**: Try queries that need multiple agents
3. **Check Session State**: Verify context is maintained across queries
4. **Review Logs**: Check console output for agent activity
5. **Customize**: Modify agent instructions or add new tools
6. **Deploy**: Follow deployment guide for Cloud Run (optional)
7. **Create Video**: Record your demo for submission

---

## 📚 Additional Resources

### Documentation
- Full README: See [README.md](README.md)
- Architecture Details: See [project-overview.md](project-overview.md)
- Submission Guide: See [submission-guide.md](submission-guide.md)

### ADK Resources
- [ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python GitHub](https://github.com/google/adk-python)
- [ADK Samples](https://github.com/google/adk-samples)

### Competition
- [Kaggle Competition Page](https://www.kaggle.com/competitions/agents-intensive-capstone-project)
- [Course Materials](https://www.kaggle.com/learn-guide/5-day-agents)

---

## 💡 Pro Tips

1. **Save Your Sessions**: Session state helps agents remember context
2. **Be Specific**: More detailed queries get better responses
3. **Explore Tools**: Check how custom tools enhance agent capabilities
4. **Monitor Logs**: Console output shows agent decision-making
5. **Iterate**: Try variations of queries to see different responses

---

## 🎓 Learning Path

If you're new to ADK or agents, follow this path:

1. **Day 1**: Get system running, try basic queries
2. **Day 2**: Understand coordinator routing logic
3. **Day 3**: Explore each specialist agent's capabilities
4. **Day 4**: Experiment with multi-agent coordination
5. **Day 5**: Customize agents or add new capabilities

---

## ✉️ Get Help

Having issues? Here's how to get help:

1. **Check Issues**: Review GitHub issues for similar problems
2. **ADK Docs**: Search [ADK documentation](https://google.github.io/adk-docs/)
3. **Kaggle Discord**: Ask in [Kaggle Discord](http://discord.com/invite/kaggle)
4. **Reddit**: Post in [r/agentdevelopmentkit](https://www.reddit.com/r/agentdevelopmentkit/)
5. **Create Issue**: Open issue on GitHub repository

---

## 🎉 You're Ready!

Congratulations! You now have:
- ✅ EduAssist AI running locally
- ✅ Understanding of the system
- ✅ Knowledge to customize and extend
- ✅ Foundation for your capstone submission

Now go explore, experiment, and create something amazing!

**Good luck! 🚀**
