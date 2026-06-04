"""
test_config.py

Purpose:
---------
This file tests whether:
1. Environment variables load correctly
2. Groq model initializes successfully
3. AI responses are working
"""

# Import LLM from config
from news_research_tool.core.config import get_llm


# Send a simple test prompt
response = get_llm().invoke("Say hello")


# Print response
print(response.content)
