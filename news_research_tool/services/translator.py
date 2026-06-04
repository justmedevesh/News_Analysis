"""
Translation service for the AI News Research Tool.

The app fetches news in English, then translates the user-facing briefing and
article text into the language selected in the UI.
"""

import json
import re
from typing import Dict, List

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from news_research_tool.core.config import get_llm
from news_research_tool.core.logger import logger


LANGUAGE_OPTIONS = [
    ("English", "English"),
    ("Nepali", "Nepali"),
    ("Hindi", "Hindi"),
    ("Spanish", "Spanish"),
    ("French", "French"),
    ("German", "German"),
    ("Arabic", "Arabic"),
    ("Bengali", "Bengali"),
    ("Chinese", "Chinese"),
    ("Japanese", "Japanese"),
    ("Korean", "Korean"),
    ("Portuguese", "Portuguese"),
    ("Russian", "Russian"),
    ("Urdu", "Urdu"),
]

SUPPORTED_LANGUAGE_NAMES = {language for language, _ in LANGUAGE_OPTIONS}


def normalize_language(language: str) -> str:
    """Returns a supported language name, falling back to English."""
    if language in SUPPORTED_LANGUAGE_NAMES:
        return language

    return "English"


def should_translate(language: str) -> bool:
    return normalize_language(language) != "English"


def translate_text(text: str, target_language: str) -> str:
    """Translate a single text block while preserving meaning and formatting."""
    target_language = normalize_language(target_language)

    if not text or not should_translate(target_language):
        return text

    prompt = PromptTemplate(
        input_variables=["target_language", "text"],
        template="""
You are a professional news translation assistant.

Translate the following news briefing into {target_language}.

Rules:
1. Preserve the original meaning exactly.
2. Keep names of people, companies, products, and places accurate.
3. Keep numbers, dates, currencies, and URLs unchanged.
4. Preserve paragraph breaks and bullet formatting when present.
5. Return only the translated text.

TEXT:
{text}
""",
    )

    chain = prompt | get_llm() | StrOutputParser()
    logger.info(f"Translating summary to {target_language}")

    return chain.invoke({
        "target_language": target_language,
        "text": text,
    })


def translate_articles(articles: List[Dict], target_language: str) -> List[Dict]:
    """Translate article titles and descriptions in one batch."""
    target_language = normalize_language(target_language)

    if not articles or not should_translate(target_language):
        return articles

    payload = [
        {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
        }
        for article in articles
    ]

    prompt = PromptTemplate(
        input_variables=["target_language", "articles_json"],
        template="""
You are a professional news translation assistant.

Translate each article title and description into {target_language}.

Rules:
1. Preserve facts exactly.
2. Keep names of people, companies, products, places, numbers, and dates accurate.
3. Return only valid JSON.
4. Return a JSON array with the same number of items.
5. Each item must have exactly these keys: "title", "description".

ARTICLES_JSON:
{articles_json}
""",
    )

    chain = prompt | get_llm() | StrOutputParser()
    logger.info(f"Translating article metadata to {target_language}")

    response = chain.invoke({
        "target_language": target_language,
        "articles_json": json.dumps(payload, ensure_ascii=False),
    })

    try:
        translated_fields = _parse_json_array(response)
    except ValueError as error:
        logger.error(f"Article translation JSON parse failed: {error}")
        return articles

    if len(translated_fields) != len(articles):
        logger.error("Article translation count mismatch")
        return articles

    translated_articles = []

    for article, translated in zip(articles, translated_fields):
        translated_article = article.copy()
        translated_article["title"] = translated.get("title", article.get("title", ""))
        translated_article["description"] = translated.get("description", article.get("description", ""))
        translated_articles.append(translated_article)

    return translated_articles


def _parse_json_array(text: str) -> List[Dict]:
    """Parse an LLM JSON response, tolerating fenced code blocks."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    data = json.loads(cleaned)

    if not isinstance(data, list):
        raise ValueError("Expected a JSON array")

    return data
