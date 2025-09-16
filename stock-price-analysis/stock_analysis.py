import os
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import argparse

def fetch_and_plot(ticker='AAPL', start='2020-01-01', end='2025-01-01', save_path='plots/sample_plot.png'):
    try:
        # Explicitly set auto_adjust=False to remove warning
        data = yf.download(ticker, start=start, end=end, auto_adjust=False)

        # Check if data is empty (failed download or rate-limited)
        if data.empty:
            print(f"⚠️ No data found for {ticker} between {start} and {end}.")
            print("👉 Possible reasons: wrong ticker symbol, no trading data, or rate limit from Yahoo Finance.")
            return

        # Add simple moving averages
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        data['SMA50'] = data['Close'].rolling(window=50).mean()

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(data['Close'], label=f'{ticker} Close', color='blue')
        plt.plot(data['SMA20'], label='SMA 20', color='orange')
        plt.plot(data['SMA50'], label='SMA 50', color='green')
        plt.title(f'{ticker} Closing Price with SMA20 & SMA50')
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        plt.show()

    except Exception as e:
        print(f"❌ Error fetching data for {ticker}: {e}")
        print("👉 Try again later or use a different ticker (MSFT, GOOG, TSLA, etc.).")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Stock Price Analysis with yfinance")
    parser.add_argument('--ticker', type=str, default='AAPL', help='Stock ticker symbol (e.g., AAPL, MSFT)')
    parser.add_argument('--start', type=str, default='2020-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2025-01-01', help='End date (YYYY-MM-DD)')
    parser.add_argument('--output', type=str, default='plots/sample_plot.png', help='Path to save plot image')

    args = parser.parse_args()
    fetch_and_plot(args.ticker, args.start, args.end, args.output)
