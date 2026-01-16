"""
Training Script to Generate Pre-trained ML Models
This script creates and trains models for ticket categorization and priority prediction
Models are saved as .pkl files in the models/ directory
"""

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import os

# Create models directory if it doesn't exist
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# ==================== SAMPLE TRAINING DATA ====================
# This is representative IT support ticket data
training_descriptions = [
    # Network & Connectivity Issues
    "Cannot connect to company network after moving to new floor",
    "WiFi connection keeps dropping intermittently",
    "Internet speed is very slow affecting work productivity",
    "VPN connection fails when I try to access remote resources",
    "Network cable not detected by laptop",
    
    # Access & Authentication Issues
    "Unable to login to company portal after password reset",
    "Cannot access shared drive on file server",
    "Need permissions to access project directory",
    "Locked out of email account after failed login attempts",
    "SSO authentication not working for enterprise apps",
    
    # Hardware Issues
    "Laptop screen is flickering constantly",
    "Mouse and keyboard not responding properly",
    "Printer not printing from my computer",
    "External hard drive not recognized by system",
    "Monitor display showing black screen",
    
    # Software & Application Issues
    "Microsoft Word crashes when opening large documents",
    "Excel formulas not calculating correctly",
    "Outlook email client freezes frequently",
    "Adobe Reader PDF files not opening properly",
    "Slack notifications not working as expected",
    
    # Data & Storage Issues
    "Disk space critically low on C drive",
    "Cannot save files to network backup",
    "Data loss after system crash yesterday",
    "Backup job failed for critical project files",
    "Storage quota exceeded on cloud drive",
    
    # System & Performance Issues
    "Computer running extremely slow and sluggish",
    "Fan making unusual noise and system overheating",
    "System restart required after each application",
    "Memory usage at 100 percent constantly",
    "System boots very slowly taking 10 minutes",
]

training_categories = [
    # Network & Connectivity
    "Network", "Network", "Network", "Network", "Network",
    
    # Access & Authentication
    "Access", "Access", "Access", "Access", "Access",
    
    # Hardware
    "Hardware", "Hardware", "Hardware", "Hardware", "Hardware",
    
    # Software & Application
    "Software", "Software", "Software", "Software", "Software",
    
    # Data & Storage
    "Storage", "Storage", "Storage", "Storage", "Storage",
    
    # System & Performance
    "System", "System", "System", "System", "System",
]

training_priorities = [
    # Network & Connectivity
    "High", "Medium", "Medium", "High", "High",
    
    # Access & Authentication
    "High", "High", "Medium", "High", "High",
    
    # Hardware
    "Medium", "Medium", "Low", "Medium", "High",
    
    # Software & Application
    "Medium", "Medium", "Medium", "Low", "Low",
    
    # Data & Storage
    "High", "High", "Critical", "High", "High",
    
    # System & Performance
    "High", "High", "Medium", "High", "High",
]

# ==================== TRAINING FUNCTION ====================
def train_category_model():
    """
    Trains TF-IDF + Logistic Regression model for category classification
    Returns the trained model pipeline
    """
    print("Training Category Classification Model...")
    
    # Create pipeline: TF-IDF vectorizer + Logistic Regression classifier
    category_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=500,           # Limit vocabulary size
            stop_words='english',        # Remove common English words
            ngram_range=(1, 2),          # Use unigrams and bigrams
            min_df=1,                    # Minimum document frequency
            max_df=0.8                   # Maximum document frequency
        )),
        ('classifier', LogisticRegression(
            max_iter=200,
            random_state=42,
            multi_class='multinomial'
        ))
    ])
    
    # Train the model
    category_pipeline.fit(training_descriptions, training_categories)
    print(f"  ✓ Trained on {len(training_descriptions)} samples")
    print(f"  ✓ Categories: {set(training_categories)}")
    
    return category_pipeline


def train_priority_model():
    """
    Trains TF-IDF + SVM model for priority prediction
    Returns the trained model pipeline
    """
    print("Training Priority Prediction Model...")
    
    # Create pipeline: TF-IDF vectorizer + SVM classifier
    priority_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )),
        ('classifier', SVC(
            kernel='rbf',
            probability=True,           # Enable probability estimates
            random_state=42
        ))
    ])
    
    # Train the model
    priority_pipeline.fit(training_descriptions, training_priorities)
    print(f"  ✓ Trained on {len(training_descriptions)} samples")
    print(f"  ✓ Priorities: {set(training_priorities)}")
    
    return priority_pipeline


def save_models(category_model, priority_model):
    """
    Saves trained models to disk as .pkl files
    """
    print("\nSaving Models to Disk...")
    
    # Save category model
    category_path = os.path.join(MODELS_DIR, 'category_model.pkl')
    joblib.dump(category_model, category_path)
    print(f"  ✓ Category model saved: {category_path}")
    
    # Save priority model
    priority_path = os.path.join(MODELS_DIR, 'priority_model.pkl')
    joblib.dump(priority_model, priority_path)
    print(f"  ✓ Priority model saved: {priority_path}")


def main():
    """
    Main function: trains and saves all required models
    """
    print("=" * 60)
    print("🧠 AI TICKET SYSTEM - MODEL TRAINING")
    print("=" * 60)
    
    # Train models
    category_model = train_category_model()
    priority_model = train_priority_model()
    
    # Save models
    save_models(category_model, priority_model)
    
    print("\n" + "=" * 60)
    print("✅ Model Training Complete!")
    print("=" * 60)
    print("\nModels ready for prediction. Run: streamlit run ui/app.py")


if __name__ == "__main__":
    main()
