# 🎫 AI-Powered Ticket Creation & Categorization System

An intelligent support ticket system that automatically creates, categorizes, and prioritizes IT support tickets using **Machine Learning** and **Natural Language Processing**.

## 📌 Project Overview

This system converts free-text IT issue descriptions into structured support tickets by leveraging pre-trained ML models. Instead of using hardcoded rules, the system learns from data to intelligently classify tickets and assign priorities.

**Key Features:**
- 🧠 **ML-Based Classification** - Uses TF-IDF + Logistic Regression/SVM models
- 🏷️ **Automatic Categorization** - Classifies tickets into 6 categories (Network, Access, Hardware, Software, Storage, System)
- 📊 **Priority Prediction** - Predicts priority levels (Critical, High, Medium, Low)
- 🔍 **Entity Extraction** - Extracts usernames, devices, error codes from descriptions
- 🧹 **Text Preprocessing** - Includes stemming, lemmatization, stopword removal
- 📝 **Structured Output** - Generates JSON-formatted tickets
- 🎨 **User-Friendly UI** - Clean Streamlit web interface
- 📊 **Confidence Scores** - Shows model confidence for predictions

---

## 📁 Project Structure

```
AI-Ticket-Project/
│
├── models/                          # Pre-trained ML models (generated at runtime)
│   ├── category_model.pkl           # Category classification model
│   └── priority_model.pkl           # Priority prediction model
│
├── scripts/                         # Core Python modules
│   ├── train_models.py              # Trains and saves ML models
│   ├── preprocess.py                # Text preprocessing pipeline
│   ├── predict.py                   # Model prediction logic
│   ├── entity_extraction.py         # Entity extraction using regex
│   └── utils.py                     # Utility functions
│
├── ui/
│   └── app.py                       # Streamlit web application
│
├── data/
│   ├── raw/                         # Store raw input data here
│   └── cleaned/                     # Store preprocessed data here
│
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🧠 Machine Learning Architecture

### Model Pipeline

```
User Input Text
    ↓
[TEXT PREPROCESSING]
    • Lowercasing
    • Punctuation removal
    • Number removal
    • Stopword removal
    • Lemmatization
    • Whitespace cleanup
    ↓
[TF-IDF VECTORIZATION]
    • Converts text to numerical features
    • Max features: 500
    • Bigram support (1-2 grams)
    ↓
[ML MODEL PREDICTION]
    ┌─────────────────────────────┬──────────────────────┐
    │                             │                      │
    ↓                             ↓                      ↓
[CATEGORY MODEL]        [PRIORITY MODEL]        [ENTITY EXTRACTION]
Logistic Regression     SVM (RBF Kernel)        Regex-based patterns
    ↓                             ↓                      ↓
Output: Category        Output: Priority        Output: Entities
+ Confidence Score      + Confidence Score      (usernames, devices, errors)
    ↓                             ↓                      ↓
    └─────────────────────────────┴──────────────────────┘
                        ↓
            [STRUCTURED JSON TICKET]
```

### Model Details

| Component | Algorithm | Input | Output |
|-----------|-----------|-------|--------|
| **Vectorizer** | TF-IDF | Raw text | 500-dim numerical vector |
| **Category Model** | Logistic Regression | Vectorized text | Category + Confidence |
| **Priority Model** | SVM (RBF) | Vectorized text | Priority + Confidence |
| **Entity Extractor** | Regex Patterns | Raw text | Entities (list) |

### Training Data

The system is trained on 30 IT support ticket descriptions covering:
- **Network & Connectivity** (5 samples)
- **Access & Authentication** (5 samples)
- **Hardware** (5 samples)
- **Software & Applications** (5 samples)
- **Data & Storage** (5 samples)
- **System & Performance** (5 samples)

**Classes:**
- **Categories**: Network, Access, Hardware, Software, Storage, System
- **Priorities**: Critical, High, Medium, Low

---

## 🔄 Data Flow & Pipeline

### Complete Workflow

```
1. USER SUBMITS TICKET
   └─→ Raw text input from web interface

2. INPUT VALIDATION
   └─→ Check if text is valid (length, content)

3. TEXT PREPROCESSING
   └─→ Run through preprocessing pipeline
   └─→ Output: cleaned text for ML

4. ENTITY EXTRACTION
   └─→ Extract usernames, devices, error codes using regex
   └─→ Output: structured entities dict

5. ML PREDICTIONS
   ├─→ Load pre-trained models
   ├─→ Predict Category + confidence
   ├─→ Predict Priority + confidence

6. TICKET GENERATION
   └─→ Combine all data into structured JSON

7. DISPLAY & EXPORT
   ├─→ Show in web UI with formatting
   ├─→ Allow JSON download
   └─→ Save to file (optional)
