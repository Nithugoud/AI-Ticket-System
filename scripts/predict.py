"""
Prediction Module
Loads trained ML models and performs ticket categorization and priority prediction
"""

import joblib
import os
from typing import Tuple, Dict
import numpy as np


class TicketPredictor:
    """
    Main predictor class for ticket categorization and priority assignment
    Uses pre-trained ML models loaded from .pkl files
    """
    
    def __init__(self, models_dir: str = None):
        """
        Initialize the TicketPredictor by loading pre-trained models
        
        Args:
            models_dir (str): Path to models directory containing .pkl files
                            If None, looks for '../models' relative to script location
        """
        # Set default models directory
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        self.models_dir = models_dir
        self.category_model = None
        self.priority_model = None
        
        # Load models
        self._load_models()
    
    def _load_models(self):
        """
        Load pre-trained models from disk
        Raises error if models don't exist
        """
        # Load category model
        category_path = os.path.join(self.models_dir, 'category_model.pkl')
        if not os.path.exists(category_path):
            raise FileNotFoundError(
                f"Category model not found at {category_path}\n"
                f"Please run: python scripts/train_models.py"
            )
        self.category_model = joblib.load(category_path)
        
        # Load priority model
        priority_path = os.path.join(self.models_dir, 'priority_model.pkl')
        if not os.path.exists(priority_path):
            raise FileNotFoundError(
                f"Priority model not found at {priority_path}\n"
                f"Please run: python scripts/train_models.py"
            )
        self.priority_model = joblib.load(priority_path)
    
    def predict_category(self, text: str) -> Tuple[str, float]:
        """
        Predict ticket category using trained ML model
        
        Args:
            text (str): Preprocessed ticket description
        
        Returns:
            Tuple[str, float]: (predicted_category, confidence_score)
        
        Example:
            >>> predictor = TicketPredictor()
            >>> category, confidence = predictor.predict_category("unable login to company portal")
            >>> print(f"Category: {category}, Confidence: {confidence:.2%}")
            Category: Access, Confidence: 94.23%
        """
        # Get prediction
        prediction = self.category_model.predict([text])[0]
        
        # Get confidence score (probability of predicted class)
        probabilities = self.category_model.predict_proba([text])[0]
        confidence = float(np.max(probabilities))
        
        return prediction, confidence
    
    def predict_priority(self, text: str) -> Tuple[str, float]:
        """
        Predict ticket priority using trained ML model
        
        Args:
            text (str): Preprocessed ticket description
        
        Returns:
            Tuple[str, float]: (predicted_priority, confidence_score)
        
        Example:
            >>> predictor = TicketPredictor()
            >>> priority, confidence = predictor.predict_priority("data loss in critical files")
            >>> print(f"Priority: {priority}, Confidence: {confidence:.2%}")
            Priority: Critical, Confidence: 89.45%
        """
        # Get prediction
        prediction = self.priority_model.predict([text])[0]
        
        # Get confidence score
        probabilities = self.priority_model.predict_proba([text])[0]
        confidence = float(np.max(probabilities))
        
        return prediction, confidence
    
    def predict_all(self, text: str) -> Dict:
        """
        Perform both category and priority predictions
        
        Args:
            text (str): Preprocessed ticket description
        
        Returns:
            dict: Dictionary containing both predictions and confidence scores
        
        Example:
            >>> predictor = TicketPredictor()
            >>> results = predictor.predict_all("unable login after password reset")
            >>> results
            {
                'category': 'Access',
                'category_confidence': 0.9234,
                'priority': 'High',
                'priority_confidence': 0.8756
            }
        """
        category, category_conf = self.predict_category(text)
        priority, priority_conf = self.predict_priority(text)
        
        return {
            'category': category,
            'category_confidence': round(category_conf, 4),
            'priority': priority,
            'priority_confidence': round(priority_conf, 4)
        }
    
    def get_model_classes(self) -> Dict[str, list]:
        """
        Get all possible classes (categories and priorities) that models can predict
        Useful for understanding model capabilities
        
        Returns:
            dict: Dictionary with 'categories' and 'priorities' lists
        """
        return {
            'categories': list(self.category_model.classes_),
            'priorities': list(self.priority_model.classes_)
        }


def create_predictor(models_dir: str = None) -> TicketPredictor:
    """
    Factory function to create a TicketPredictor instance
    
    Args:
        models_dir (str): Optional path to models directory
    
    Returns:
        TicketPredictor: Initialized predictor instance
    
    Raises:
        FileNotFoundError: If models don't exist
    """
    return TicketPredictor(models_dir)
