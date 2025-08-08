import csv
import io
from datetime import datetime
from .models import Review

NEGATIVE_KEYWORDS = ['cold', 'bad', 'slow', 'rude', 'late', 'terrible', 'worst']
TAG_CATEGORIES = {
    'cold': 'Cold Food',
    'slow': 'Slow Service',
    'rude': 'Rude Staff',
    'late': 'Late Delivery',
    'bad': 'Bad Experience',
    'terrible': 'Terrible',
    'worst': 'Worst Experience'
}

def classify_sentiment(rating, text):
    if rating >= 4:
        return 'positive'
    elif rating == 3:
        return 'neutral'
    else:
        for word in NEGATIVE_KEYWORDS:
            if word in text.lower():
                return 'negative'
        return 'neutral'

def tag_negative_review(text):
    tags = set()
    for word in TAG_CATEGORIES:
        if word in text.lower():
            tags.add(TAG_CATEGORIES[word])
    return ', '.join(tags)
