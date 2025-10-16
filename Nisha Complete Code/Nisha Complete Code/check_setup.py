"""
Pre-flight Check Script
Verifies that all requirements are met before running the Flask app
"""

import os
import sys

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.8+")
        return False

def check_directory_structure():
    """Check if all required directories exist"""
    required_dirs = [
        'app',
        'app/templates',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/data',
        'app/models'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_exist = False
    
    return all_exist

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        'app/app.py',
        'app/data_loader.py',
        'app/model_utils.py',
        'app/visualization.py',
        'app/requirements.txt',
        'app/templates/base.html',
        'app/templates/index.html',
        'app/templates/eda.html',
        'app/templates/forecast.html',
        'app/templates/compare.html'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_exist = False
    
    return all_exist

def check_data_files():
    """Check if CSV data files exist"""
    data_dir = 'app/data'
    expected_files = [
        'crypto_BTC.csv',
        'crypto_ETH.csv',
        'crypto_BNB.csv',
        'stock_AAPL.csv',
        'stock_MSFT.csv',
        'stock_TSLA.csv'
    ]
    
    found = 0
    for filename in expected_files:
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            print(f"✅ Data file exists: {filename}")
            found += 1
        else:
            print(f"⚠️  Missing data file: {filename}")
    
    if found == 0:
        print("\n❌ No data files found!")
        print("   Run: python setup_data.py")
        return False
    elif found < len(expected_files):
        print(f"\n⚠️  Only {found}/{len(expected_files)} data files found")
        print("   Some assets won't be available")
        return True
    else:
        print(f"\n✅ All {found} data files found!")
        return True

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'plotly',
        'statsmodels',
        'sklearn',
    ]
    
    optional_packages = [
        'pmdarima',
        'tensorflow'
    ]
    
    print("\nChecking required packages...")
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            all_installed = False
    
    print("\nChecking optional packages...")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"⚠️  {package} NOT installed (models may use fallback)")
    
    if not all_installed:
        print("\n❌ Missing required packages!")
        print("   Run: cd app && pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all checks"""
    print("="*70)
    print("🔍 PRE-FLIGHT CHECK - Flask Financial Forecasting Dashboard")
    print("="*70)
    print()
    
    checks = {
        "Python Version": check_python_version(),
        "Directory Structure": check_directory_structure(),
        "Required Files": check_required_files(),
        "Data Files": check_data_files(),
        "Dependencies": check_dependencies()
    }
    
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    
    all_passed = True
    for check_name, passed in checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to run the dashboard.")
        print("\n▶️  To start the dashboard, run:")
        print("   cd app")
        print("   python app.py")
        print("\n🌐 Then open: http://localhost:5000")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before running.")
        print("\n📚 Common fixes:")
        print("   1. Install dependencies: cd app && pip install -r requirements.txt")
        print("   2. Copy data files: python setup_data.py")
        print("   3. Check file structure matches documentation")
    
    print()
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
