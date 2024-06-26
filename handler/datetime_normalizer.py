from datetime import datetime

import readtime
from models import Article


def normalize_article_datetime(article: Article):
    """Normalizes the datetime of an article."""
    article.date = _ensure_correct_timezone(article.date)
    article.date = datetime.fromisoformat(article.date)
    article.accessed_date = datetime.fromisoformat(article.accessed_date)
    article.read_time_minutes = _get_read_time_minutes(article.content)


TIMEZONE7 = "+07:00"


def _ensure_correct_timezone(date: str):
    """Checks if the datetime is in UTC timezone."""
    if date.endswith("-07:00"):
        return date.replace("-07:00", TIMEZONE7)
    if not date.endswith(TIMEZONE7):
        return date + TIMEZONE7
    return date


def _get_read_time_minutes(text: str):
    """Calculates the read time of an article."""
    return readtime.of_text(text).minutes
