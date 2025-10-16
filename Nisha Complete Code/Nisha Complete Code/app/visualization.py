"""
Visualization Module
Creates interactive plots using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        self.colors = {
            'crypto': ['#f7931a', '#627eea', '#f0b90b'],
            'stock': ['#a6cee3', '#1f78b4', '#b2df8a']
        }
    
    def plot_closing_prices(self, crypto_dfs, stock_dfs):
        """Create closing price trend plot"""
        fig = go.Figure()
        
        # Add crypto traces
        for i, (name, df) in enumerate(crypto_dfs.items()):
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Close'],
                mode='lines',
                name=f'{name} (Crypto)',
                line=dict(width=2)
            ))
        
        # Add stock traces
        for i, (name, df) in enumerate(stock_dfs.items()):
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Close'],
                mode='lines',
                name=f'{name} (Stock)',
                line=dict(width=2, dash='dash')
            ))
        
        fig.update_layout(
            title='Closing Price Trends (Crypto vs Stocks)',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def plot_daily_returns(self, crypto_dfs, stock_dfs):
        """Create daily returns distribution plot"""
        fig = go.Figure()
        
        # Add crypto distributions
        for name, df in crypto_dfs.items():
            returns = df['Daily Return'].dropna()
            fig.add_trace(go.Histogram(
                x=returns,
                name=f'{name} (Crypto)',
                opacity=0.6,
                nbinsx=50
            ))
        
        # Add stock distributions
        for name, df in stock_dfs.items():
            returns = df['Daily Return'].dropna()
            fig.add_trace(go.Histogram(
                x=returns,
                name=f'{name} (Stock)',
                opacity=0.6,
                nbinsx=50
            ))
        
        fig.update_layout(
            title='Distribution of Daily Returns',
            xaxis_title='Daily Return',
            yaxis_title='Frequency',
            barmode='overlay',
            template='plotly_white',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def plot_volatility(self, crypto_dfs, stock_dfs):
        """Create 30-day rolling volatility plot"""
        fig = go.Figure()
        
        # Add crypto volatility
        for name, df in crypto_dfs.items():
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Volatility_30D'],
                mode='lines',
                name=f'{name} Volatility (Crypto)',
                line=dict(width=2)
            ))
        
        # Add stock volatility
        for name, df in stock_dfs.items():
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=df['Volatility_30D'],
                mode='lines',
                name=f'{name} Volatility (Stock)',
                line=dict(width=2, dash='dash')
            ))
        
        fig.update_layout(
            title='30-Day Rolling Volatility (Crypto vs Stocks)',
            xaxis_title='Date',
            yaxis_title='Volatility (Standard Deviation)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def plot_correlation_heatmap(self, crypto_dfs, stock_dfs):
        """Create correlation heatmap"""
        # Combine all dataframes
        cleaned_dfs = []
        for name, df in {**crypto_dfs, **stock_dfs}.items():
            df_unique = df.drop_duplicates(subset="Date")
            df_unique = df_unique.set_index("Date")[["Close"]].rename(columns={"Close": name})
            cleaned_dfs.append(df_unique)
        
        combined_df = pd.concat(cleaned_dfs, axis=1)
        combined_df = combined_df.ffill().bfill()
        
        # Calculate correlation based on daily returns
        corr_matrix = combined_df.pct_change().corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Correlation of Daily Returns (Crypto vs Stocks)',
            template='plotly_white',
            height=600,
            xaxis={'side': 'bottom'}
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def plot_asset_details(self, df, asset_name, asset_type):
        """Create detailed view for a single asset"""
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                f'{asset_name} Price & Moving Average',
                f'{asset_name} Daily Returns',
                f'{asset_name} Volume'
            ),
            vertical_spacing=0.1,
            row_heights=[0.4, 0.3, 0.3]
        )
        
        # Price and MA
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', line=dict(color='blue', width=2)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Date'], y=df['MA_50'], name='50-day MA', line=dict(color='orange', width=1)),
            row=1, col=1
        )
        
        # Daily Returns
        fig.add_trace(
            go.Bar(x=df['Date'], y=df['Daily Return'], name='Daily Return', marker_color='green'),
            row=2, col=1
        )
        
        # Volume
        fig.add_trace(
            go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker_color='purple'),
            row=3, col=1
        )
        
        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
        fig.update_yaxes(title_text="Return", row=2, col=1)
        fig.update_yaxes(title_text="Volume", row=3, col=1)
        
        fig.update_layout(
            height=900,
            showlegend=True,
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def plot_forecast_comparison(self, df, arima_pred, lstm_pred, asset_name):
        """Create forecast comparison plot"""
        fig = go.Figure()
        
        # Historical data (last 180 days)
        historical = df.tail(180)
        fig.add_trace(go.Scatter(
            x=historical['Date'],
            y=historical['Close'],
            mode='lines',
            name='Historical Price',
            line=dict(color='blue', width=2)
        ))
        
        # ARIMA forecast
        last_date = df['Date'].iloc[-1]
        forecast_dates = pd.date_range(start=last_date, periods=31, freq='D')[1:]
        
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=arima_pred,
            mode='lines',
            name='ARIMA Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        # LSTM forecast
        fig.add_trace(go.Scatter(
            x=forecast_dates,
            y=lstm_pred,
            mode='lines',
            name='LSTM Forecast',
            line=dict(color='green', width=2, dash='dot')
        ))
        
        fig.update_layout(
            title=f'{asset_name} - 30-Day Price Forecast (ARIMA vs LSTM)',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def plot_model_comparison(self, metrics_df):
        """Create bar chart comparing ARIMA vs LSTM performance"""
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('MAE Comparison', 'RMSE Comparison', 'MAPE Comparison')
        )
        
        assets = metrics_df['Asset'].tolist()
        
        # MAE
        fig.add_trace(
            go.Bar(name='ARIMA', x=assets, y=metrics_df['ARIMA_MAE'], marker_color='red'),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name='LSTM', x=assets, y=metrics_df['LSTM_MAE'], marker_color='green'),
            row=1, col=1
        )
        
        # RMSE
        fig.add_trace(
            go.Bar(name='ARIMA', x=assets, y=metrics_df['ARIMA_RMSE'], marker_color='red', showlegend=False),
            row=1, col=2
        )
        fig.add_trace(
            go.Bar(name='LSTM', x=assets, y=metrics_df['LSTM_RMSE'], marker_color='green', showlegend=False),
            row=1, col=2
        )
        
        # MAPE
        fig.add_trace(
            go.Bar(name='ARIMA', x=assets, y=metrics_df['ARIMA_MAPE'], marker_color='red', showlegend=False),
            row=1, col=3
        )
        fig.add_trace(
            go.Bar(name='LSTM', x=assets, y=metrics_df['LSTM_MAPE'], marker_color='green', showlegend=False),
            row=1, col=3
        )
        
        fig.update_layout(
            title_text='Model Performance Comparison (Lower is Better)',
            template='plotly_white',
            height=500,
            showlegend=True,
            barmode='group'
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
