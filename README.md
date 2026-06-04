# AI News Research Tool

A Flask web app that fetches live news articles, summarizes them with Groq and
LangChain, translates the briefing into a selected language, and exports the
generated report as TXT or Markdown.

## Setup

Create a `.env` file with:

```bash
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_newsapi_key
FLASK_SECRET_KEY=change_this_for_production
```

Install dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Run the app:

```bash
.venv/bin/python app.py
```

Then open:

```text
http://127.0.0.1:5001
```

## Project Structure

```text
.
├── app.py                         # Flask launcher
├── news_research_tool/
│   ├── web.py                     # Flask routes and page state
│   ├── core/
│   │   ├── config.py              # Environment variables and Groq setup
│   │   ├── logger.py              # Application logging
│   │   └── paths.py               # Shared project paths
│   ├── services/
│   │   ├── news_fetcher.py        # NewsAPI fetching and article cleanup
│   │   ├── summarizer.py          # LangChain summarization
│   │   ├── translator.py          # Summary and article translation
│   │   └── exporter.py            # TXT and Markdown report exports
│   ├── templates/
│   │   └── index.html             # Flask page template
│   └── static/
│       ├── app.js                 # UI interactions
│       ├── styles.css             # UI styling
│       └── images/                # UI images
├── tests/                         # Manual test scripts
├── reports/                       # Generated reports
├── logs/                          # Application logs
└── requirements.txt
```
