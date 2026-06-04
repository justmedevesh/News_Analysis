"""
summarizer.py

Purpose:
---------
This file handles:
1. Formatting news articles
2. Creating AI prompts
3. Sending prompts to Groq LLM
4. Generating final summaries

Why this file is important:
----------------------------
Professional AI systems separate:
- data fetching
- preprocessing
- AI generation

This improves:
- readability
- scalability
- debugging
- maintainability
"""

# Import LangChain prompt template
from langchain_core.prompts import PromptTemplate

# Import output parser
from langchain_core.output_parsers import StrOutputParser

# Import LLM from config
from news_research_tool.core.config import get_llm

# Import logger
from news_research_tool.core.logger import logger

# Import typing
from typing import List, Dict


def format_articles(articles: List[Dict]) -> str:
    """
    Converts articles into structured text format.

    Why formatting matters:
    ------------------------
    LLMs perform better when information is:
    - structured
    - organized
    - consistent

    Parameters:
    -----------
    articles : List[Dict]

    Returns:
    --------
    str
    """

    formatted_text = ""

    for index, article in enumerate(articles, start=1):

        formatted_text += f"""
Article {index}

Title:
{article['title']}

Description:
{article['description']}

Content:
{article['content']}

Source:
{article['source']}

==================================================
"""

    return formatted_text


def create_prompt() -> PromptTemplate:
    """
    Creates professional summarization prompt.

    Why prompt engineering matters:
    --------------------------------
    Better prompts produce:
    - better summaries
    - lower hallucinations
    - more focused responses
    """

    template = """
You are a professional AI news research assistant.

Your task is to analyze the provided news articles and generate a high-quality summary.

USER QUERY:
{query}

NEWS ARTICLES:
{articles}

INSTRUCTIONS:
1. Summarize the most important developments.
2. Highlight major trends.
3. Mention important companies or organizations.
4. Explain possible market or industry impact.
5. Identify risks or opportunities if relevant.
6. Keep the summary factual and concise.
7. Do not invent information.
8. Use professional language.

FINAL SUMMARY:
"""

    return PromptTemplate(
        input_variables=["query", "articles"],
        template=template
    )


def generate_summary(query: str, articles: List[Dict]) -> str:
    """
    Main summarization function.

    Workflow:
    ---------
    1. Format articles
    2. Create prompt
    3. Build LangChain pipeline
    4. Send request to Groq
    5. Return final summary

    Parameters:
    -----------
    query : str

    articles : List[Dict]

    Returns:
    --------
    str
    """

    # Handle empty articles
    if not articles:
        return "No valid news articles were found."

    # Convert article list into structured text
    formatted_articles = format_articles(articles)

    # Create prompt template
    prompt = create_prompt()

    # Create output parser
    parser = StrOutputParser()

    # Build LangChain pipeline
    chain = prompt | get_llm() | parser

    logger.info("Generating AI summary")

    # Generate final summary
    response = chain.invoke({
        "query": query,
        "articles": formatted_articles
    })

    logger.info("AI summary generated successfully")
    return response
