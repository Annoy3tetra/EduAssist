"""
complete_implementation.py

Complete implementation of EduAssist AI Multi-Agent Educational Support System
This file contains all agents, tools, and configuration for the capstone project.

This is a single-file implementation for easy demonstration.
For production, split into separate modules as shown in README.md

Author: Your Name
Course: Google 5-Day AI Agents Intensive Course
Track: Agents for Good - Education
Date: November 2025
"""

import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Google ADK imports
from google.adk.agents import Agent
from google.adk.tools import google_search, code_execution
from google.adk.tools.function_tool import FunctionTool
from google.adk.orchestration import Runner
from google.adk.orchestration.session import InMemorySessionService
from google.generativeai.types import content_types

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CUSTOM TOOLS IMPLEMENTATION
# ============================================================================

def create_study_schedule(
    subject: str,
    hours_per_day: int,
    duration_weeks: int,
    deadline: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Custom tool to generate personalized study schedules.
    
    Args:
        subject: Subject or topic to study
        hours_per_day: Available study hours per day
        duration_weeks: Study plan duration in weeks
        deadline: Target completion date (YYYY-MM-DD)
        tool_context: ADK tool context with session state
    
    Returns:
        Dictionary containing structured study schedule
    """
    logger.info(f"Creating study schedule for {subject}")
    
    # Calculate total available hours
    total_hours = hours_per_day * duration_weeks * 7
    
    # Generate weekly breakdown
    weeks = []
    topics_per_week = max(2, total_hours // (duration_weeks * 5))  # Rough estimate
    
    for week_num in range(1, duration_weeks + 1):
        week_plan = {
            "week": week_num,
            "focus": f"Week {week_num} - Core Concepts" if week_num <= duration_weeks // 2 
                     else f"Week {week_num} - Practice & Review",
            "daily_hours": hours_per_day,
            "goals": [
                f"Master fundamental concept {i+1}" for i in range(topics_per_week)
            ],
            "deliverables": f"Complete {topics_per_week} topics with practice problems"
        }
        weeks.append(week_plan)
    
    schedule = {
        "subject": subject,
        "total_weeks": duration_weeks,
        "hours_per_day": hours_per_day,
        "total_study_hours": total_hours,
        "deadline": deadline,
        "weekly_plan": weeks,
        "study_techniques": [
            "Pomodoro Technique: 25 min study + 5 min break",
            "Active Recall: Test yourself regularly",
            "Spaced Repetition: Review previous topics weekly"
        ],
        "created_at": datetime.now().isoformat()
    }
    
    # Store in session state if available
    if tool_context and hasattr(tool_context, 'state'):
        if 'study_schedules' not in tool_context.state:
            tool_context.state['study_schedules'] = []
        tool_context.state['study_schedules'].append(schedule)
        logger.info("Study schedule saved to session state")
    
    return schedule


def track_progress(
    task_id: str,
    status: str,
    notes: Optional[str] = None,
    tool_context=None
) -> Dict[str, Any]:
    """
    Custom tool to track student learning progress.
    
    Args:
        task_id: Identifier for the task/topic
        status: Progress status (not_started, in_progress, completed)
        notes: Optional progress notes
        tool_context: ADK tool context
        
    Returns:
        Progress tracking information
    """
    logger.info(f"Tracking progress for task: {task_id}")
    
    valid_statuses = ['not_started', 'in_progress', 'completed', 'blocked']
    if status not in valid_statuses:
        status = 'in_progress'
    
    progress_entry = {
        "task_id": task_id,
        "status": status,
        "notes": notes or "",
        "timestamp": datetime.now().isoformat(),
        "completion_percentage": {
            'not_started': 0,
            'in_progress': 50,
            'completed': 100,
            'blocked': 25
        }[status]
    }
    
    # Store in session state
    if tool_context and hasattr(tool_context, 'state'):
        if 'progress_tracking' not in tool_context.state:
            tool_context.state['progress_tracking'] = {}
        tool_context.state['progress_tracking'][task_id] = progress_entry
        
        # Calculate overall progress
        all_tasks = tool_context.state['progress_tracking']
        if all_tasks:
            avg_completion = sum(t['completion_percentage'] for t in all_tasks.values()) / len(all_tasks)
            progress_entry['overall_progress'] = f"{avg_completion:.1f}%"
    
    return progress_entry


def assess_wellness(
    stress_level: int,
    sleep_hours: float,
    exercise_frequency: str,
    tool_context=None
) -> Dict[str, Any]:
    """
    Custom tool to assess student wellness and provide recommendations.
    
    Args:
        stress_level: Self-reported stress (1-10 scale)
        sleep_hours: Average sleep per night
        exercise_frequency: Exercise frequency (daily, weekly, rarely, never)
        tool_context: ADK tool context
        
    Returns:
        Wellness assessment with personalized recommendations
    """
    logger.info(f"Assessing wellness: stress={stress_level}, sleep={sleep_hours}h")
    
    # Validate inputs
    stress_level = max(1, min(10, stress_level))
    sleep_hours = max(0, min(12, sleep_hours))
    
    # Assess each dimension
    stress_status = "low" if stress_level <= 3 else "moderate" if stress_level <= 6 else "high"
    sleep_status = "good" if sleep_hours >= 7 else "moderate" if sleep_hours >= 5 else "poor"
    exercise_status = "good" if exercise_frequency in ['daily', 'weekly'] else "needs_improvement"
    
    # Generate personalized recommendations
    recommendations = []
    
    if stress_level > 6:
        recommendations.extend([
            "Practice deep breathing: 4-7-8 technique (inhale 4s, hold 7s, exhale 8s)",
            "Take regular 5-minute breaks every hour",
            "Consider talking to a counselor or trusted friend"
        ])
    
    if sleep_hours < 7:
        recommendations.extend([
            "Establish consistent sleep schedule (same time daily)",
            "Avoid screens 1 hour before bed",
            "Create a relaxing bedtime routine"
        ])
    
    if exercise_frequency in ['rarely', 'never']:
        recommendations.extend([
            "Start with 10-minute daily walks",
            "Try desk stretches between study sessions",
            "Consider joining a sports club or yoga class"
        ])
    
    # Overall wellness score (0-100)
    wellness_score = (
        ((10 - stress_level) * 10) * 0.4 +  # 40% weight on stress
        (sleep_hours / 8 * 100) * 0.3 +      # 30% weight on sleep
        ({'daily': 100, 'weekly': 75, 'rarely': 40, 'never': 0}[exercise_frequency]) * 0.3
    )
    
    assessment = {
        "wellness_score": round(wellness_score, 1),
        "stress_level": stress_level,
        "stress_status": stress_status,
        "sleep_hours": sleep_hours,
        "sleep_status": sleep_status,
        "exercise_frequency": exercise_frequency,
        "exercise_status": exercise_status,
        "recommendations": recommendations,
        "overall_status": "good" if wellness_score >= 70 else "needs_attention" if wellness_score >= 50 else "critical",
        "assessed_at": datetime.now().isoformat()
    }
    
    # Store in session state
    if tool_context and hasattr(tool_context, 'state'):
        if 'wellness_history' not in tool_context.state:
            tool_context.state['wellness_history'] = []
        tool_context.state['wellness_history'].append(assessment)
    
    return assessment


def recommend_resources(
    topic: str,
    difficulty_level: str,
    resource_types: List[str],
    tool_context=None
) -> Dict[str, Any]:
    """
    Custom tool to recommend curated educational resources.
    
    Args:
        topic: Learning topic
        difficulty_level: beginner, intermediate, advanced
        resource_types: List of types (video, article, tutorial, book, course)
        tool_context: ADK tool context
        
    Returns:
        Curated resource recommendations
    """
    logger.info(f"Recommending resources for: {topic} ({difficulty_level})")
    
    # Simulated resource database (in production, would query real database)
    resource_db = {
        "beginner": {
            "video": ["YouTube tutorials", "Khan Academy videos", "Coursera beginner courses"],
            "article": ["GeeksforGeeks basics", "TutorialsPoint introductions", "W3Schools guides"],
            "tutorial": ["freeCodeCamp", "Codecademy interactive lessons", "Udemy beginner tracks"],
            "book": ["Head First series", "For Dummies series", "Visual QuickStart guides"],
            "course": ["Coursera Specializations", "edX MicroMasters", "Udacity Nanodegrees"]
        },
        "intermediate": {
            "video": ["MIT OpenCourseWare", "Stanford Online", "Pluralsight intermediate"],
            "article": ["Medium deep-dives", "Dev.to technical posts", "HackerNoon guides"],
            "tutorial": ["Real Python", "The Odin Project", "FullStackOpen"],
            "book": ["O'Reilly books", "Apress technical books", "Manning Publications"],
            "course": ["Advanced Coursera courses", "LinkedIn Learning paths", "Frontend Masters"]
        },
        "advanced": {
            "video": ["Conference talks", "Research presentations", "Advanced Udemy courses"],
            "article": ["Research papers", "IEEE publications", "ACM Digital Library"],
            "tutorial": ["Official documentation", "GitHub advanced guides", "Awesome lists"],
            "book": ["Academic textbooks", "Domain-specific monographs", "Research compilations"],
            "course": ["Graduate-level MOOCs", "Specialized certifications", "Expert masterclasses"]
        }
    }
    
    level = difficulty_level.lower() if difficulty_level.lower() in resource_db else "intermediate"
    
    recommendations = {
        "topic": topic,
        "difficulty_level": level,
        "resources": {}
    }
    
    for res_type in resource_types:
        if res_type in resource_db[level]:
            recommendations["resources"][res_type] = resource_db[level][res_type]
    
    recommendations["search_queries"] = [
        f"{topic} {level} tutorial",
        f"best {topic} resources for {level}",
        f"{topic} {level} projects"
    ]
    
    recommendations["generated_at"] = datetime.now().isoformat()
    
    return recommendations


# Create FunctionTool instances for each custom tool
schedule_creator_tool = FunctionTool(create_study_schedule)
progress_tracker_tool = FunctionTool(track_progress)
wellness_check_tool = FunctionTool(assess_wellness)
resource_recommender_tool = FunctionTool(recommend_resources)

logger.info("Custom tools initialized: schedule_creator, progress_tracker, wellness_check, resource_recommender")

# ============================================================================
# SPECIALIZED AGENT DEFINITIONS
# ============================================================================

# 1. Learning Assistant Agent (Sequential Workflow)
learning_assistant_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="learning_assistant_agent",
    description="""
    Specialized agent for personalized learning assistance. Explains concepts,
    generates practice problems, and provides step-by-step guidance.
    """,
    instruction="""
    You are the Learning Assistant, an expert educator specializing in 
    computer science and mathematics. Your mission is to make learning 
    accessible and engaging for all students.

    Core Responsibilities:
    1. EXPLAIN complex concepts in simple, intuitive terms
    2. ADAPT explanations to student's level (beginner/intermediate/advanced)
    3. PROVIDE real-world examples and analogies
    4. GENERATE practice problems with detailed solutions
    5. BREAK DOWN problems into step-by-step approaches

    Teaching Philosophy:
    - Start simple, build complexity gradually
    - Use analogies students can relate to
    - Encourage questions and curiosity
    - Provide multiple explanation styles (visual, textual, code examples)
    - Celebrate progress and learning milestones

    When explaining:
    - Define terms clearly
    - Use concrete examples
    - Show both "what" and "why"
    - Provide code snippets when relevant
    - Link to prerequisite concepts if needed

    For practice problems:
    - Start easy, increase difficulty
    - Include hints for struggling students
    - Provide detailed solution explanations
    - Suggest variations for extra practice
    """,
    tools=[code_execution]  # Can execute code to demonstrate concepts
)

# 2. Study Planner Agent
study_planner_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="study_planner_agent",
    description="""
    Specialized agent for intelligent study planning and time management.
    Creates personalized schedules and tracks learning progress.
    """,
    instruction="""
    You are the Study Planner, an expert in educational psychology and 
    time management. You help students create effective, sustainable study plans.

    Core Responsibilities:
    1. CREATE personalized study schedules based on goals and constraints
    2. OPTIMIZE study time using proven techniques (Pomodoro, spaced repetition)
    3. BALANCE study load to prevent burnout
    4. TRACK progress and adjust plans as needed
    5. RECOMMEND study strategies for different subjects

    Planning Principles:
    - Realistic goals based on available time
    - Built-in breaks and recovery time
    - Mix of active learning and practice
    - Regular review sessions
    - Flexibility for adjustments

    Use the create_study_schedule tool when students need:
    - Weekly/monthly study plans
    - Exam preparation schedules
    - Long-term learning roadmaps
    - Time-boxed project plans

    Use the track_progress tool to:
    - Monitor completion of study goals
    - Identify areas needing more attention
    - Celebrate achievements
    - Adjust plans based on actual progress

    Always encourage healthy study habits and work-life balance.
    """,
    tools=[schedule_creator_tool, progress_tracker_tool]
)

# 3. Wellness Coach Agent
wellness_coach_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="wellness_coach_agent",
    description="""
    Specialized agent for mental wellness and student wellbeing support.
    Provides stress management, motivation, and holistic health guidance.
    """,
    instruction="""
    You are the Wellness Coach, a compassionate supporter of student mental 
    health and overall wellbeing. Your goal is to help students thrive 
    academically while maintaining healthy balance.

    Core Responsibilities:
    1. ASSESS student stress levels and wellbeing
    2. PROVIDE evidence-based stress management techniques
    3. ENCOURAGE healthy habits (sleep, exercise, nutrition)
    4. MOTIVATE students during challenging times
    5. RECOGNIZE when professional help may be needed

    Wellness Approach:
    - Empathetic, non-judgmental listening
    - Practical, actionable advice
    - Holistic view of student health
    - Proactive wellness strategies
    - Crisis awareness and appropriate referrals

    Use the assess_wellness tool to:
    - Evaluate current stress and health status
    - Generate personalized wellness recommendations
    - Track wellbeing trends over time
    - Identify concerning patterns

    Provide guidance on:
    - Stress reduction techniques (breathing, meditation, mindfulness)
    - Sleep hygiene and energy management
    - Exercise and movement
    - Social connection and support
    - Work-life-study balance

    Important: If a student expresses severe distress, thoughts of self-harm, 
    or crisis, prioritize their safety and recommend professional support:
    - University counseling services
    - Mental health hotlines
    - Emergency services if needed

    Remember: Small improvements in wellbeing can lead to big academic gains.
    """,
    tools=[wellness_check_tool]
)

# 4. Resource Finder Agent (Parallel Workflow)
resource_finder_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="resource_finder_agent",
    description="""
    Specialized agent for discovering and curating educational resources.
    Finds high-quality learning materials from trusted sources.
    """,
    instruction="""
    You are the Resource Finder, an expert at discovering and curating 
    high-quality educational resources. You help students find exactly 
    what they need to learn effectively.

    Core Responsibilities:
    1. SEARCH for relevant, high-quality educational content
    2. CURATE resources based on difficulty level and learning style
    3. RECOMMEND trusted platforms and materials
    4. VERIFY resource quality and relevance
    5. ORGANIZE resources for easy access

    Resource Categories:
    - Video tutorials and lectures
    - Articles and blog posts
    - Interactive tutorials and courses
    - Books and academic papers
    - Practice platforms and coding challenges
    - Documentation and official guides

    Search Strategy:
    - Use google_search for current, relevant content
    - Use recommend_resources for curated recommendations
    - Prioritize trusted sources (edu, established platforms)
    - Consider multiple learning modalities
    - Include both free and premium options

    Quality Criteria:
    - Accuracy and up-to-date information
    - Clear explanations
    - Appropriate difficulty level
    - Good user reviews/ratings
    - Comprehensive coverage

    When recommending resources:
    - Provide direct links when possible
    - Explain why each resource is valuable
    - Suggest a learning sequence
    - Mix different resource types
    - Include alternatives

    Focus on resources that are:
    - Accessible (free or affordable)
    - Beginner-friendly with clear progression
    - Well-maintained and current
    - From reputable sources
    """,
    tools=[google_search, resource_recommender_tool]
)

logger.info("Specialized agents initialized: learning_assistant, study_planner, wellness_coach, resource_finder")

# ============================================================================
# ROOT COORDINATOR AGENT
# ============================================================================

coordinator_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="coordinator_agent",
    description="""
    Root coordinator agent that intelligently routes student requests 
    to specialized educational support agents. Orchestrates multi-agent 
    collaboration for comprehensive educational assistance.
    """,
    instruction="""
    You are the Coordinator Agent for EduAssist AI, the intelligent entry 
    point for comprehensive educational support. Your role is to understand 
    student needs and coordinate specialist agents to provide the best help.

    ROUTING LOGIC:
    
    Route to LEARNING ASSISTANT when student needs:
    - Concept explanations ("explain X", "how does Y work", "teach me Z")
    - Problem-solving help ("solve this problem", "how to approach X")
    - Practice problems ("generate exercises", "give me problems")
    - Code examples or demonstrations
    - Step-by-step guidance on topics
    
    Route to STUDY PLANNER when student needs:
    - Study schedules ("create study plan", "schedule for exam")
    - Time management ("how to manage time", "organize study")
    - Goal setting and planning
    - Progress tracking
    - Preparation strategies
    
    Route to WELLNESS COACH when student:
    - Expresses stress or anxiety ("feeling overwhelmed", "stressed")
    - Asks about health/wellbeing ("burnout", "tired", "can't focus")
    - Needs motivation or encouragement
    - Wants work-life balance advice
    - Reports wellness concerns
    
    Route to RESOURCE FINDER when student needs:
    - Learning materials ("find resources", "best tutorials")
    - Recommendations ("what should I learn from", "good books on X")
    - Course suggestions
    - Practice platforms
    - Documentation or references
    
    MULTI-AGENT COORDINATION:
    When student has multiple needs, coordinate agents in sequence:
    1. Learning + Planning: Explain concept, then create study plan
    2. Planning + Resources: Create schedule, then find materials
    3. Learning + Wellness: Help with concept, check if stressed
    
    CONVERSATION MANAGEMENT:
    - Greet students warmly on first interaction
    - Maintain context across conversation
    - Ask clarifying questions if intent unclear
    - Provide unified, coherent responses
    - End with helpful next steps
    
    PRIORITIES:
    1. Student safety and wellbeing (route to wellness if concerns)
    2. Clear, helpful responses
    3. Appropriate agent delegation
    4. Comprehensive support
    
    Remember: You're the friendly face of EduAssist AI. Be encouraging, 
    supportive, and focused on student success!
    """,
    sub_agents=[
        learning_assistant_agent,
        study_planner_agent,
        wellness_coach_agent,
        resource_finder_agent
    ],
    tools=[]  # Coordinator doesn't need tools, delegates to specialists
)

logger.info("Root Coordinator Agent initialized with 4 specialist sub-agents")

# ============================================================================
# SESSION AND RUNNER SETUP
# ============================================================================

# Create session service for managing conversations
session_service = InMemorySessionService()

# Create runner with coordinator agent
runner = Runner(
    root_agent=coordinator_agent,
    session_service=session_service
)

logger.info("Runner initialized with InMemorySessionService")

# ============================================================================
# MAIN EXECUTION FUNCTION
# ============================================================================

def run_interactive_session():
    """
    Run an interactive CLI session with the EduAssist AI agent system.
    """
    import uuid
    
    print("=" * 70)
    print("🎓 Welcome to EduAssist AI - Multi-Agent Educational Support System")
    print("=" * 70)
    print("\nI'm here to help you with:")
    print("  📚 Learning assistance and concept explanations")
    print("  📅 Study planning and time management")
    print("  💚 Mental wellness and stress management")
    print("  🔍 Finding quality educational resources")
    print("\nType 'exit' or 'quit' to end the session")
    print("Type 'help' for example questions")
    print("=" * 70)
    print()
    
    # Create session
    user_id = "student_" + str(uuid.uuid4())[:8]
    session_id = "session_" + str(uuid.uuid4())[:8]
    
    # Initialize session state with user preferences
    initial_state = {
        "user_preferences": {
            "learning_style": "visual_and_textual",
            "difficulty_level": "intermediate",
            "interests": ["computer_science", "mathematics"]
        },
        "interaction_count": 0,
        "study_schedules": [],
        "progress_tracking": {},
        "wellness_history": []
    }
    
    session_service.create_session(
        app_name="eduassist_ai",
        user_id=user_id,
        session_id=session_id,
        state=initial_state
    )
    
    logger.info(f"Started interactive session: user={user_id}, session={session_id}")
    
    while True:
        try:
            # Get user input
            user_input = input("\n🧑 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Thank you for using EduAssist AI. Good luck with your studies!")
                break
            
            if user_input.lower() == 'help':
                print("\n📝 Example Questions:")
                print("  • Explain binary search trees in simple terms")
                print("  • Create a 2-week study plan for data structures")
                print("  • I'm feeling stressed about upcoming exams")
                print("  • Find good resources for learning Python")
                print("  • Help me understand recursion with examples")
                continue
            
            # Create message content
            message = content_types.Content(
                role="user",
                parts=[user_input]
            )
            
            # Run agent
            print("\n🤖 EduAssist AI: ", end="", flush=True)
            
            response = runner.run(
                user_id=user_id,
                session_id=session_id,
                content=message
            )
            
            # Extract and print response
            for event in response.events:
                if event.type == "content" and event.content.role == "agent":
                    response_text = event.content.parts[0].text
                    print(response_text)
            
            # Update interaction count
            session = session_service.get_session(
                app_name="eduassist_ai",
                user_id=user_id,
                session_id=session_id
            )
            session.state["interaction_count"] += 1
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error in interactive session: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or rephrase your question.")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in environment variables")
        print("Please create a .env file with your Gemini API key:")
        print("  GOOGLE_API_KEY=your_api_key_here")
        exit(1)
    
    try:
        run_interactive_session()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
