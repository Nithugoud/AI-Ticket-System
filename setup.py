"""
Setup Script for AI Ticket System
Automates initial setup and configuration
Run: python setup.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    print_header("CHECKING PYTHON VERSION")
    
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    print_info(f"Current Python version: {'.'.join(map(str, current_version))}")
    print_info(f"Required Python version: {'.'.join(map(str, required_version))} or higher")
    
    if current_version >= required_version:
        print_success(f"Python version compatible")
        return True
    else:
        print_error(f"Python version too old. Please upgrade to Python 3.8+")
        return False

def create_directories():
    """Create required directories"""
    print_header("CREATING DIRECTORIES")
    
    dirs = [
        'models',
        'scripts',
        'ui',
        'data/raw',
        'data/cleaned',
        'tickets_output'
    ]
    
    for directory in dirs:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created directory: {directory}")
        else:
            print_info(f"Directory already exists: {directory}")
    
    return True

def check_pip():
    """Check if pip is available"""
    print_header("CHECKING PIP")
    
    try:
        result = subprocess.run(
            ['pip', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"pip is available: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print_error("pip not found. Please ensure pip is installed.")
    return False

def install_dependencies():
    """Install Python dependencies"""
    print_header("INSTALLING DEPENDENCIES")
    
    if not os.path.exists('requirements.txt'):
        print_warning("requirements.txt not found in current directory")
        return False
    
    print_info("Installing packages from requirements.txt...")
    print_info("This may take a few minutes...\n")
    
    try:
        result = subprocess.run(
            ['pip', 'install', '-r', 'requirements.txt'],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print_success("All dependencies installed successfully")
            return True
        else:
            print_error("Failed to install dependencies")
            return False
    
    except Exception as e:
        print_error(f"Error installing dependencies: {str(e)}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print_header("DOWNLOADING NLTK DATA")
    
    try:
        import nltk
        
        required_data = ['punkt', 'stopwords', 'wordnet']
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}' if data == 'punkt' else f'corpora/{data}')
                print_info(f"NLTK data '{data}' already available")
            except LookupError:
                print_info(f"Downloading NLTK data '{data}'...")
                nltk.download(data, quiet=True)
                print_success(f"Downloaded NLTK data '{data}'")
        
        return True
    
    except Exception as e:
        print_error(f"Error downloading NLTK data: {str(e)}")
        print_warning("This is non-critical. You can manually download NLTK data later.")
        return False

def train_models():
    """Train ML models"""
    print_header("TRAINING ML MODELS")
    
    if not os.path.exists('scripts/train_models.py'):
        print_error("train_models.py not found")
        return False
    
    print_info("Training ML models... This may take 1-2 minutes")
    print_info("(Models will be saved to models/ directory)\n")
    
    try:
        result = subprocess.run(
            ['python', 'scripts/train_models.py'],
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print_success("Models trained successfully")
            return True
        else:
            print_error("Failed to train models")
            print_error(result.stderr)
            return False
    
    except Exception as e:
        print_error(f"Error training models: {str(e)}")
        return False

def verify_setup():
    """Verify that all components are set up correctly"""
    print_header("VERIFYING SETUP")
    
    checks = {
        'models/category_model.pkl': 'Category Model',
        'models/priority_model.pkl': 'Priority Model',
        'scripts/preprocess.py': 'Preprocessing Module',
        'scripts/predict.py': 'Prediction Module',
        'scripts/entity_extraction.py': 'Entity Extraction Module',
        'scripts/utils.py': 'Utils Module',
        'ui/app.py': 'Streamlit Application',
        'requirements.txt': 'Requirements File',
        'README.md': 'Documentation',
        'config.py': 'Configuration File'
    }
    
    all_ok = True
    for filepath, description in checks.items():
        if os.path.exists(filepath):
            print_success(f"{description}: {filepath}")
        else:
            print_error(f"{description} not found: {filepath}")
            all_ok = False
    
    return all_ok

def print_next_steps():
    """Print next steps"""
    print_header("SETUP COMPLETE ✓")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.END}\n")
    
    print("1. Activate virtual environment (if created):")
    print(f"   {Colors.CYAN}venv\\Scripts\\Activate  {Colors.GRAY}# Windows{Colors.END}")
    print(f"   {Colors.CYAN}source venv/bin/activate  {Colors.GRAY}# Mac/Linux{Colors.END}\n")
    
    print("2. Run the Streamlit application:")
    print(f"   {Colors.CYAN}streamlit run ui/app.py{Colors.END}\n")
    
    print("3. Open your browser to:")
    print(f"   {Colors.CYAN}http://localhost:8501{Colors.END}\n")
    
    print("4. Try creating your first ticket!\n")
    
    print(f"{Colors.BOLD}Documentation:{Colors.END}")
    print(f"  • {Colors.CYAN}README.md{Colors.END} - Comprehensive guide")
    print(f"  • {Colors.CYAN}QUICKSTART.md{Colors.END} - Quick start guide")
    print(f"  • {Colors.CYAN}SAMPLE_TESTS.py{Colors.END} - Test examples\n")

def main():
    """Main setup function"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("""
    ╔════════════════════════════════════════╗
    ║  🎫 AI TICKET SYSTEM - SETUP WIZARD   ║
    ║                                        ║
    ║  Version 1.0.0                         ║
    ║  Infosys Springboard                   ║
    ╚════════════════════════════════════════╝
    """)
    print(f"{Colors.END}\n")
    
    steps = [
        ("Python Version Check", check_python_version),
        ("Creating Directories", create_directories),
        ("Checking pip", check_pip),
        ("Installing Dependencies", install_dependencies),
        ("Downloading NLTK Data", download_nltk_data),
        ("Training ML Models", train_models),
        ("Verifying Setup", verify_setup),
    ]
    
    completed = []
    skipped = []
    failed = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed.append(step_name)
        except KeyboardInterrupt:
            print_warning("\nSetup interrupted by user")
            sys.exit(1)
        except Exception as e:
            print_error(f"Unexpected error in {step_name}: {str(e)}")
            failed.append(step_name)
        
        completed.append(step_name)
    
    # Print summary
    print_header("SETUP SUMMARY")
    
    print(f"{Colors.GREEN}{Colors.BOLD}Completed Steps:{Colors.END}")
    for step in completed:
        if step not in failed:
            print(f"  ✓ {step}")
    
    if failed:
        print(f"\n{Colors.RED}{Colors.BOLD}Failed Steps:{Colors.END}")
        for step in failed:
            print(f"  ✗ {step}")
        print_warning("Please resolve the above issues and run setup again")
    
    # Final status
    if not failed:
        print_success("\nSetup completed successfully!")
        print_next_steps()
        return 0
    else:
        print_error(f"\nSetup failed with {len(failed)} error(s)")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_warning("\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
        sys.exit(1)
