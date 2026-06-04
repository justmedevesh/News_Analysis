"""
exporter.py

Purpose:
---------
Handles exporting and saving AI summaries.

Features:
---------
1. Save summaries as TXT files
2. Save summaries as Markdown files
3. Generate timestamped filenames
4. Organize reports professionally
"""

# ---------------------------------------------------
# IMPORTS
# ---------------------------------------------------

from datetime import datetime

from news_research_tool.core.paths import REPORTS_DIR


# ---------------------------------------------------
# CREATE REPORTS FOLDER IF MISSING
# ---------------------------------------------------

REPORTS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------
# CLEAN FILENAME FUNCTION
# ---------------------------------------------------

def clean_filename(text: str) -> str:
    """
    Cleans filenames by removing invalid characters.

    Example:
    --------
    "Artificial Intelligence!"
    becomes:
    "Artificial_Intelligence"
    """

    cleaned = text.replace(" ", "_")

    # Keep only safe filename characters
    cleaned = "".join(
        char for char in cleaned
        if char.isalnum() or char == "_"
    )

    return cleaned


# ---------------------------------------------------
# SAVE TXT REPORT
# ---------------------------------------------------

def save_as_txt(query: str, summary: str) -> str:
    """
    Saves summary as TXT file.

    Returns:
    --------
    str : file path
    """

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Clean query for filename
    safe_query = clean_filename(query)

    # Create filename
    filename = f"{safe_query}_{timestamp}.txt"

    # Full path
    filepath = REPORTS_DIR / filename

    # Write file
    with filepath.open("w", encoding="utf-8") as file:

        file.write("AI NEWS RESEARCH REPORT\n")
        file.write("=" * 50)
        file.write("\n\n")

        file.write(f"Query: {query}\n")
        file.write(f"Generated: {timestamp}\n\n")

        file.write("SUMMARY\n")
        file.write("-" * 50)
        file.write("\n")

        file.write(summary)

    return str(filepath)


# ---------------------------------------------------
# SAVE MARKDOWN REPORT
# ---------------------------------------------------

def save_as_markdown(query: str, summary: str) -> str:
    """
    Saves summary as Markdown report.

    Returns:
    --------
    str : file path
    """

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Clean filename
    safe_query = clean_filename(query)

    # Markdown filename
    filename = f"{safe_query}_{timestamp}.md"

    # Full path
    filepath = REPORTS_DIR / filename

    # Write markdown file
    with filepath.open("w", encoding="utf-8") as file:

        file.write("# AI News Research Report\n\n")

        file.write(f"**Query:** {query}\n\n")

        file.write(f"**Generated:** {timestamp}\n\n")

        file.write("---\n\n")

        file.write("## AI Summary\n\n")

        file.write(summary)

    return str(filepath)
