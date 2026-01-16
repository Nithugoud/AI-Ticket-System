# 🚀 Quick Start Guide

Get the AI Ticket System up and running in 5 minutes!

## ⚡ Quick Setup (Windows PowerShell)

### 1. Navigate to Project
```powershell
cd "c:\Users\ABHINAY\AI Ticket project"
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\Activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Train ML Models (One-time setup)
```powershell
python scripts/train_models.py
```

**Expected Output:**
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

### 5. Launch Application
```powershell
streamlit run ui/app.py
```

The app will automatically open in your browser at: **http://localhost:8501**

---

## 📝 Example Ticket Creation

### Input:
```
I cannot connect to the company WiFi on my laptop. 
Error says "Network is unreachable". 
I've tried restarting but still getting the same issue. 
I need this fixed urgently as I can't do my work!
```

### Expected Output:
- **Ticket ID**: INC-1001
- **Category**: Network (96% confidence)
- **Priority**: High (91% confidence)
- **Entities**: device=[laptop], error_code=[Network is unreachable]
- **Status**: Open
- **JSON**: Ready to download

---

## 🧪 Testing

### Run Predictions Programmatically
```python
from scripts.predict import create_predictor
from scripts.preprocess import preprocess_text
from scripts.entity_extraction import extract_all_entities

# Initialize predictor
predictor = create_predictor()

# Test input
test_description = "Cannot login to company portal after password reset"

# Preprocess
cleaned = preprocess_text(test_description)
print(f"Cleaned: {cleaned}")

# Predict
results = predictor.predict_all(cleaned)
print(f"Category: {results['category']} ({results['category_confidence']:.2%})")
print(f"Priority: {results['priority']} ({results['priority_confidence']:.2%})")

# Extract entities
entities = extract_all_entities(test_description)
print(f"Entities: {entities}")
```

---

## 📂 File Structure Verification

After setup, you should have:

```
AI-Ticket-Project/
├── models/
│   ├── category_model.pkl          ✓ (created by train_models.py)
│   └── priority_model.pkl          ✓ (created by train_models.py)
├── scripts/
│   ├── __init__.py                 ✓
│   ├── train_models.py             ✓
│   ├── preprocess.py               ✓
│   ├── predict.py                  ✓
│   ├── entity_extraction.py        ✓
│   └── utils.py                    ✓
├── ui/
│   └── app.py                      ✓
├── data/
│   ├── raw/                        (for storing raw data)
│   └── cleaned/                    (for storing processed data)
├── requirements.txt                ✓
├── README.md                       ✓
└── QUICKSTART.md                   ✓ (this file)
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Make sure you're in the project directory and venv is activated |
| "Models not found" | Run `python scripts/train_models.py` again |
| "Port 8501 already in use" | Run `streamlit run ui/app.py --server.port 8502` |
| "Permission denied" | Check file permissions, or run as administrator |
| "NLTK data missing" | Modules auto-download on first run. Be patient! |

---

## 📞 Need Help?

- Check **README.md** for detailed documentation
- Review code comments in individual modules
- Check error messages carefully - they often indicate the solution

---

## 🎯 Next Steps

1. ✅ Run the app with sample data
2. 📊 Test different ticket descriptions
3. 📖 Review the code to understand the ML pipeline
4. 🔧 Customize categories/priorities in `train_models.py`
5. 📈 Integrate with your existing systems

---

**Happy Ticket Processing! 🎫**

Need more info? See **README.md** for comprehensive documentation.
