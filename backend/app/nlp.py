import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag, ne_chunk
from nltk.tree import Tree
from textblob import TextBlob  # For sentiment analysis and spell checking
from fuzzywuzzy import fuzz

# Download NLTK data (run once)
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('maxent_ne_chunker_tab')
nltk.download('words')

# Initialize stemmer and lemmatizer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def process_text(text: str):
    """
    Enhanced intent recognition using advanced NLP techniques.
    """
    text = text.lower()
    tokens = tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Spell checking and correction
    corrected_text = str(TextBlob(text).correct())

    # POS tagging
    pos_tags = pos_tag(tokens)

    # Named Entity Recognition (NER) using NLTK
    entities = extract_entities(text)

    # Sentiment analysis
    sentiment = analyze_sentiment(text)

    # Intent recognition
    if is_greeting(lemmatized_tokens):
        return {"intent": "greet", "message": "Hello! How can I help you?"}
    elif is_weather_query(lemmatized_tokens):
        city = extract_city(text)
        if city:
            return {"intent": "get_weather", "city": city, "entities": entities, "sentiment": sentiment}
        else:
            return {"intent": "get_weather", "error": "City not found in query"}
    else:
        return {"intent": "unknown", "message": "Sorry, I didn't understand that.", "entities": entities, "sentiment": sentiment}

def tokenize(text: str):
    """
    Tokenize the input text into words.
    """
    return word_tokenize(text)

def is_greeting(tokens):
    """
    Check if the input is a greeting using synonym matching.
    """
    greetings = ["hello", "hi", "hey", "greetings"]
    for token in tokens:
        if token in greetings:
            return True
    return False

def is_weather_query(tokens):
    """
    Check if the input is a weather-related query using stemming and fuzzy matching.
    """
    weather_keywords = ["weather", "forecast", "temperature", "rain", "sun"]
    for token in tokens:
        for keyword in weather_keywords:
            if fuzz.ratio(token, keyword) > 70:  # Fuzzy matching with 70% threshold
                return True
    return False

def extract_city(text: str):
    """
    Extract city name using regex.
    """
    # Regex to match city names (basic implementation)
    city_pattern = re.compile(r'\b(?:in|at|for)\s+([A-Za-z]+)\b')
    match = city_pattern.search(text)
    if match:
        return match.group(1).strip()
    return None

def extract_entities(text: str):
    """
    Extract named entities using NLTK's ne_chunk.
    """
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    tree = ne_chunk(pos_tags)
    entities = []
    for subtree in tree:
        if isinstance(subtree, Tree):
            entity = " ".join([word for word, pos in subtree.leaves()])
            entities.append((entity, subtree.label()))
    return entities

def analyze_sentiment(text: str):
    """
    Perform sentiment analysis using TextBlob.
    """
    blob = TextBlob(text)
    sentiment = blob.sentiment
    return {
        "polarity": sentiment.polarity,
        "subjectivity": sentiment.subjectivity,
        "sentiment": "positive" if sentiment.polarity > 0 else "negative" if sentiment.polarity < 0 else "neutral"
    }

def get_wordnet_pos(treebank_tag):
    """
    Map POS tag to WordNet POS tag for lemmatization.
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun