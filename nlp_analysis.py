from textblob import TextBlob

def analyze_text(text):
    blob = TextBlob(text)
    sentiment = "Positive" if blob.sentiment.polarity > 0 else "Negative" if blob.sentiment.polarity < 0 else "Neutral"
    keywords = [word.lower() for word in blob.noun_phrases]
    return sentiment, keywords
