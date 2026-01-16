"""
Utility Functions Module
Contains helper functions for ticket ID generation, JSON formatting, and other utilities
"""

import json
import uuid
from datetime import datetime
from typing import Tuple
import os


class TicketIDGenerator:
    """
    Generates unique ticket IDs in the format INC-XXXX
    """
    
    # Counter to track tickets created in this session
    _counter = 1000
    
    @classmethod
    def generate_ticket_id(cls) -> str:
        """
        Generate a unique ticket ID
        Format: INC-XXXX (where XXXX is a sequential number)
        
        Returns:
            str: Unique ticket ID
        
        Example:
            >>> TicketIDGenerator.generate_ticket_id()
            'INC-1001'
            >>> TicketIDGenerator.generate_ticket_id()
            'INC-1002'
        """
        cls._counter += 1
        return f"INC-{cls._counter}"
    
    @classmethod
    def reset_counter(cls):
        """Reset counter to initial value (for testing)"""
        cls._counter = 1000


def get_current_timestamp() -> str:
    """
    Get current timestamp in standard format
    
    Returns:
        str: Timestamp in format 'YYYY-MM-DD HH:MM:SS'
    
    Example:
        >>> get_current_timestamp()
        '2025-01-16 14:30:45'
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_ticket_json(
    ticket_id: str,
    title: str,
    description: str,
    cleaned_description: str,
    category: str,
    priority: str,
    category_confidence: float,
    priority_confidence: float,
    entities: dict
) -> dict:
    """
    Create structured ticket JSON object
    
    Args:
        ticket_id (str): Unique ticket identifier
        title (str): Short title/subject of ticket
        description (str): Full description of issue
        cleaned_description (str): Preprocessed description
        category (str): ML-predicted category
        priority (str): ML-predicted priority
        category_confidence (float): Confidence score for category (0-1)
        priority_confidence (float): Confidence score for priority (0-1)
        entities (dict): Extracted entities (usernames, devices, error codes)
    
    Returns:
        dict: Structured ticket dictionary
    
    Example:
        >>> ticket = create_ticket_json(
        ...     ticket_id="INC-1001",
        ...     title="Unable to Login",
        ...     description="Cannot access portal",
        ...     cleaned_description="cannot access portal",
        ...     category="Access",
        ...     priority="High",
        ...     category_confidence=0.94,
        ...     priority_confidence=0.87,
        ...     entities={'usernames': [], 'devices': [], 'error_codes': []}
        ... )
    """
    
    # Calculate average confidence
    avg_confidence = round((category_confidence + priority_confidence) / 2, 4)
    
    ticket = {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "cleaned_description": cleaned_description,
        "category": category,
        "category_confidence": round(category_confidence, 4),
        "priority": priority,
        "priority_confidence": round(priority_confidence, 4),
        "avg_confidence": avg_confidence,
        "entities": entities,
        "status": "Open",  # Default status as per requirements
        "created_at": get_current_timestamp()
    }
    
    return ticket


def ticket_to_json_string(ticket: dict, indent: int = 2) -> str:
    """
    Convert ticket dictionary to formatted JSON string
    
    Args:
        ticket (dict): Ticket dictionary
        indent (int): Indentation level for pretty printing
    
    Returns:
        str: JSON formatted string
    
    Example:
        >>> ticket = {'ticket_id': 'INC-1001', 'category': 'Access'}
        >>> json_str = ticket_to_json_string(ticket)
    """
    return json.dumps(ticket, indent=indent, ensure_ascii=False)


def save_ticket_to_file(ticket: dict, output_dir: str = None) -> str:
    """
    Save ticket JSON to a file
    
    Args:
        ticket (dict): Ticket dictionary
        output_dir (str): Directory to save file. If None, uses 'tickets_output'
    
    Returns:
        str: Path to saved file
    
    Example:
        >>> ticket = {'ticket_id': 'INC-1001'}
        >>> filepath = save_ticket_to_file(ticket)
        >>> print(f"Saved to {filepath}")
    """
    if output_dir is None:
        output_dir = 'tickets_output'
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create filename with ticket ID and timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"ticket_{ticket['ticket_id']}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(ticket, f, indent=2, ensure_ascii=False)
    
    return filepath


def extract_title_from_description(description: str, max_length: int = 50) -> str:
    """
    Auto-generate ticket title from description
    Takes first meaningful part of text
    
    Args:
        description (str): Full ticket description
        max_length (int): Maximum title length
    
    Returns:
        str: Generated title
    
    Example:
        >>> desc = "I am unable to login to the company portal after password reset"
        >>> extract_title_from_description(desc)
        'Unable to login to company portal'
    """
    # Clean and shorten
    title = description.strip()
    
    # Take first sentence or first max_length chars
    if '.' in title:
        title = title.split('.')[0]
    
    if len(title) > max_length:
        # Find last space before max_length
        title = title[:max_length].rsplit(' ', 1)[0] + '...'
    
    # Capitalize first letter
    title = title[0].upper() + title[1:] if title else "Support Ticket"
    
    return title


def format_confidence_percentage(confidence: float) -> str:
    """
    Format confidence score as percentage string
    
    Args:
        confidence (float): Confidence score (0-1)
    
    Returns:
        str: Formatted percentage string
    
    Example:
        >>> format_confidence_percentage(0.9234)
        '92.34%'
    """
    return f"{confidence * 100:.2f}%"


def get_confidence_color(confidence: float) -> str:
    """
    Get color indicator based on confidence level
    For UI display purposes
    
    Args:
        confidence (float): Confidence score (0-1)
    
    Returns:
        str: Color code or label
    """
    if confidence >= 0.9:
        return "green"  # High confidence
    elif confidence >= 0.7:
        return "yellow"  # Medium confidence
    else:
        return "red"  # Low confidence


def validate_ticket_input(description: str) -> Tuple[bool, str]:
    """
    Validate ticket input before processing
    
    Args:
        description (str): User input description
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    
    Example:
        >>> is_valid, msg = validate_ticket_input("  ")
        >>> is_valid
        False
        >>> msg
        'Description cannot be empty'
    """
    if not description or not description.strip():
        return False, "Description cannot be empty"
    
    if len(description.strip()) < 10:
        return False, "Description must be at least 10 characters long"
    
    if len(description) > 5000:
        return False, "Description cannot exceed 5000 characters"
    
    return True, ""
