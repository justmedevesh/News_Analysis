"""
news_fetcher.py

Purpose:
---------
This file handles:
1. Connecting to NewsAPI
2. Fetching latest news articles
3. Cleaning article data
4. Removing duplicates
5. Handling API errors safely

Why this file is important:
----------------------------
Professional AI systems separate:
- UI
- business logic
- API communication

This makes the project:
- scalable
- maintainable
- easier to debug
"""

# Import NewsAPI client
from newsapi import NewsApiClient

# Import logger
from news_research_tool.core.logger import logger

# Import API key from config
from news_research_tool.core.config import NEWS_API_KEY, require_env

# Import requests exception handling
import requests

# Import typing for better readability
from typing import List, Dict


def clean_article(article: Dict) -> Dict:
    """
    Cleans and validates a single news article.

    Parameters:
    -----------
    article : Dict
        Raw article dictionary from NewsAPI

    Returns:
    --------
    Dict
        Cleaned article dictionary
    """

    return {
        "title": article.get("title", "No Title"),
        "description": article.get("description", ""),
        "content": article.get("content", ""),
        "url": article.get("url", ""),
        "source": article.get("source", {}).get("name", "Unknown Source")
    }


def is_valid_article(article: Dict) -> bool:
    """
    Checks whether an article contains enough useful information.

    Why validation is important:
    -----------------------------
    Some articles may:
    - Have missing descriptions
    - Contain null content
    - Be advertisements
    - Be incomplete

    Returns:
    --------
    bool
    """

    # Check minimum content quality
    if not article["description"]:
        return False

    if len(article["description"]) < 20:
        return False

    return True


def remove_duplicates(articles: List[Dict]) -> List[Dict]:
    """
    Removes duplicate articles based on title.

    Why duplicates happen:
    -----------------------
    Multiple news sources may publish the same story.

    Returns:
    --------
    List[Dict]
    """

    unique_titles = set()
    unique_articles = []

    for article in articles:

        title = article["title"]

        # Skip duplicate titles
        if title in unique_titles:
            continue

        unique_titles.add(title)
        unique_articles.append(article)

    return unique_articles


def fetch_news(query: str, page_size: int = 10) -> List[Dict]:
    """
    Fetches news articles from NewsAPI.

    Parameters:
    -----------
    query : str
        User search query

    page_size : int
        Number of articles to fetch

    Returns:
    --------
    List[Dict]
        Cleaned and validated news articles
    """

    try:

        logger.info(f"Fetching news for query: {query}")

        newsapi = NewsApiClient(api_key=require_env(NEWS_API_KEY, "NEWS_API_KEY"))

        # Fetch news articles
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=page_size
        )

        # Extract articles list
        raw_articles = response.get("articles", [])

        cleaned_articles = []

        # Process each article
        for article in raw_articles:

            cleaned_article = clean_article(article)

            # Validate article quality
            if is_valid_article(cleaned_article):
                cleaned_articles.append(cleaned_article)

        # Remove duplicate articles
        unique_articles = remove_duplicates(cleaned_articles)

        logger.info(f"Fetched {len(unique_articles)} unique articles")
        return unique_articles

    except requests.exceptions.RequestException as error:

        print(f"Network Error: {error}")
        return []
        logger.error(f"Network Error: {error}")

    except Exception as error:
        logger.error(f"Unexpected Error: {error}")
        raise
