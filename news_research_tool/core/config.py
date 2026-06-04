"""
config.py

Purpose:
---------
This file handles:
1. Loading environment variables
2. Initializing the Groq LLM
3. Central project configuration

Why this file is important:
----------------------------
Instead of writing API setup everywhere,
we centralize configuration in one place.

Benefits:
---------
- Cleaner code
- Easier maintenance
- Better scalability
- Professional project structure
"""

# Load environment variables from .env file
from dotenv import load_dotenv

# Allows access to environment variables
import os

# LangChain Groq integration
from langchain_groq import ChatGroq


# Load all variables from .env
load_dotenv()


# Fetch API keys securely from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# Validate Groq API key
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in .env file")


# Validate News API key
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY is missing in .env file")


# Initialize Groq LLM
# We use llama3 model because:
# - Fast
# - Good summarization
# - Cost efficient
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)