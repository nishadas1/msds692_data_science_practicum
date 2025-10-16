"""
Data Loading and Processing Module
Handles loading, cleaning, and feature engineering for crypto and stock data
"""

import pandas as pd
import glob
import os

class DataLoader:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.crypto_dfs = {}
        self.stock_dfs = {}
        
    def load_all_data(self):
        """Load all crypto and stock CSV files"""
        # Load crypto data
        crypto_files = glob.glob(os.path.join(self.data_dir, "crypto_*.csv"))
        for file in crypto_files:
            name = os.path.basename(file).split("_")[1].split(".")[0]
            df = pd.read_csv(file)
            self.crypto_dfs[name] = self.clean_data(df)
        
        # Load stock data
        stock_files = glob.glob(os.path.join(self.data_dir, "stock_*.csv"))
        for file in stock_files:
            name = os.path.basename(file).split("_")[1].split(".")[0]
            df = pd.read_csv(file)
            self.stock_dfs[name] = self.clean_data(df)
        
        return self.crypto_dfs, self.stock_dfs
    
    def clean_data(self, df):
        """Clean and add features to dataframe"""
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Convert Date column to datetime
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Ensure numeric columns are numeric
        numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Sort by Date
        df = df.sort_values("Date")
        
        # Fill missing values
        df = df.ffill().bfill()
        
        # Compute Daily Return
        if "Close" in df.columns:
            df["Daily Return"] = df["Close"].pct_change()
        
        # Compute 30-day Rolling Volatility
        if "Daily Return" in df.columns:
            df["Volatility_30D"] = df["Daily Return"].rolling(window=30).std()
        
        # Compute 50-day Moving Average
        if "Close" in df.columns:
            df["MA_50"] = df["Close"].rolling(window=50).mean()
        
        return df
    
    def get_asset_list(self, asset_type="all"):
        """Get list of available assets"""
        if asset_type == "crypto":
            return list(self.crypto_dfs.keys())
        elif asset_type == "stock":
            return list(self.stock_dfs.keys())
        else:
            return list(self.crypto_dfs.keys()) + list(self.stock_dfs.keys())
    
    def get_data(self, asset_name):
        """Get data for a specific asset"""
        if asset_name in self.crypto_dfs:
            return self.crypto_dfs[asset_name], "crypto"
        elif asset_name in self.stock_dfs:
            return self.stock_dfs[asset_name], "stock"
        else:
            return None, None
    
    def get_all_data(self):
        """Get all data as a combined dictionary"""
        return {**self.crypto_dfs, **self.stock_dfs}
    
    def get_date_range(self):
        """Get the date range of the data"""
        all_dfs = list(self.crypto_dfs.values()) + list(self.stock_dfs.values())
        if not all_dfs:
            return None, None
        
        min_date = min(df["Date"].min() for df in all_dfs)
        max_date = max(df["Date"].max() for df in all_dfs)
        return min_date, max_date
