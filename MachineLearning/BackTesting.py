import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 定義各股的權重
weights = {
    '1101.TW': 0.068328,
    '1216.TW': 0.034927,
    '1326.TW': 0.011053,
    '1590.TW': 0.035170,
    '2207.TW': 0.035103,
    '2308.TW': 0.035666,
    '2327.TW': 0.037979,
    '2330.TW': 0.070731,
    '2379.TW': 0.032088,
    '2395.TW': 0.037747,
    '2412.TW': 0.033803,
    '2454.TW': 0.035223,
    '2881.TW': 0.036484,
    '2884.TW': 0.035462,
    '2885.TW': 0.062520,
    '2886.TW': 0.046320,
    '2890.TW': 0.050024,
    '2891.TW': 0.035904,
    '2912.TW': 0.035114,
    '3008.TW': 0.035797,
    '3231.TW': 0.018399,
    '3661.TW': 0.034974,
    '4938.TW': 0.039800,
    '5871.TW': 0.032435,
    '6505.TW': 0.033844,
    '6669.TW': 0.035105
}

# 從yfinance獲取歷史價格數據
tickers = list(weights.keys())
prices = yf.download(tickers, start='2024-06-28', end='2024-09-30')['Adj Close']

# 確保權重和價格數據對應
prices = prices[list(weights.keys())]

# 計算每日回報率
returns = prices.pct_change()

# 確保数据从2024年7月1日开始
returns = returns.loc['2024-07-01':'2024-09-30']

# 計算投资组合的每日回报率
portfolio_returns = returns.dot(pd.Series(weights))

# 将投资组合回报率转换为百分比格式，并保留四位小数
portfolio_returns_percentage = portfolio_returns * 100
portfolio_returns_percentage = portfolio_returns_percentage.apply(lambda x: f'{x:.4f}%')

# 创建数据表并显示
portfolio_returns_percentage = portfolio_returns_percentage.to_frame('Portfolio Returns')
display(portfolio_returns_percentage)

# 計算投资组合的累积回报率
cumulative_returns = (1 + portfolio_returns).cumprod() - 1

# 計算绩效指标
annual_return = portfolio_returns.mean() * 252
annual_volatility = portfolio_returns.std() * np.sqrt(252)
sharpe_ratio = annual_return / annual_volatility

print(f'年化報酬率: {annual_return:.2%}')
print(f'年化波動率: {annual_volatility:.2%}')
print(f'夏普比率: {sharpe_ratio:.2f}')

# 可視化
plt.figure(figsize=(10, 6))
cumulative_returns.plot(title='Portfolio Cumulative Returns')
plt.ylabel('Cumulative Returns')
plt.xlabel('Date')
plt.show()