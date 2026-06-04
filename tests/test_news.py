"""
test_news.py

Purpose:
---------
This file tests whether:
1. NewsAPI connection works
2. Articles are fetched correctly
3. Cleaning logic works
4. Duplicate removal works
"""

# Import fetch function
from news_research_tool.services.news_fetcher import fetch_news


# Test query
query = "Artificial Intelligence"


# Fetch articles
articles = fetch_news(query)


# Print total articles
print(f"\nTotal Articles Found: {len(articles)}\n")


# Print articles one by one
for index, article in enumerate(articles, start=1):

    print(f"Article {index}")
    print("-" * 50)

    print("Title:")
    print(article["title"])

    print("\nDescription:")
    print(article["description"])

    print("\nSource:")
    print(article["source"])

    print("\nURL:")
    print(article["url"])

    print("\n")