```

### Example End-to-End Flow

**Input:**
```
"I am unable to login to the company portal. I get error code 0x80070005 
after resetting my password on my laptop. This is urgent!"
```

**Processing:**
1. **Preprocessing** → `unable login company portal error password reset laptop urgent`
2. **Entity Extraction** → `{error_codes: ['0x80070005'], devices: ['laptop']}`
3. **Category Prediction** → `Access` (94.5% confidence)
4. **Priority Prediction** → `High` (87.3% confidence)

**Output:**
```json
{
  "ticket_id": "INC-1001",
  "title": "Unable to login to company portal",
  "description": "I am unable to login to the company portal...",
  "cleaned_description": "unable login company portal error password reset...",
  "category": "Access",
  "category_confidence": 0.945,
  "priority": "High",
  "priority_confidence": 0.873,
  "avg_confidence": 0.909,
  "entities": {
    "usernames": [],
    "devices": ["laptop"],
    "error_codes": ["0x80070005"],
    "emails": [],
    "urls": [],
    "file_paths": []
  },
  "status": "Open",
  "created_at": "2025-01-16 14:30:45"
}
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+ installed
- Windows/Mac/Linux OS
- ~500MB disk space

### Step 1: Clone/Setup Project
```bash
cd c:\Users\ABHINAY\AI Ticket project
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train ML Models
```bash
# This generates the .pkl model files
python scripts/train_models.py
```

**Output:**
```
============================================================
🧠 AI TICKET SYSTEM - MODEL TRAINING
============================================================
Training Category Classification Model...
  ✓ Trained on 30 samples
  ✓ Categories: {'Network', 'Access', 'Hardware', 'Software', 'Storage', 'System'}
Training Priority Prediction Model...
  ✓ Trained on 30 samples
  ✓ Priorities: {'Critical', 'High', 'Medium', 'Low'}

Saving Models to Disk...
  ✓ Category model saved: models/category_model.pkl
  ✓ Priority model saved: models/priority_model.pkl

============================================================
✅ Model Training Complete!
============================================================
```

### Step 5: Run Streamlit Application
```bash
streamlit run ui/app.py
```

The app will open automatically at `http://localhost:8501`

---

## 📖 How to Use the Application

### User Interface Walkthrough

#### 1. **Main Input Area**
   - Enter your IT issue description in the text area
   - Minimum: 10 characters
   - Maximum: 5000 characters

#### 2. **Generate Ticket Button**
   - Click to process your input
   - System will analyze and predict

#### 3. **Results Section**
   Shows:
   - **Ticket ID** (auto-generated, format: INC-XXXX)
   - **Category** with confidence score
   - **Priority** with confidence score
   - **Average Confidence** (overall model confidence)

#### 4. **Detailed Analysis**
   - Category classification details
   - Priority level prediction details
   - Current status (always starts as "Open")
   - Creation timestamp

#### 5. **Extracted Entities**
   - Usernames detected
   - Devices mentioned
   - Error codes found
   - Email addresses
   - URLs
   - File paths

#### 6. **Full Ticket JSON**
   - Complete structured ticket in JSON format
   - Download as file
   - Save to disk

### Example Usage

**Scenario: Network Connectivity Issue**

Input:
```
"I cannot connect to the company WiFi network. 
The error shows network unreachable. 
I'm on my MacBook and tried rebooting but still no connection. 
This is blocking my work!"
```

Expected Output:
```
Ticket ID: INC-1023
Category: Network (95% confidence)
Priority: High (88% confidence)
Entities: devices=['macbook'], error_codes=['network unreachable']
```

---

## 📝 API Reference

### Core Modules

#### `preprocess.py`
```python
from preprocess import preprocess_text

# Clean raw text for ML
cleaned = preprocess_text("Unable to LOGIN to company portal!")
# Output: "unable login company portal"
```

#### `predict.py`
```python
from predict import create_predictor

predictor = create_predictor()

# Single prediction
category, confidence = predictor.predict_category("unable login to portal")
priority, confidence = predictor.predict_priority("unable login to portal")

# Both predictions
results = predictor.predict_all("unable login to portal")
# {category: "Access", category_confidence: 0.945, priority: "High", ...}
```

#### `entity_extraction.py`
```python
from entity_extraction import extract_all_entities

entities = extract_all_entities("Error 0x80070005 on SERVER-01")
# {usernames: [], devices: ['SERVER-01'], error_codes: ['0x80070005'], ...}
```

#### `utils.py`
```python
from utils import TicketIDGenerator, create_ticket_json

ticket_id = TicketIDGenerator.generate_ticket_id()  # INC-1001

ticket = create_ticket_json(
    ticket_id="INC-1001",
    title="Access Issue",
    description="...",
    cleaned_description="...",
    category="Access",
    priority="High",
    category_confidence=0.94,
    priority_confidence=0.87,
    entities={...}
)
```

---

## 🎯 Training Custom Models

To train models on your own data:

### 1. Prepare Training Data
Create a CSV or modify `scripts/train_models.py`:

