import subprocess
import sys
import os
import venv
from pathlib import Path

def main():
    # Project root directory
    project_dir = Path(__file__).parent.absolute()
    
    # Create virtual environment
    venv_dir = project_dir / "venv"
    print(f"Creating virtual environment in {venv_dir}...")
    venv.create(venv_dir, with_pip=True)
    
    # Determine the pip path
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:
        pip_path = venv_dir / "bin" / "pip"
    
    # Install requirements
    requirements_file = project_dir / "requirements.txt"
    print(f"Installing requirements from {requirements_file}...")
    subprocess.check_call([str(pip_path), "install", "-r", str(requirements_file)])
    
    # Download NLTK data
    print("Downloading NLTK data...")
    nltk_script = project_dir / "setup_nltk.py"
    
    if sys.platform == "win32":
        python_path = venv_dir / "Scripts" / "python.exe"
    else:
        python_path = venv_dir / "bin" / "python"
    
    subprocess.check_call([str(python_path), str(nltk_script)])
    
    print("\nSetup complete! To activate the virtual environment:")
    if sys.platform == "win32":
        print(f"Run: {venv_dir}\\Scripts\\activate")
    else:
        print(f"Run: source {venv_dir}/bin/activate")
    
    print("\nAfter activation, you can run your Python scripts with the installed packages.")

if __name__ == "__main__":
    main()