import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 定義各股的權重
# weights = {
#     '1101.TW': 0.068328,
#     '1216.TW': 0.034927,
#     '1326.TW': 0.011053,
#     '1590.TW': 0.035170,
#     '2207.TW': 0.035103,
#     '2308.TW': 0.035666,
#     '2327.TW': 0.037979,
#     '2330.TW': 0.070731,
#     '2379.TW': 0.032088,
#     '2395.TW': 0.037747,
#     '2412.TW': 0.033803,
#     '2454.TW': 0.035223,
#     '2881.TW': 0.036484,
#     '2884.TW': 0.035462,
#     '2885.TW': 0.062520,
#     '2886.TW': 0.046320,
#     '2890.TW': 0.050024,
#     '2891.TW': 0.035904,
#     '2912.TW': 0.035114,
#     '3008.TW': 0.035797,
#     '3231.TW': 0.018399,
#     '3661.TW': 0.034974,
#     '4938.TW': 0.039800,
#     '5871.TW': 0.032435,
#     '6505.TW': 0.033844,
#     '6669.TW': 0.035105
# }
weights = {
    '1101.TW': 0.058578,
    '1216.TW': 0.039290,
    '1301.TW': 0.000000,
'1303.TW': 0.000000,
'1326.TW': 0.000000,
'1590.TW': 0.038583,
'2002.TW': 0.000000,
'2207.TW': 0.038479,
'2301.TW': 0.000000,
'2303.TW': 0.000000,
'2308.TW': 0.038893,
'2317.TW': 0.000000,
'2327.TW': 0.040506,
'2330.TW': 0.051002,
'2345.TW': 0.000000,
'2357.TW': 0.000000,
'2379.TW': 0.025260,
'2382.TW': 0.000000,
'2395.TW': 0.049748,
'2408.TW': 0.000000,
'2412.TW': 0.037599,
'2454.TW': 0.039905,
'2603.TW': 0.000000,
'2880.TW': 0.000000,
'2881.TW': 0.039567,
'2882.TW': 0.000000,
'2883.TW': 0.000000,
'2884.TW': 0.039334,
'2885.TW': 0.045974,
'2886.TW': 0.031034,
'2887.TW': 0.000000,
'2890.TW': 0.060871,
'2891.TW': 0.038354,
'2892.TW': 0.000000,
'2912.TW': 0.038583,
'3008.TW': 0.039405,
'3017.TW': 0.000000,
'3034.TW': 0.000000,
'3037.TW': 0.000000,
'3045.TW': 0.000000,
'3231.TW': 0.009339,
'3661.TW': 0.038322,
'3711.TW': 0.000000,
'4904.TW': 0.000000,
'4938.TW': 0.050036,
'5871.TW': 0.036660,
'5876.TW': 0.000000,
'5880.TW': 0.000000,
'6505.TW': 0.036295,
'6669.TW': 0.038383
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
