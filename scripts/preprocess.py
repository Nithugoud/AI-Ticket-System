"""
Text Preprocessing Module
Handles all text cleaning and normalization before ML model prediction
"""

import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk

# Download required NLTK data (only needed once)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.download('punkt_tab', quiet=True)
    except:
        nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def lowercase_text(text):
    """
    Convert text to lowercase for consistency
    
    Args:
        text (str): Input text
    
    Returns:
        str: Lowercased text
    """
    return text.lower()


def remove_punctuation(text):
    """
    Remove all punctuation marks from text
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text without punctuation
    """
    # Remove punctuation using string module
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def remove_numbers(text):
    """
    Remove numeric digits from text
    Preserves alphanumeric identifiers like 'error404'
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text with standalone numbers removed
    """
    # Remove standalone numbers
    text = re.sub(r'\b\d+\b', '', text)
    return text


def remove_stopwords(text):
    """
    Remove common English stopwords
    Stopwords are common words like 'the', 'is', 'and' that don't add semantic meaning
    
    Args:
        text (str): Input text
    
    Returns:
        str: Text without stopwords
    """
    # Tokenize and filter
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_tokens)


def lemmatize_text(text):
    """
    Lemmatize words to their root form
    Example: 'running' -> 'run', 'better' -> 'good'
    
    Args:
        text (str): Input text
    
    Returns:
        str: Lemmatized text
    """
    # Tokenize and lemmatize each word
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized_tokens)


def clean_whitespace(text):
    """
    Remove extra whitespaces and normalize
    - Remove leading/trailing spaces
    - Replace multiple spaces with single space
    - Remove tabs and newlines
    
    Args:
        text (str): Input text
    
    Returns:
        str: Cleaned text with normalized whitespace
    """
    # Replace multiple spaces/tabs/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing whitespace
    return text.strip()


def preprocess_text(text):
    """
    Main preprocessing pipeline
    Applies all cleaning steps in the correct order
    
    Order matters:
    1. Lowercase (consistency)
    2. Remove punctuation (reduce noise)
    3. Remove numbers (reduce noise)
    4. Remove stopwords (reduce noise)
    5. Lemmatize (standardize word forms)
    6. Clean whitespace (final formatting)
    
    Args:
        text (str): Raw input text
    
    Returns:
        str: Fully preprocessed text
    
    Example:
        >>> raw = "I'm unable to LOGIN to the company portal!"
        >>> preprocess_text(raw)
        'unable login company portal'
    """
    if not isinstance(text, str) or not text:
        return ""
    
    # Step 1: Lowercase
    text = lowercase_text(text)
    
    # Step 2: Remove punctuation
    text = remove_punctuation(text)
    
    # Step 3: Remove numbers
    text = remove_numbers(text)
    
    # Step 4: Remove stopwords
    text = remove_stopwords(text)
    
    # Step 5: Lemmatize
    text = lemmatize_text(text)
    
    # Step 6: Clean whitespace
    text = clean_whitespace(text)
    
    return text


# Optional: Keep original text for display purposes
def get_preprocessing_summary(original_text, cleaned_text):
    """
    Generates a summary of preprocessing changes
    Useful for debugging and understanding transformations
    
    Args:
        original_text (str): Original raw text
        cleaned_text (str): Preprocessed text
    
    Returns:
        dict: Summary of preprocessing
    """
    return {
        'original': original_text,
        'cleaned': cleaned_text,
        'original_length': len(original_text),
        'cleaned_length': len(cleaned_text),
        'compression_ratio': round((1 - len(cleaned_text) / max(len(original_text), 1)) * 100, 2)
    }
