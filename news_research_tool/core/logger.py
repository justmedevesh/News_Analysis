"""
logger.py

Purpose:
---------
Central logging system for the application.

This file handles:
1. Error logging
2. User activity logging
3. Debug logging
4. Event tracking

Why logging is important:
--------------------------
Production applications need logs to:
- debug issues
- monitor system behavior
- track failures
- analyze usage
"""

# Import logging module
import logging

from news_research_tool.core.paths import LOGS_DIR


# Create logs folder automatically
LOGS_DIR.mkdir(exist_ok=True)


# Configure logger
logging.basicConfig(

    # Log file location
    filename=str(LOGS_DIR / "app.log"),

    # Append mode
    filemode="a",

    # Log format
    format="""
%(asctime)s
%(levelname)s
%(message)s
------------------------
""",

    # Logging level
    level=logging.INFO
)


# Create reusable logger
logger = logging.getLogger(__name__)
