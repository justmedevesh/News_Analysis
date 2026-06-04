"""
Flask application for the AI News Research Tool.

The fetching, summarizing, exporting, and logging logic lives in separate
modules. This file only handles web routes and page state.
"""

from datetime import datetime
from functools import lru_cache
import json
import os
import time

from flask import Flask, abort, redirect, render_template, request, send_file, session, url_for

from news_research_tool.core.logger import logger
from news_research_tool.core.paths import REPORTS_DIR
from news_research_tool.services.exporter import save_as_markdown, save_as_txt
from news_research_tool.services.news_fetcher import fetch_news
from news_research_tool.services.summarizer import generate_summary
from news_research_tool.services.translator import (
    LANGUAGE_OPTIONS,
    normalize_language,
    should_translate,
    translate_articles,
    translate_text,
)


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-news-research-secret")


@lru_cache(maxsize=32)
def cached_fetch_news(query):
    """Cache NewsAPI responses by query to reduce repeated API calls."""
    return fetch_news(query)


@lru_cache(maxsize=32)
def cached_generate_summary(query, articles_json):
    """Cache Groq summaries using a stable serialized article payload."""
    articles = json.loads(articles_json)
    return generate_summary(query, articles)


@lru_cache(maxsize=64)
def cached_translate_text(text, target_language):
    """Cache translated summaries by exact text and language."""
    return translate_text(text, target_language)


@lru_cache(maxsize=64)
def cached_translate_articles(articles_json, target_language):
    """Cache translated article metadata by exact article payload and language."""
    articles = json.loads(articles_json)
    return translate_articles(articles, target_language)


def get_query_history():
    return session.setdefault("query_history", [])


def get_total_searches():
    return session.setdefault("total_searches", 0)


@app.get("/")
def index():
    return render_template(
        "index.html",
        query="",
        history=get_query_history(),
        total_searches=get_total_searches(),
        language_options=LANGUAGE_OPTIONS,
        selected_language="English",
        result=None,
        error=None,
    )


@app.post("/")
def search():
    query = request.form.get("query", "").strip()
    selected_language = normalize_language(request.form.get("target_language", "English"))
    logger.info(f"User searched for: {query}")

    if not query:
        return render_template(
            "index.html",
            query=query,
            history=get_query_history(),
            total_searches=get_total_searches(),
            language_options=LANGUAGE_OPTIONS,
            selected_language=selected_language,
            result=None,
            error="Please enter a valid topic.",
        )

    try:
        start_time = time.time()

        history = get_query_history()
        history.append(query)
        session["query_history"] = history[-20:]
        session["total_searches"] = get_total_searches() + 1
        session.modified = True

        articles = cached_fetch_news(query)
        articles_json = json.dumps(articles, sort_keys=True)
        summary = cached_generate_summary(query, articles_json)

        display_summary = summary
        display_articles = articles

        if should_translate(selected_language):
            display_summary = cached_translate_text(summary, selected_language)
            display_articles = cached_translate_articles(articles_json, selected_language)

        txt_path = save_as_txt(query, display_summary)
        md_path = save_as_markdown(query, display_summary)

        result = {
            "query": query,
            "summary": display_summary,
            "articles": display_articles,
            "articles_found": len(articles),
            "processing_time": round(time.time() - start_time, 2),
            "generated_at": datetime.now().strftime("%H:%M:%S"),
            "language": selected_language,
            "txt_file": os.path.basename(txt_path),
            "md_file": os.path.basename(md_path),
        }

        return render_template(
            "index.html",
            query=query,
            history=get_query_history(),
            total_searches=get_total_searches(),
            language_options=LANGUAGE_OPTIONS,
            selected_language=selected_language,
            result=result,
            error=None,
        )

    except Exception as error:
        logger.error(f"Application Error: {error}")

        return render_template(
            "index.html",
            query=query,
            history=get_query_history(),
            total_searches=get_total_searches(),
            language_options=LANGUAGE_OPTIONS,
            selected_language=selected_language,
            result=None,
            error=f"Application Error: {error}",
        )


@app.post("/clear-history")
def clear_history():
    session["query_history"] = []
    session["total_searches"] = 0
    session.modified = True
    return redirect(url_for("index"))


@app.get("/download/<path:filename>")
def download_report(filename):
    reports_dir = os.path.abspath(REPORTS_DIR)
    requested_path = os.path.abspath(os.path.join(reports_dir, filename))

    if not requested_path.startswith(reports_dir + os.sep):
        abort(404)

    if not os.path.exists(requested_path):
        abort(404)

    return send_file(requested_path, as_attachment=True)
