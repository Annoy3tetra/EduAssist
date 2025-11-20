"""
coordinator_agent.py

Root Coordinator Agent for EduAssist AI Multi-Agent System
This agent routes user requests to appropriate specialist agents.

Features:
- Intelligent request routing
- Multi-agent orchestration
- Response synthesis
- Context management

Author: Your Name
Date: November 2025
License: MIT
"""

from google.adk.agents import Agent
from typing import List
import logging

# Import sub-agents (will be created separately)
from .learning_assistant import learning_assistant_agent
from .study_planner import study_planner_agent
from .wellness_coach import wellness_coach_agent
from .resource_finder import resource_finder_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Define the root coordinator agent
coordinator_agent = Agent(
    model="gemini-2.0-flash-exp",  # Using Gemini 2.0 Flash for speed
    name="coordinator_agent",
    description="""
    Root coordinator agent that intelligently routes student requests 
    to specialized educational support agents. Provides holistic 
    educational assistance through coordinated multi-agent responses.
    """,
    instruction="""
    You are the Coordinator Agent for EduAssist AI, an intelligent educational 
    support system. Your primary responsibilities are:

    1. ANALYZE user requests to understand their intent and needs
    2. ROUTE requests to the appropriate specialist agent(s):
       - Learning Assistant: For concept explanations, problem-solving, practice
       - Study Planner: For creating schedules, time management, planning
       - Wellness Coach: For stress management, mental health, motivation
       - Resource Finder: For discovering educational materials and resources
    
    3. COORDINATE multiple agents when needed (e.g., if user needs both 
       learning help AND study planning)
    
    4. SYNTHESIZE responses from multiple agents into a coherent answer
    
    5. MAINTAIN context across conversations using session state
    
    Guidelines:
    - Always be supportive and encouraging
    - If uncertain, ask clarifying questions
    - Prioritize student wellbeing alongside academic success
    - Use simple, clear language
    - Provide actionable advice
    
    When routing:
    - Single clear intent → Delegate to one specialist
    - Multiple needs → Coordinate multiple specialists
    - Unclear intent → Ask clarifying questions first
    
    Remember: You are here to make education more accessible, 
    personalized, and supportive for every student.
    """,
    
    # Register all specialist agents as sub-agents
    sub_agents=[
        learning_assistant_agent,
        study_planner_agent,
        wellness_coach_agent,
        resource_finder_agent
    ],
    
    # No tools needed at coordinator level - specialists have tools
    tools=[],
)

logger.info("Coordinator Agent initialized with 4 specialist sub-agents")


# Export for use in main.py
__all__ = ['coordinator_agent']
