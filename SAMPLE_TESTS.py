"""
Sample Test Cases & Examples
Use these to test and understand the AI Ticket System
"""

# Test Case 1: Network Issue
SAMPLE_1 = {
    "input": """
    I cannot connect to the company WiFi network. The error shows "Network is unreachable". 
    I'm on my MacBook and tried rebooting but still no connection. This is blocking my work!
    """,
    "expected_category": "Network",
    "expected_priority": "High"
}

# Test Case 2: Access Issue
SAMPLE_2 = {
    "input": """
    I'm locked out of my email account after too many failed login attempts. 
    I need to reset my password but the reset link is not working. 
    Error: Invalid credentials. This is urgent!
    """,
    "expected_category": "Access",
    "expected_priority": "High"
}

# Test Case 3: Hardware Issue
SAMPLE_3 = {
    "input": """
    My laptop screen is flickering constantly and making strange noises. 
    The display looks like it's about to fail. 
    I'm concerned the hardware might be damaged.
    """,
    "expected_category": "Hardware",
    "expected_priority": "Medium"
}

# Test Case 4: Software Issue
SAMPLE_4 = {
    "input": """
    Microsoft Word crashes every time I try to open a document larger than 50MB. 
    The application freezes and I have to force quit. 
    This is affecting my productivity.
    """,
    "expected_category": "Software",
    "expected_priority": "Medium"
}

# Test Case 5: Storage Issue
SAMPLE_5 = {
    "input": """
    My disk space is critically low. C drive shows only 100MB free. 
    I'm getting out of disk space warnings constantly. 
    I cannot save files anymore. This is critical!
    """,
    "expected_category": "Storage",
    "expected_priority": "Critical"
}

# Test Case 6: System Performance Issue
SAMPLE_6 = {
    "input": """
    My computer has become extremely slow. 
    Every task takes forever to complete. 
    CPU and memory usage are maxed out. 
    The system is barely usable.
    """,
    "expected_category": "System",
    "expected_priority": "High"
}

# Test Case 7: Complex Multi-Issue Ticket
SAMPLE_7 = {
    "input": """
    I'm experiencing multiple issues on my Windows laptop (DEVICE-12345). 
    First, I cannot access the shared network drive \\\\SERVER-01\\projects. 
    Second, I'm getting error code 0x80070005 when trying to authenticate. 
    Third, my printer HP-LaserJet-5 won't print from my computer. 
    User john.smith@company.com has the same issues. 
    This needs to be resolved ASAP!
    """,
    "expected_category": "Access or Network",
    "expected_priority": "High"
}

# ============================================================================

"""
HOW TO USE THESE SAMPLES:

1. Copy a sample description
2. Paste into the Streamlit UI
3. Click "Generate Ticket"
4. Check if predictions match expected results
5. Review confidence scores

TESTING IN CODE:
"""

def test_samples():
    """
    Test all samples programmatically
    Run this in your Python environment
    """
    from scripts.preprocess import preprocess_text
    from scripts.predict import create_predictor
    from scripts.entity_extraction import extract_all_entities
    
    samples = [SAMPLE_1, SAMPLE_2, SAMPLE_3, SAMPLE_4, SAMPLE_5, SAMPLE_6, SAMPLE_7]
    predictor = create_predictor()
    
    for i, sample in enumerate(samples, 1):
        print(f"\n{'='*70}")
        print(f"TEST CASE {i}")
        print(f"{'='*70}")
        
        description = sample['input'].strip()
        print(f"Input: {description[:100]}...")
        
        # Preprocess
        cleaned = preprocess_text(description)
        print(f"\nCleaned: {cleaned[:80]}...")
        
        # Predict
        results = predictor.predict_all(cleaned)
        print(f"\nPredicted Category: {results['category']} ({results['category_confidence']:.2%})")
        print(f"Predicted Priority: {results['priority']} ({results['priority_confidence']:.2%})")
        
        print(f"\nExpected Category: {sample['expected_category']}")
        print(f"Expected Priority: {sample['expected_priority']}")
        
        # Extract entities
        entities = extract_all_entities(description)
        if any(entities.values()):
            print(f"\nExtracted Entities:")
            for entity_type, values in entities.items():
                if values:
                    print(f"  {entity_type}: {values}")

if __name__ == "__main__":
    # Run this to test all samples
    test_samples()

# ============================================================================

"""
EXPECTED PATTERNS:

Network Issues typically contain:
- Keywords: connect, network, wifi, internet, connection, unreachable, signal
- Priority: Usually Medium-High

Access Issues typically contain:
- Keywords: login, access, password, authentication, locked, permission, denied
- Priority: Usually High

Hardware Issues typically contain:
- Keywords: screen, keyboard, mouse, printer, laptop, desktop, device, fan, noise
- Priority: Usually Medium

Software Issues typically contain:
- Keywords: crash, freeze, error, application, word, excel, freeze, quit
- Priority: Usually Low-Medium

Storage Issues typically contain:
- Keywords: disk, space, storage, drive, backup, quota, save
- Priority: Usually High-Critical

System Issues typically contain:
- Keywords: slow, performance, cpu, memory, boot, restart, hang, freeze
- Priority: Usually Medium-High
"""
