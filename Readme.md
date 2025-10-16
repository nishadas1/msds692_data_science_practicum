# 📈 Financial Forecasting Dashboard

A comprehensive web-based financial forecasting application that compares cryptocurrency and stock market performance using advanced time series analysis and machine learning models.

## 🌟 Features

- **Interactive Dashboard**: Real-time visualization of financial data with responsive web interface
- **Multi-Asset Support**: Compare cryptocurrencies (BTC, ETH, BNB) and stocks (AAPL, MSFT, TSLA)
- **Exploratory Data Analysis (EDA)**: Comprehensive statistical analysis and visualizations
- **Time Series Forecasting**: Advanced prediction models including:
  - ARIMA (AutoRegressive Integrated Moving Average)
  - LSTM (Long Short-Term Memory Neural Networks)
- **Comparative Analysis**: Side-by-side comparison of different assets
- **Performance Metrics**: Detailed model evaluation with MAE, RMSE, and MAPE
- **Interactive Visualizations**: Built with Plotly for rich, interactive charts

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "Nisha Complete Code"
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
cd app
pip install -r requirements.txt
```

### Step 4: Set Up Data

```bash
# Run from the root directory
python setup_data.py
```

This will copy all CSV files to the `app/data/` directory.

### Step 5: Verify Setup

```bash
python check_setup.py
```

This script checks that all required dependencies and data files are properly installed.

## ⚡ Quick Start

1. **Navigate to the app directory**:
   ```bash
   cd app
   ```

2. **Run the Flask application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and visit:
   ```
   http://localhost:5000
   ```

4. **Explore the dashboard**:
   - View summary statistics on the home page
   - Navigate to EDA for exploratory data analysis
   - Generate forecasts with ARIMA or LSTM models
   - Compare different assets side-by-side

## 📁 Project Structure

```
Nisha Complete Code/
├── app/
│   ├── app.py                  # Main Flask application
│   ├── data_loader.py          # Data loading and preprocessing
│   ├── model_utils.py          # ARIMA and LSTM model implementations
│   ├── visualization.py        # Plotly visualization functions
│   ├── requirements.txt        # Python dependencies
│   │
│   ├── data/                   # CSV data files
│   │   ├── crypto_BTC.csv
│   │   ├── crypto_ETH.csv
│   │   ├── crypto_BNB.csv
│   │   ├── stock_AAPL.csv
│   │   ├── stock_MSFT.csv
│   │   └── stock_TSLA.csv
│   │
│   ├── models/                 # Saved model files
│   │
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   │   └── style.css      # Custom styles
│   │   ├── js/
│   │   │   └── main.js        # Client-side JavaScript
│   │   └── images/            # Image assets
│   │
│   └── templates/              # HTML templates
│       ├── base.html          # Base template
│       ├── index.html         # Home page
│       ├── eda.html           # EDA page
│       ├── forecast.html      # Forecasting page
│       ├── compare.html       # Comparison page
│       └── 404.html           # Error page
│
├── setup_data.py               # Data setup script
├── check_setup.py              # Installation verification script
└── README.md                   # This file
```

## 💻 Usage

### Home Dashboard

The main dashboard displays:
- Total number of cryptocurrencies and stocks tracked
- Date range of available data
- Latest prices and daily changes
- Quick access to all features

### Exploratory Data Analysis (EDA)

Access detailed analysis including:
- Time series plots
- Price distribution histograms
- Correlation matrices
- Volatility analysis
- Moving averages
- Volume analysis

**Example**:
1. Navigate to `/eda`
2. Select an asset from the dropdown
3. Choose analysis type
4. View interactive visualizations

### Forecasting

Generate predictions using ARIMA or LSTM models:

1. Navigate to `/forecast`
2. Select an asset (crypto or stock)
3. Choose model type (ARIMA or LSTM)
4. Set forecast horizon (number of days)
5. Click "Generate Forecast"
6. View predictions with confidence intervals and model metrics

### Comparison

Compare multiple assets:
1. Navigate to `/compare`
2. Select assets to compare
3. Choose comparison metrics
4. Analyze side-by-side performance

## 📊 Data

### Data Sources

- **Cryptocurrencies**: Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB)
- **Stocks**: Apple (AAPL), Microsoft (MSFT), Tesla (TSLA)

### Data Format

Each CSV file contains the following columns:
- `Date`: Trading date
- `Open`: Opening price
- `High`: Highest price
- `Low`: Lowest price
- `Close`: Closing price
- `Volume`: Trading volume
- `Daily Return`: Calculated daily return percentage

### Data Collection

Data can be collected using `yfinance` library. The application expects CSV files in the `app/data/` directory with the naming convention:
- `crypto_<SYMBOL>.csv` for cryptocurrencies
- `stock_<SYMBOL>.csv` for stocks

## 🤖 Models

### ARIMA (AutoRegressive Integrated Moving Average)

- **Use Case**: Linear time series with trend and seasonality
- **Features**:
  - Auto-parameter selection using `pmdarima`
  - Confidence intervals
  - Fast training time
  - Good for short to medium-term forecasts

### LSTM (Long Short-Term Memory)

- **Use Case**: Complex non-linear patterns in time series
- **Features**:
  - Deep learning architecture
  - Captures long-term dependencies
  - Better for volatile assets
  - Requires more training data

### Model Metrics

Both models provide:
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **MAPE** (Mean Absolute Percentage Error)

## 🔌 API Endpoints

### Main Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home dashboard |
| `/eda` | GET | Exploratory data analysis page |
| `/forecast` | GET | Forecasting interface |
| `/compare` | GET | Asset comparison page |

### API Routes

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/data/<asset>` | GET | Get raw data for an asset |
| `/api/forecast` | POST | Generate forecast (ARIMA/LSTM) |
| `/api/compare` | POST | Compare multiple assets |
| `/api/eda/<asset>` | GET | Get EDA statistics |

