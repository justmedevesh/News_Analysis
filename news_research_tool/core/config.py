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


def require_env(value: str, name: str) -> str:
    """Return an env value or raise a clear runtime error."""
    if value:
        return value

    raise RuntimeError(f"{name} is missing. Add it in your environment variables.")


# Initialize Groq LLM
# We use llama3 model because:
# - Fast
# - Good summarization
# - Cost efficient
def get_llm() -> ChatGroq:
    return ChatGroq(
        groq_api_key=require_env(GROQ_API_KEY, "GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.3
    )
