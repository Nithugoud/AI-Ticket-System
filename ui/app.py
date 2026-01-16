"""
AI-Powered Ticket Creation & Categorization System
Streamlit UI Application

A production-ready web application for creating, categorizing, and prioritizing
IT support tickets using machine learning models trained on historical data.

Run with: streamlit run ui/app.py
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add scripts directory to path for imports
scripts_path = os.path.join(os.path.dirname(__file__), '..', 'scripts')
sys.path.insert(0, scripts_path)

# Import custom modules
from preprocess import preprocess_text, get_preprocessing_summary
from entity_extraction import extract_all_entities, get_entities_summary
from predict import create_predictor
from utils import (
    TicketIDGenerator, 
    create_ticket_json,
    ticket_to_json_string,
    extract_title_from_description,
    format_confidence_percentage,
    get_confidence_color,
    validate_ticket_input,
    save_ticket_to_file
)


# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AI Ticket System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 14px;
    }
    .confidence-high {
        color: #00cc00;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffaa00;
        font-weight: bold;
    }
    .confidence-low {
        color: #ff0000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("⚙️ Settings & Info")
    
    st.markdown("---")
    
    # About section
    st.subheader("📋 About")
    st.markdown("""
    **AI Ticket Creation & Categorization System**
    
    Uses trained ML models to:
    - 🏷️ Classify tickets into categories
    - 📊 Predict priority levels
    - 🔍 Extract entities from descriptions
    - 📝 Generate structured tickets
    """)
    
    st.markdown("---")
    
    # Statistics section
    if 'ticket_count' not in st.session_state:
        st.session_state.ticket_count = 0
    
    st.subheader("📊 Session Statistics")
    st.metric("Tickets Created", st.session_state.ticket_count)
    
    st.markdown("---")
    
    # Help section
    st.subheader("❓ How to Use")
    st.markdown("""
    1. **Enter Description**: Describe your IT issue in detail
    2. **Click Generate**: System analyzes and predicts category/priority
    3. **Review Ticket**: Check ML predictions and confidence scores
    4. **Download**: Save ticket as JSON file
    
    **Tips for better predictions:**
    - Be specific and detailed in descriptions
    - Include error messages or codes if available
    - Mention affected devices or systems
    """)


# ==================== MAIN CONTENT ====================
st.title("🎫 AI-Powered Ticket Creation System")
st.markdown("*Convert your issue description into a structured support ticket using AI*")

st.markdown("---")

# ==================== INITIALIZATION ====================
# Initialize session state
if 'predictor' not in st.session_state:
    with st.spinner("Loading ML models..."):
        try:
            st.session_state.predictor = create_predictor()
            st.session_state.models_loaded = True
        except FileNotFoundError as e:
            st.error(f"❌ Error loading models: {str(e)}")
            st.info("Please run: `python scripts/train_models.py` in the project directory")
            st.session_state.models_loaded = False

if 'current_ticket' not in st.session_state:
    st.session_state.current_ticket = None

if 'ticket_history' not in st.session_state:
    st.session_state.ticket_history = []


# ==================== MAIN INTERFACE ====================
if st.session_state.models_loaded:
    
    # ========== INPUT SECTION ==========
    st.subheader("📝 Ticket Description")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_area(
            "Describe your IT issue:",
            placeholder="Example: I cannot login to the company portal after resetting my password. I get an error message saying 'Invalid credentials'...",
            height=120,
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        generate_button = st.button("🔄 Generate Ticket", use_container_width=True, key="generate")
    
    st.markdown("---")
    
    # ========== PROCESSING & PREDICTION ==========
    if generate_button:
        # Validate input
        is_valid, error_msg = validate_ticket_input(user_input)
        
        if not is_valid:
            st.error(f"❌ {error_msg}")
        else:
            with st.spinner("🤖 Analyzing ticket with ML models..."):
                try:
                    # Step 1: Preprocess text
                    cleaned_text = preprocess_text(user_input)
                    
                    # Step 2: Extract entities
                    entities = extract_all_entities(user_input)
                    
                    # Step 3: ML predictions
                    predictions = st.session_state.predictor.predict_all(cleaned_text)
                    
                    # Step 4: Generate ticket
                    ticket_id = TicketIDGenerator.generate_ticket_id()
                    title = extract_title_from_description(user_input)
                    
                    ticket = create_ticket_json(
                        ticket_id=ticket_id,
                        title=title,
                        description=user_input,
                        cleaned_description=cleaned_text,
                        category=predictions['category'],
                        priority=predictions['priority'],
                        category_confidence=predictions['category_confidence'],
                        priority_confidence=predictions['priority_confidence'],
                        entities=entities
                    )
                    
                    # Store in session
                    st.session_state.current_ticket = ticket
                    st.session_state.ticket_history.append(ticket)
                    st.session_state.ticket_count += 1
                    
                    # Success message
                    st.success("✅ Ticket generated successfully!")
                
                except Exception as e:
                    st.error(f"❌ Error processing ticket: {str(e)}")
    
    # ========== RESULTS SECTION ==========
    if st.session_state.current_ticket:
        ticket = st.session_state.current_ticket
        
        st.subheader("🎯 Generated Ticket")
        
        # Main ticket information in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Ticket ID", ticket['ticket_id'])
        
        with col2:
            st.metric("Category", ticket['category'])
        
        with col3:
            st.metric("Priority", ticket['priority'])
        
        with col4:
            avg_conf = ticket['avg_confidence']
            st.metric(
                "Avg Confidence",
                format_confidence_percentage(avg_conf),
                delta=None
            )
        
        st.markdown("---")
        
        # Detailed predictions
        st.subheader("🔍 Detailed Analysis")
        
        pred_col1, pred_col2, pred_col3 = st.columns(3)
        
        with pred_col1:
            st.write("**Category Classification**")
            st.write(f"🏷️ **{ticket['category']}**")
            conf_color = get_confidence_color(ticket['category_confidence'])
            st.progress(ticket['category_confidence'])
            st.write(f"Confidence: {format_confidence_percentage(ticket['category_confidence'])}")
        
        with pred_col2:
            st.write("**Priority Level**")
            # Priority color coding
            priority_colors = {
                "Critical": "🔴",
                "High": "🟠",
                "Medium": "🟡",
                "Low": "🟢"
            }
            priority_icon = priority_colors.get(ticket['priority'], "⚪")
            st.write(f"{priority_icon} **{ticket['priority']}**")
            st.progress(ticket['priority_confidence'])
            st.write(f"Confidence: {format_confidence_percentage(ticket['priority_confidence'])}")
        
        with pred_col3:
            st.write("**Status**")
            st.write(f"✅ **{ticket['status']}**")
            st.write(f"**Created:** {ticket['created_at']}")
        
        st.markdown("---")
        
        # Entity extraction results
        st.subheader("🔎 Extracted Entities")
        
        if any(ticket['entities'].values()):
            entity_col1, entity_col2 = st.columns(2)
            
            with entity_col1:
                if ticket['entities']['usernames']:
                    st.write("**Usernames:**")
                    for user in ticket['entities']['usernames']:
                        st.write(f"  • `{user}`")
                
                if ticket['entities']['devices']:
                    st.write("**Devices:**")
                    for device in ticket['entities']['devices']:
                        st.write(f"  • `{device}`")
            
            with entity_col2:
                if ticket['entities']['error_codes']:
                    st.write("**Error Codes:**")
                    for code in ticket['entities']['error_codes']:
                        st.write(f"  • `{code}`")
                
                if ticket['entities']['emails']:
                    st.write("**Email Addresses:**")
                    for email in ticket['entities']['emails']:
                        st.write(f"  • `{email}`")
        else:
            st.info("ℹ️ No specific entities detected in the description")
        
        st.markdown("---")
        
        # Full ticket JSON
        st.subheader("📋 Full Ticket (JSON)")
        
        json_string = ticket_to_json_string(ticket)
        st.code(json_string, language="json")
        
        # Download button
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.download_button(
                label="📥 Download JSON",
                data=json_string,
                file_name=f"ticket_{ticket['ticket_id']}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            if st.button("💾 Save to File", use_container_width=True):
                filepath = save_ticket_to_file(ticket)
                st.success(f"✅ Saved to: `{filepath}`")
        
        st.markdown("---")
        
        # Preprocessing details (expandable)
        with st.expander("🔧 Text Preprocessing Details"):
            preprocess_summary = get_preprocessing_summary(
                ticket['description'],
                ticket['cleaned_description']
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Length", preprocess_summary['original_length'], "chars")
            with col2:
                st.metric("Cleaned Length", preprocess_summary['cleaned_length'], "chars")
            with col3:
                st.metric("Compression", f"{preprocess_summary['compression_ratio']}%", "reduced")
            
            st.write("**Original Text:**")
            st.write(f"> {preprocess_summary['original']}")
            
            st.write("**Processed Text (for ML):**")
            st.write(f"> `{preprocess_summary['cleaned']}`")
    
    st.markdown("---")
    
    # ========== TICKET HISTORY ==========
    if st.session_state.ticket_history:
        with st.expander("📊 Ticket History"):
            st.write(f"Total tickets created this session: **{len(st.session_state.ticket_history)}**")
            
            # Display history as table
            history_data = []
            for t in st.session_state.ticket_history:
                history_data.append({
                    "Ticket ID": t['ticket_id'],
                    "Category": t['category'],
                    "Priority": t['priority'],
                    "Confidence": f"{t['avg_confidence']:.2%}",
                    "Created": t['created_at']
                })
            
            st.table(history_data)

else:
    st.error("❌ Could not load ML models. Please ensure training is complete.")
