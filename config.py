"""
Configuration File
Centralized settings for the AI Ticket System
Modify these values to customize system behavior
"""

import os

# ========================== PATHS ==========================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'tickets_output')

# ========================== TEXT PREPROCESSING ==========================
# TF-IDF Configuration
TFIDF_MAX_FEATURES = 500           # Maximum vocabulary size
TFIDF_NGRAM_RANGE = (1, 2)         # Use unigrams and bigrams
TFIDF_MIN_DF = 1                   # Minimum document frequency
TFIDF_MAX_DF = 0.8                 # Maximum document frequency

# ========================== ML MODEL CONFIGURATION ==========================
# Category Model Settings
CATEGORY_MODEL_TYPE = "LogisticRegression"  # Options: LogisticRegression, RandomForest
CATEGORY_MAX_ITER = 200
CATEGORY_RANDOM_STATE = 42

# Priority Model Settings
PRIORITY_MODEL_TYPE = "SVM"  # Options: SVM, RandomForest, GradientBoosting
PRIORITY_KERNEL = "rbf"
PRIORITY_RANDOM_STATE = 42

# ========================== TICKET CONFIGURATION ==========================
# Ticket ID Settings
TICKET_ID_PREFIX = "INC"
TICKET_ID_START_NUMBER = 1000
DEFAULT_STATUS = "Open"

# Ticket Input Validation
MIN_DESCRIPTION_LENGTH = 10
MAX_DESCRIPTION_LENGTH = 5000

# ========================== CATEGORIES & PRIORITIES ==========================
# Ticket Categories
CATEGORIES = [
    "Network",
    "Access", 
    "Hardware",
    "Software",
    "Storage",
    "System"
]

# Priority Levels (ordered from highest to lowest)
PRIORITY_LEVELS = [
    "Critical",
    "High",
    "Medium",
    "Low"
]

# Priority Color Codes (for UI display)
PRIORITY_COLORS = {
    "Critical": "🔴",
    "High": "🟠",
    "Medium": "🟡",
    "Low": "🟢"
}

# ========================== CONFIDENCE THRESHOLDS ==========================
# Confidence levels for alerts/reviews
CONFIDENCE_HIGH = 0.90      # >= 90%: High confidence, auto-accept
CONFIDENCE_MEDIUM = 0.70    # 70-89%: Medium confidence, review recommended
CONFIDENCE_LOW = 0.50       # < 70%: Low confidence, manual review needed

# ========================== ENTITY EXTRACTION ==========================
# Regex patterns for entity extraction
ENTITY_EXTRACTION_CONFIG = {
    "usernames": {
        "enabled": True,
        "min_length": 3,
        "max_length": 20
    },
    "devices": {
        "enabled": True,
        "min_length": 2
    },
    "error_codes": {
        "enabled": True,
        "patterns": ["ERROR", "0x", "E[0-9]{3,4}"]  # Common error code formats
    }
}

# ========================== TRAINING DATA ==========================
# Sample training data (can be overridden with external data)
USE_SAMPLE_DATA = True  # Set to False to use external data source
SAMPLE_DATA_FILE = None  # Path to external training data CSV

# ========================== LOGGING & DEBUG ==========================
DEBUG_MODE = False
VERBOSE = True
LOG_PREDICTIONS = True

# ========================== STREAMLIT UI CONFIG ==========================
STREAMLIT_CONFIG = {
    "page_title": "AI Ticket System",
    "page_icon": "🎫",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# ========================== API INTEGRATION ==========================
# For future REST API integration
API_ENABLED = False
API_PORT = 5000
API_HOST = "127.0.0.1"

# ========================== DATABASE ==========================
# For future database integration
DATABASE_ENABLED = False
DATABASE_TYPE = "sqlite"  # Options: sqlite, postgresql, mysql
DATABASE_PATH = os.path.join(PROJECT_ROOT, "tickets.db")

# ========================== HELPER FUNCTIONS ==========================

def get_config_summary():
    """Print current configuration"""
    print("=" * 60)
    print("SYSTEM CONFIGURATION")
    print("=" * 60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Models Directory: {MODELS_DIR}")
    print(f"Categories: {', '.join(CATEGORIES)}")
    print(f"Priorities: {', '.join(PRIORITY_LEVELS)}")
    print(f"TF-IDF Max Features: {TFIDF_MAX_FEATURES}")
    print(f"Confidence Thresholds - High: {CONFIDENCE_HIGH}, Medium: {CONFIDENCE_MEDIUM}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print("=" * 60)

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not os.path.exists(MODELS_DIR):
        errors.append(f"Models directory not found: {MODELS_DIR}")
    
    if MIN_DESCRIPTION_LENGTH > MAX_DESCRIPTION_LENGTH:
        errors.append("MIN_DESCRIPTION_LENGTH cannot be greater than MAX_DESCRIPTION_LENGTH")
    
    if not CATEGORIES or len(CATEGORIES) == 0:
        errors.append("CATEGORIES list is empty")
    
    if not PRIORITY_LEVELS or len(PRIORITY_LEVELS) == 0:
        errors.append("PRIORITY_LEVELS list is empty")
    
    if CONFIDENCE_HIGH <= CONFIDENCE_MEDIUM or CONFIDENCE_MEDIUM <= CONFIDENCE_LOW:
        errors.append("Confidence thresholds not in correct order")
    
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  ✗ {error}")
        return False
    else:
        print("✓ Configuration validated successfully")
        return True

# ========================== CUSTOMIZATION GUIDE ==========================

"""
CUSTOMIZATION EXAMPLES:

1. Add new ticket category:
   CATEGORIES.append("Email")

2. Change priority levels:
   PRIORITY_LEVELS = ["Urgent", "Normal", "Low"]

3. Adjust model confidence:
   CONFIDENCE_HIGH = 0.95  # Stricter
   CONFIDENCE_LOW = 0.60   # More lenient

4. Change TF-IDF vectorizer:
   TFIDF_MAX_FEATURES = 1000  # Larger vocabulary
   TFIDF_NGRAM_RANGE = (1, 3) # Include trigrams

5. Enable debug mode:
   DEBUG_MODE = True
"""
