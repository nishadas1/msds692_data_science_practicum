"""
Flask Financial Forecasting Dashboard
Week 7: Interactive Dashboard / Visualization Development

Run this app with: python app.py
Then visit: http://localhost:5000

Author: Nisha
Project: Crypto vs Stocks Financial Forecasting
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import sys
import io
import json

# Import custom modules
from data_loader import DataLoader
from visualization import Visualizer
from model_utils import ModelTrainer

# ---------------------------------------------------
# FLASK APP CONFIGURATION
# ---------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize components
data_loader = DataLoader(data_dir='data')
visualizer = Visualizer()
model_trainer = ModelTrainer()

# Global variables to store loaded data
crypto_dfs = {}
stock_dfs = {}
all_data = {}

# ---------------------------------------------------
# DATA LOADING ON STARTUP
# ---------------------------------------------------
def load_initial_data():
    """Load all data when the app starts"""
    global crypto_dfs, stock_dfs, all_data
    
    print("Loading data files...")
    crypto_dfs, stock_dfs = data_loader.load_all_data()
    all_data = {**crypto_dfs, **stock_dfs}
    
    if not all_data:
        print("WARNING: No data files found in /data directory!")
        print("Please ensure crypto_*.csv and stock_*.csv files are in the /data folder")
    else:
        print(f"Loaded {len(crypto_dfs)} crypto assets and {len(stock_dfs)} stock assets")
        print(f"Assets: {list(all_data.keys())}")

# Load data on startup
load_initial_data()

# ---------------------------------------------------
# ROUTE: HOME PAGE
# ---------------------------------------------------
@app.route('/')
def index():
    """Dashboard home page with summary statistics"""
    # Get summary statistics
    total_cryptos = len(crypto_dfs)
    total_stocks = len(stock_dfs)
    
    min_date, max_date = data_loader.get_date_range()
    date_range = f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}" if min_date else "N/A"
    
    # Calculate some summary stats
    crypto_names = list(crypto_dfs.keys())
    stock_names = list(stock_dfs.keys())
    
    # Get latest prices
    latest_prices = {}
    for name, df in all_data.items():
        if not df.empty:
            latest_prices[name] = {
                'price': round(df['Close'].iloc[-1], 2),
                'change': round(df['Daily Return'].iloc[-1] * 100, 2) if pd.notna(df['Daily Return'].iloc[-1]) else 0
            }
    
    return render_template(
        'index.html',
        total_cryptos=total_cryptos,
        total_stocks=total_stocks,
        date_range=date_range,
        crypto_names=crypto_names,
        stock_names=stock_names,
        latest_prices=latest_prices
    )

# ---------------------------------------------------
# ROUTE: EDA (Exploratory Data Analysis)
# ---------------------------------------------------
@app.route('/eda')
def eda():
    """EDA page with visualizations"""
    selected_asset = request.args.get('asset', 'all')
    
    if selected_asset == 'all':
        # Show combined plots for all assets
        plot_closing = visualizer.plot_closing_prices(crypto_dfs, stock_dfs)
        plot_returns = visualizer.plot_daily_returns(crypto_dfs, stock_dfs)
        plot_vol = visualizer.plot_volatility(crypto_dfs, stock_dfs)
        plot_corr = visualizer.plot_correlation_heatmap(crypto_dfs, stock_dfs)
        plot_detail = None
    else:
        # Show detailed view for selected asset
        df, asset_type = data_loader.get_data(selected_asset)
        if df is not None:
            plot_closing = visualizer.plot_closing_prices(crypto_dfs, stock_dfs)
            plot_returns = visualizer.plot_daily_returns(crypto_dfs, stock_dfs)
            plot_vol = visualizer.plot_volatility(crypto_dfs, stock_dfs)
            plot_corr = visualizer.plot_correlation_heatmap(crypto_dfs, stock_dfs)
            plot_detail = visualizer.plot_asset_details(df, selected_asset, asset_type)
        else:
            plot_closing = plot_returns = plot_vol = plot_corr = plot_detail = None
    
    asset_list = ['all'] + list(all_data.keys())
    
    return render_template(
        'eda.html',
        plot_closing=plot_closing,
        plot_returns=plot_returns,
        plot_volatility=plot_vol,
        plot_correlation=plot_corr,
        plot_detail=plot_detail,
        asset_list=asset_list,
        selected_asset=selected_asset
    )

# ---------------------------------------------------
# ROUTE: FORECAST
# ---------------------------------------------------
@app.route('/forecast')
def forecast():
    """Forecast page - ARIMA vs LSTM predictions"""
    asset_list = list(all_data.keys())
    selected_asset = request.args.get('asset', asset_list[0] if asset_list else None)
    
    if not selected_asset or selected_asset not in all_data:
        return render_template(
            'forecast.html',
            asset_list=asset_list,
            selected_asset=None,
            plot_forecast=None,
            metrics_table=None,
            error="Please select a valid asset"
        )
    
    # Get data for selected asset
    df = all_data[selected_asset]
    
    # Train models and get forecasts
    results = model_trainer.train_and_forecast(df, selected_asset, forecast_steps=30)
    
    # Create forecast plot
    plot_forecast = visualizer.plot_forecast_comparison(
        df,
        results['arima_forecast'],
        results['lstm_forecast'],
        selected_asset
    )
    
    # Create metrics table
    metrics_data = {
        'Model': ['ARIMA', 'LSTM'],
        'MAE': [results['arima_metrics']['MAE'], results['lstm_metrics']['MAE']],
        'RMSE': [results['arima_metrics']['RMSE'], results['lstm_metrics']['RMSE']],
        'MAPE': [results['arima_metrics']['MAPE'], results['lstm_metrics']['MAPE']]
    }
    metrics_df = pd.DataFrame(metrics_data)
    
    # Store forecast data for download
    forecast_data = {
        'asset': selected_asset,
        'arima_forecast': results['arima_forecast'].tolist(),
        'lstm_forecast': results['lstm_forecast'].tolist(),
        'arima_metrics': results['arima_metrics'],
        'lstm_metrics': results['lstm_metrics']
    }
    
    return render_template(
        'forecast.html',
        asset_list=asset_list,
        selected_asset=selected_asset,
        plot_forecast=plot_forecast,
        metrics_table=metrics_df.to_html(classes='table table-striped table-hover', index=False),
        forecast_data=json.dumps(forecast_data)
    )

# ---------------------------------------------------
# ROUTE: COMPARISON
# ---------------------------------------------------
@app.route('/compare')
def compare():
    """Comparative analysis - ARIMA vs LSTM across all assets"""
    if not all_data:
        return render_template(
            'compare.html',
            plot_comparison=None,
            metrics_table=None,
            error="No data available for comparison"
        )
    
    # Train models for all assets and get metrics
    print("Training models for all assets... This may take a few minutes.")
    metrics_df = model_trainer.batch_train_all_assets(all_data)
    
    # Determine best model per asset
    metrics_df['Best_Model'] = metrics_df.apply(
        lambda row: 'ARIMA' if row['ARIMA_MAE'] < row['LSTM_MAE'] else 'LSTM',
        axis=1
    )
    
    # Create comparison plot
    plot_comparison = visualizer.plot_model_comparison(metrics_df)
    
    # Calculate summary statistics
    arima_wins = (metrics_df['Best_Model'] == 'ARIMA').sum()
    lstm_wins = (metrics_df['Best_Model'] == 'LSTM').sum()
    
    summary = {
        'arima_wins': arima_wins,
        'lstm_wins': lstm_wins,
        'total_assets': len(metrics_df),
        'avg_arima_mae': round(metrics_df['ARIMA_MAE'].mean(), 2),
        'avg_lstm_mae': round(metrics_df['LSTM_MAE'].mean(), 2)
    }
    
    return render_template(
        'compare.html',
        plot_comparison=plot_comparison,
        metrics_table=metrics_df.to_html(classes='table table-striped table-hover', index=False),
        summary=summary
    )

# ---------------------------------------------------
# ROUTE: DOWNLOAD FORECAST DATA
# ---------------------------------------------------
@app.route('/download_forecast')
def download_forecast():
    """Download forecast data as CSV"""
    asset = request.args.get('asset')
    
    if not asset or asset not in all_data:
        return jsonify({'error': 'Invalid asset'}), 400
    
    # Get forecast data
    df = all_data[asset]
    results = model_trainer.train_and_forecast(df, asset, forecast_steps=30)
    
    # Create forecast DataFrame
    last_date = df['Date'].iloc[-1]
    forecast_dates = pd.date_range(start=last_date, periods=31, freq='D')[1:]
    
    forecast_df = pd.DataFrame({
        'Date': forecast_dates,
        'ARIMA_Forecast': results['arima_forecast'],
        'LSTM_Forecast': results['lstm_forecast']
    })
    
    # Convert to CSV
    output = io.StringIO()
    forecast_df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'{asset}_forecast.csv'
    )

# ---------------------------------------------------
# ROUTE: API - Get Asset Data (JSON)
# ---------------------------------------------------
@app.route('/api/asset/<asset_name>')
def api_asset_data(asset_name):
    """API endpoint to get asset data as JSON"""
    if asset_name not in all_data:
        return jsonify({'error': 'Asset not found'}), 404
    
    df = all_data[asset_name]
    
    # Convert to JSON-friendly format
    data = {
        'asset': asset_name,
        'dates': df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'close': df['Close'].tolist(),
        'volume': df['Volume'].tolist(),
        'daily_return': df['Daily Return'].fillna(0).tolist(),
        'volatility': df['Volatility_30D'].fillna(0).tolist()
    }
    
    return jsonify(data)

# ---------------------------------------------------
# FAVICON ROUTE
# ---------------------------------------------------
@app.route('/favicon.ico')
def favicon():
    """Return empty response for favicon to prevent 404 errors"""
    return '', 204

# ---------------------------------------------------
# ERROR HANDLERS
# ---------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# ---------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------
if __name__ == '__main__':
    # Check if data directory exists
    if not os.path.exists('data'):
        print("\n" + "="*60)
        print("WARNING: 'data' directory not found!")
        print("Please create a 'data' folder and add your CSV files:")
        print("  - crypto_BTC.csv")
        print("  - crypto_ETH.csv")
        print("  - crypto_BNB.csv")
        print("  - stock_AAPL.csv")
        print("  - stock_MSFT.csv")
        print("  - stock_TSLA.csv")
        print("="*60 + "\n")
    
    print("\n" + "="*60)
    print("🚀 Starting Flask Financial Forecasting Dashboard")
    print("="*60)
    print("\n📊 Dashboard URL: http://localhost:5000")
    print("\n📝 Available Routes:")
    print("  - Home:       http://localhost:5000/")
    print("  - EDA:        http://localhost:5000/eda")
    print("  - Forecast:   http://localhost:5000/forecast")
    print("  - Compare:    http://localhost:5000/compare")
    print("\n⚡ Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
