"""
test_summary.py

Purpose:
---------
This file tests:
1. News fetching
2. AI summarization
3. LangChain pipeline
4. Groq response generation
"""

# Import news fetcher
from news_research_tool.services.news_fetcher import fetch_news

# Import summarizer
from news_research_tool.services.summarizer import generate_summary


# User query
query = "Artificial Intelligence"


# Fetch articles
articles = fetch_news(query)


# Generate AI summary
summary = generate_summary(query, articles)


# Print final result
print("\nFINAL AI SUMMARY\n")
print("=" * 60)

print(summary)
