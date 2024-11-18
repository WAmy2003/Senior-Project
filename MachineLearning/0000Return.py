import yfinance as yf
import pandas as pd

# 抓取台灣加權指數 (^TWII) 的數據
taiex = yf.download("^TWII", start="2024-07-01", end="2024-09-30")

# 確保只有 Close 欄位
close_prices = taiex['Close']

# 計算日報酬率
daily_returns = close_prices.pct_change()

annual_return = close_prices.mean() * 252

# 印出數據
print(daily_returns)

print(f': {annual_return:.2f}')