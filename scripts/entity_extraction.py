"""
Entity Extraction Module
Extracts structured information from ticket text using regex patterns
Used to populate the 'entities' section of the ticket JSON
"""

import re


def extract_usernames(text):
    """
    Extract username patterns from text
    Matches patterns like: @username, user=something, username:
    
    Args:
        text (str): Input text to search
    
    Returns:
        list: List of extracted usernames
    """
    usernames = []
    
    # Pattern 1: @mention style usernames
    mention_pattern = r'@(\w+)'
    usernames.extend(re.findall(mention_pattern, text, re.IGNORECASE))
    
    # Pattern 2: user=username or user:username
    user_pattern = r'(?:user\s*[:=]\s*)(\w+)'
    usernames.extend(re.findall(user_pattern, text, re.IGNORECASE))
    
    # Pattern 3: username like john.smith or john_smith
    email_like = r'([a-zA-Z]+[._]?[a-zA-Z]+)@(?:company|infosys|corp)'
    usernames.extend(re.findall(email_like, text, re.IGNORECASE))
    
    # Remove duplicates and return
    return list(set([u.lower() for u in usernames if u]))


def extract_devices(text):
    """
    Extract device/machine names from text
    Matches patterns like: SERVER-NAME, DEVICE-01, MacBook, Laptop, etc.
    
    Args:
        text (str): Input text to search
    
    Returns:
        list: List of extracted device names
    """
    devices = []
    
    # Pattern 1: All-caps device names (SERVER, DEVICE, etc.)
    caps_pattern = r'\b([A-Z]{2,}[A-Z0-9\-]*)\b'
    devices.extend(re.findall(caps_pattern, text))
    
    # Pattern 2: Common device names
    common_devices = [
        'laptop', 'desktop', 'server', 'printer', 'monitor',
        'keyboard', 'mouse', 'external drive', 'hard drive',
        'macbook', 'windows', 'linux', 'ipad', 'iphone',
        'router', 'switch', 'gateway'
    ]
    
    text_lower = text.lower()
    for device in common_devices:
        if device in text_lower:
            # Use more specific pattern to get context
            pattern = rf'\b({device}(?:\s+(?:pro|air|mini))?)\b'
            found = re.findall(pattern, text_lower)
            devices.extend(found)
    
    # Remove duplicates and return
    return list(set([d.strip() for d in devices if d.strip()]))


def extract_error_codes(text):
    """
    Extract error codes and error messages from text
    Matches patterns like: ERROR-404, 0x80070005, Code: 500, etc.
    
    Args:
        text (str): Input text to search
    
    Returns:
        list: List of extracted error codes
    """
    error_codes = []
    
    # Pattern 1: ERROR-### or ERROR### format
    error_number = r'(?:ERROR|ERR|CODE)\s*[-:]?\s*([0-9A-Fa-f]+)'
    error_codes.extend(re.findall(error_number, text, re.IGNORECASE))
    
    # Pattern 2: Hexadecimal error codes like 0x80070005
    hex_pattern = r'0x[0-9A-Fa-f]+'
    error_codes.extend(re.findall(hex_pattern, text, re.IGNORECASE))
    
    # Pattern 3: HTTP status codes
    http_pattern = r'\b([45]\d{2})\b'  # 4xx or 5xx status codes
    found_http = re.findall(http_pattern, text)
    error_codes.extend(found_http)
    
    # Pattern 4: Common error codes (Windows/System)
    common_errors = ['404', '500', '503', '403', '401', 'BSOD', 'STOP']
    for err in common_errors:
        if err in text.upper():
            error_codes.append(err)
    
    # Remove duplicates and return
    return list(set([e.strip() for e in error_codes if e.strip()]))


def extract_email_addresses(text):
    """
    Extract email addresses from text
    
    Args:
        text (str): Input text to search
    
    Returns:
        list: List of extracted email addresses
    """
    # Standard email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return list(set(emails))


def extract_urls(text):
    """
    Extract URLs/links from text
    
    Args:
        text (str): Input text to search
    
    Returns:
        list: List of extracted URLs
    """
    # URL pattern for http/https
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, text)
    return list(set(urls))


def extract_file_paths(text):
    """
    Extract file paths from text
    Matches patterns like: C:\\Users\\..., /home/user/..., etc.
    
    Args:
        text (str): Input text to search
    
    Returns:
        list: List of extracted file paths
    """
    paths = []
    
    # Windows paths: C:\Users\something
    windows_pattern = r'[A-Z]:\\(?:[^\s\\]*\\)*[^\s\\]*'
    paths.extend(re.findall(windows_pattern, text))
    
    # Linux/Mac paths: /path/to/something
    unix_pattern = r'/(?:[a-zA-Z0-9._\-/]*)'
    paths.extend(re.findall(unix_pattern, text))
    
    # Network paths: \\server\share
    network_pattern = r'\\\\[^\s\\]+\\[^\s\\]+'
    paths.extend(re.findall(network_pattern, text))
    
    return list(set(paths))


def extract_all_entities(text):
    """
    Master function to extract all types of entities from text
    
    Args:
        text (str): Input text to analyze
    
    Returns:
        dict: Dictionary containing all extracted entities
    
    Example:
        >>> text = "User john.smith has ERROR-500 on SERVER-01"
        >>> extract_all_entities(text)
        {
            'usernames': ['john.smith'],
            'devices': ['SERVER-01'],
            'error_codes': ['500'],
            'emails': [],
            'urls': [],
            'file_paths': []
        }
    """
    entities = {
        'usernames': extract_usernames(text),
        'devices': extract_devices(text),
        'error_codes': extract_error_codes(text),
        'emails': extract_email_addresses(text),
        'urls': extract_urls(text),
        'file_paths': extract_file_paths(text)
    }
    
    return entities


def get_entities_summary(entities):
    """
    Generate a readable summary of extracted entities
    
    Args:
        entities (dict): Dictionary of extracted entities
    
    Returns:
        str: Human-readable summary
    """
    summary_parts = []
    
    for entity_type, values in entities.items():
        if values:
            summary_parts.append(f"  • {entity_type}: {', '.join(values)}")
    
    if not summary_parts:
        return "  • No specific entities detected"
    
    return '\n'.join(summary_parts)