### Example API Request

```python
import requests

# Generate forecast
response = requests.post('http://localhost:5000/api/forecast', json={
    'asset': 'BTC',
    'model': 'LSTM',
    'forecast_days': 30
})

forecast_data = response.json()
```

## ⚙️ Configuration

### Flask Configuration

Edit `app.py` to modify:
- `SECRET_KEY`: Application secret key
- `DEBUG`: Debug mode (default: True)
- `HOST`: Server host (default: localhost)
- `PORT`: Server port (default: 5000)

### Model Parameters

Edit `model_utils.py` to adjust:
- ARIMA parameters (p, d, q)
- LSTM architecture (layers, units, dropout)
- Training epochs and batch size

## 🛠️ Development

### Adding New Assets

1. Add CSV file to `app/data/` with proper naming convention
2. Restart the application
3. Asset will be automatically detected and loaded

### Adding New Models

1. Create model class in `model_utils.py`
2. Implement `train()` and `predict()` methods
3. Add model option in `forecast.html`
4. Update forecast route in `app.py`

### Running Tests

```bash
# Add tests to a tests/ directory
pytest tests/
```

## 📝 Dependencies

Key dependencies include:
- **Flask 3.0.0**: Web framework
- **pandas 2.1.4**: Data manipulation
- **numpy 1.26.2**: Numerical computing
- **matplotlib 3.8.2**: Static plotting
- **plotly 5.18.0**: Interactive visualizations
- **statsmodels 0.14.1**: ARIMA models
- **tensorflow 2.17.0**: LSTM neural networks
- **scikit-learn 1.3.2**: Machine learning utilities
- **yfinance 0.2.33**: Financial data retrieval

See `app/requirements.txt` for complete list.

## 🐛 Troubleshooting

### Common Issues

**Issue**: Module not found error
```bash
# Solution: Ensure virtual environment is activated and dependencies are installed
pip install -r app/requirements.txt
```

**Issue**: No data files found
```bash
# Solution: Run the setup script
python setup_data.py
```

**Issue**: Port already in use
```bash
# Solution: Change port in app.py or kill process using port 5000
lsof -ti:5000 | xargs kill -9  # macOS/Linux
```

**Issue**: TensorFlow/LSTM errors
```bash
# Solution: Ensure TensorFlow is properly installed
pip install --upgrade tensorflow
```

## 🙏 Acknowledgments

- Financial data provided by Yahoo Finance
- Built with Flask and TensorFlow
- Visualization powered by Plotly
- ARIMA implementation using statsmodels and pmdarima