```python
training_descriptions = [
    "your issue description 1",
    "your issue description 2",
    # ... more descriptions
]

training_categories = ["Category1", "Category2", ...]
training_priorities = ["High", "Low", ...]
```

### 2. Run Training
```bash
python scripts/train_models.py
```

### 3. Models Auto-Save
Models are saved as:
- `models/category_model.pkl`
- `models/priority_model.pkl`

---

## 📊 Sample Outputs

### Sample Ticket JSON
```json
{
  "ticket_id": "INC-1001",
  "title": "Unable to login to company portal",
  "description": "I cannot access the company portal after resetting my password",
  "cleaned_description": "unable login company portal password reset",
  "category": "Access",
  "category_confidence": 0.9234,
  "priority": "High",
  "priority_confidence": 0.8756,
  "avg_confidence": 0.8995,
  "entities": {
    "usernames": [],
    "devices": [],
    "error_codes": [],
    "emails": [],
    "urls": [],
    "file_paths": []
  },
  "status": "Open",
  "created_at": "2025-01-16 14:30:00"
}
```

### Confidence Score Interpretation
- **90-100%**: Very confident prediction (high quality)
- **70-89%**: Fairly confident prediction (good quality)
- **50-69%**: Uncertain prediction (review recommended)
- **<50%**: Low confidence (consider manual review)

---

## 🐛 Troubleshooting

### Issue: "Models not found"
**Solution:**
```bash
python scripts/train_models.py
```

### Issue: "NLTK data missing"
**Solution:** Modules auto-download on first run. If issues persist:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Issue: Streamlit not found
**Solution:**
```bash
pip install streamlit==1.28.1
```

### Issue: Poor predictions
**Solutions:**
1. Provide more detailed descriptions
2. Include error codes/messages if available
3. Consider training with more/better quality data

---

## 📚 Technologies & Libraries

| Technology | Purpose | Version |
|-----------|---------|---------|
| **scikit-learn** | ML algorithms (LR, SVM, TF-IDF) | 1.3.2 |
| **NLTK** | NLP preprocessing (tokenization, lemmatization) | 3.8.1 |
| **Streamlit** | Web UI framework | 1.28.1 |
| **joblib** | Model serialization (.pkl files) | 1.3.2 |
| **NumPy** | Numerical computing | 1.24.3 |

---

## 💡 Key Design Decisions

1. **TF-IDF + ML Models**: Chosen for their balance of simplicity and effectiveness in text classification without needing large datasets.

2. **Pipeline Architecture**: Separate modules for preprocessing, prediction, and extraction enable easy maintenance and testing.

3. **Streamlit UI**: Provides fast, professional web interface without frontend complexity.

4. **Regex-Based Entity Extraction**: Lightweight alternative to NER models, sufficient for IT ticket use case.

5. **JSON Output Format**: Industry-standard, easily integrable with other systems.

6. **Session-Based History**: Tracks tickets created in current session for quick reference.

---

## 🚀 Future Enhancements

- [ ] Deep learning models (BERT, transformer-based) for better accuracy
- [ ] Named Entity Recognition (NER) for advanced entity extraction
- [ ] Database integration (SQLite, PostgreSQL)
- [ ] REST API for system integration
- [ ] Multi-language support
- [ ] Feedback loop for model improvement
- [ ] Advanced visualization dashboards
- [ ] Batch ticket processing
- [ ] Integration with ticketing systems (Jira, ServiceNow, etc.)
- [ ] Sentiment analysis for urgency detection

---

## 📝 Notes for Interview/Viva Explanation

### Key Points to Highlight:

1. **ML Approach**: "The system uses trained ML models instead of hardcoded rules, making it scalable and adaptable to new ticket types."

2. **Pipeline Design**: "Clear separation of concerns - preprocessing → prediction → output - makes the code maintainable and testable."

3. **Confidence Scores**: "ML models provide probability estimates showing how confident they are in predictions, which is important for decision-making."

4. **Text Preprocessing**: "Multiple preprocessing steps (lemmatization, stopword removal, etc.) standardize input and improve model accuracy."

5. **Entity Extraction**: "Regex patterns extract structured information like error codes and devices, adding value to tickets."

6. **Production-Ready**: "The code uses industry practices - modular design, error handling, configuration management, logging-ready structure."

---

## 📄 License & Credits

**Author**: AI Intern, Infosys Springboard

**Project**: AI-Powered Ticket Creation and Categorization System

For any questions or improvements, feel free to reach out!

---

## 🔗 Quick Links

- **Run App**: `streamlit run ui/app.py`
- **Train Models**: `python scripts/train_models.py`
- **Dependencies**: `pip install -r requirements.txt`
- **Python Docs**: https://docs.python.org/3/
- **Scikit-learn**: https://scikit-learn.org/
- **Streamlit Docs**: https://docs.streamlit.io/

---

**Last Updated**: January 16, 2025

**Status**: ✅ Production Ready
