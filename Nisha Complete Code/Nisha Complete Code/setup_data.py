"""
Setup Script: Copy CSV files to the app/data directory
Run this script from the main Nisha_Code directory to move data files
"""

import shutil
import glob
import os

def setup_data_files():
    """Copy CSV files from root directory to app/data directory"""
    
    source_dir = "."
    target_dir = "app/data"
    
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Find all crypto and stock CSV files
    crypto_files = glob.glob(os.path.join(source_dir, "crypto_*.csv"))
    stock_files = glob.glob(os.path.join(source_dir, "stock_*.csv"))
    
    all_files = crypto_files + stock_files
    
    if not all_files:
        print("⚠️  No CSV files found in the current directory!")
        print("Please run the data collection script first to generate:")
        print("  - crypto_BTC.csv")
        print("  - crypto_ETH.csv")
        print("  - crypto_BNB.csv")
        print("  - stock_AAPL.csv")
        print("  - stock_MSFT.csv")
        print("  - stock_TSLA.csv")
        return False
    
    print(f"📁 Found {len(all_files)} CSV files")
    print("📋 Copying files to app/data/...")
    
    copied = 0
    for file in all_files:
        filename = os.path.basename(file)
        target_path = os.path.join(target_dir, filename)
        
        try:
            shutil.copy2(file, target_path)
            print(f"  ✅ Copied: {filename}")
            copied += 1
        except Exception as e:
            print(f"  ❌ Error copying {filename}: {e}")
    
    print(f"\n✨ Successfully copied {copied} files to app/data/")
    print("\n🚀 You can now run the Flask app:")
    print("   cd app")
    print("   python app.py")
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("📦 Flask Dashboard Setup Script")
    print("="*60)
    print()
    
    setup_data_files()
