import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 定義各股的權重
# 有正規化smart_pick
# weights = {
#     '1101.TW': 0.0673,
#     '1216.TW': 0.0349,
#     '1301.TW': 0.0000,
#     '1303.TW': 0.0000,
#     '1326.TW': 0.0114,
#     '1590.TW': 0.0352,
#     '2002.TW': 0.0000,
#     '2207.TW': 0.0351,
#     '2301.TW': 0.0000,
#     '2303.TW': 0.0000,
#     '2308.TW': 0.0356,
#     '2317.TW': 0.0000,
#     '2327.TW': 0.0380,
#     '2330.TW': 0.0715,
#     '2345.TW': 0.0000,
#     '2357.TW': 0.0000,
#     '2379.TW': 0.0312,
#     '2382.TW': 0.0000,
#     '2395.TW': 0.0375,
#     '2408.TW': 0.0000,
#     '2412.TW': 0.0339,
#     '2454.TW': 0.0352,
#     '2603.TW': 0.0000,
#     '2880.TW': 0.0000,
#     '2881.TW': 0.0365,
#     '2882.TW': 0.0000,
#     '2883.TW': 0.0000,
#     '2884.TW': 0.0354,
#     '2885.TW': 0.0625,
#     '2886.TW': 0.0459,
#     '2887.TW': 0.0000,
#     '2890.TW': 0.0499,
#     '2891.TW': 0.0358,
#     '2892.TW': 0.0000,
#     '2912.TW': 0.0351,
#     '3008.TW': 0.0358,
#     '3017.TW': 0.0000,
#     '3034.TW': 0.0000,
#     '3037.TW': 0.0000,
#     '3045.TW': 0.0000,
#     '3231.TW': 0.0208,
#     '3661.TW': 0.0350,
#     '3711.TW': 0.0000,
#     '4904.TW': 0.0000,
#     '4938.TW': 0.0393,
#     '5871.TW': 0.0325,
#     '5876.TW': 0.0000,
#     '5880.TW': 0.0000,
#     '6505.TW': 0.0338,
#     '6669.TW': 0.0349
# }
# 無正規化
weights = {
    '1101.TW': 0.0683,
    '1216.TW': 0.0350,
    '1301.TW': 0.0000,
    '1303.TW': 0.0000,
    '1326.TW': 0.0111,
    '1590.TW': 0.0352,
    '2002.TW': 0.0000,
    '2207.TW': 0.0351,
    '2301.TW': 0.0000,
    '2303.TW': 0.0000,
    '2308.TW': 0.0357,
    '2317.TW': 0.0000,
    '2327.TW': 0.0380,
    '2330.TW': 0.0707,
    '2345.TW': 0.0000,
    '2357.TW': 0.0000,
    '2379.TW': 0.0321,
    '2382.TW': 0.0000,
    '2395.TW': 0.0377,
    '2408.TW': 0.0000,
    '2412.TW': 0.0338,
    '2454.TW': 0.0352,
    '2603.TW': 0.0000,
    '2880.TW': 0.0000,
    '2881.TW': 0.0365,
    '2882.TW': 0.0000,
    '2883.TW': 0.0000,
    '2884.TW': 0.0355,
    '2885.TW': 0.0625,
    '2886.TW': 0.0463,
    '2887.TW': 0.0000,
    '2890.TW': 0.0500,
    '2891.TW': 0.0359,
    '2892.TW': 0.0000,
    '2912.TW': 0.0351,
    '3008.TW': 0.0358,
    '3017.TW': 0.0000,
    '3034.TW': 0.0000,
    '3037.TW': 0.0000,
    '3045.TW': 0.0000,
    '3231.TW': 0.0184,
    '3661.TW': 0.0350,
    '3711.TW': 0.0000,
    '4904.TW': 0.0000,
    '4938.TW': 0.0398,
    '5871.TW': 0.0324,
    '5876.TW': 0.0000,
    '5880.TW': 0.0000,
    '6505.TW': 0.0338,
    '6669.TW': 0.0351
}

# 從 yfinance 獲取歷史價格數據
tickers = list(weights.keys())
prices = yf.download(tickers, start='2024-06-28', end='2024-10-01')['Adj Close']

# 確保權重和價格數據對應
prices = prices[list(weights.keys())]

# 計算每日回報率
returns = prices.pct_change()

# 確保數據從 2024 年 7 月 1 日開始
returns = returns.loc['2024-07-01':'2024-10-01']

# 計算投資組合的每日回報率
portfolio_returns = returns.dot(pd.Series(weights))

# 將投資組合回報率轉換為百分比格式，並保留四位小數
portfolio_returns_percentage = portfolio_returns * 100
portfolio_returns_percentage = portfolio_returns_percentage.apply(lambda x: f'{x:.4f}%')

# 建立數據表並顯示
portfolio_returns_percentage = portfolio_returns_percentage.to_frame('Portfolio Returns')
display(portfolio_returns_percentage)

# 計算投資組合的累積回報率
cumulative_returns = (1 + portfolio_returns).cumprod() - 1

# 計算績效指標
annual_return = portfolio_returns.mean() * 252
annual_volatility = portfolio_returns.std() * np.sqrt(252)
sharpe_ratio = annual_return / annual_volatility

print(f'年化報酬率: {annual_return:.2%}')
print(f'年化波動率: {annual_volatility:.2%}')
print(f'夏普比率: {sharpe_ratio:.2f}')

# 視覺化
plt.figure(figsize=(10, 6))
cumulative_returns.plot(title='Portfolio Cumulative Returns')
plt.ylabel('Cumulative Returns')
plt.xlabel('Date')
plt.show()
