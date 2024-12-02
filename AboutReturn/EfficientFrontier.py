# import yfinance as yf
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # 股票代碼
# tickers = [
#     '1101.TW', '1216.TW', '1326.TW', '1590.TW', '2207.TW', '2308.TW', '2327.TW',
#     '2330.TW', '2379.TW', '2395.TW', '2412.TW', '2454.TW', '2881.TW', '2884.TW',
#     '2885.TW', '2886.TW', '2890.TW', '2891.TW', '2912.TW', '3008.TW', '3231.TW',
#     '3661.TW', '4938.TW', '5871.TW', '6505.TW', '6669.TW'
# ]

# # 下載股票歷史價格數據
# data = yf.download(tickers, start='2023-07-01', end='2023-09-30')['Adj Close']

# # 計算每日收益率
# returns = data.pct_change().apply(lambda x: np.log(1+x))

# # 共變異數矩陣
# cov_matrix = returns.cov()

# # 平均報酬率
# expected_return = returns.mean() * 252  # 年化平均報酬率

# # 標準差 (年化)
# standard_dev = returns.std() * np.sqrt(252)

# # 投資組合模擬
# port_ret = []
# port_dev = []
# port_weights = []
# assets_nums = len(tickers)
# port_nums = 100000

# for port in range(port_nums):
#     weights = np.random.random(assets_nums)
#     weights = weights / np.sum(weights)
#     port_weights.append(weights)

#     # 計算投資組合的回報
#     returns = np.dot(weights, expected_return)
#     port_ret.append(returns)

#     # 計算投資組合的風險 (波動度)
#     var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
#     sd = np.sqrt(var)
#     ann_sd = sd * np.sqrt(252)
#     port_dev.append(ann_sd)

# # 收集投資組合數據
# data = {'Returns': port_ret, 'Standard Dev.': port_dev}
# for counter, symbol in enumerate(tickers):
#     data[symbol + ' weight'] = [w[counter] for w in port_weights]

# portfolios = pd.DataFrame(data)

# # 取效率前緣
# std = []
# ret = [portfolios[portfolios['Standard Dev.'] == portfolios['Standard Dev.'].min()]['Returns'].values[0]]
# eff_front_set = pd.DataFrame(columns=['Returns', 'Standard Dev.'] + [symbol + ' weight' for symbol in tickers])

# for i in range(800, 1800, 1):
#     df = portfolios[(portfolios['Standard Dev.'] >= i/10000) & (portfolios['Standard Dev.'] <= (i+15)/10000)]
#     try:
#         # 上側
#         max_ret = df[df['Returns'] == df['Returns'].max()]['Returns'].values[0]
#         if max_ret >= max(ret):
#             std.append(df[df['Returns'] == df['Returns'].max()]['Standard Dev.'].values[0])
#             ret.append(df[df['Returns'] == df['Returns'].max()]['Returns'].values[0])
#             eff_front_set = eff_front_set.append(df[df['Returns'] == df['Returns'].max()], ignore_index=True)
#     except:
#         pass

# ret.pop(0)
# eff_front_std = pd.Series(std)
# eff_front_ret = pd.Series(ret)

# # 繪製散點圖和效率前緣
# plt.figure(figsize=(10,7))
# plt.scatter(x=portfolios['Standard Dev.'], y=portfolios['Returns'], alpha=0.5, label='Portfolios')

# # 標示有效前緣（使用線條連接）
# plt.plot(eff_front_std, eff_front_ret, 'r-', linewidth=2, label='Efficient Frontier')

# # 顯示圖例和其他設置
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.xlabel("Standard Deviation", fontsize=12)
# plt.ylabel("Expected Returns", fontsize=12)
# plt.title("Portfolio Optimization - Efficient Frontier", fontsize=14)
# plt.legend(fontsize=10)
# plt.show()

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 股票代碼
tickers = [
    '1101.TW', '1216.TW', '1326.TW', '1590.TW', '2207.TW', '2308.TW', '2327.TW',
    '2330.TW', '2379.TW', '2395.TW', '2412.TW', '2454.TW', '2881.TW', '2884.TW',
    '2885.TW', '2886.TW', '2890.TW', '2891.TW', '2912.TW', '3008.TW', '3231.TW',
    '3661.TW', '4938.TW', '5871.TW', '6505.TW', '6669.TW'
]

# 下載股票歷史價格數據
data = yf.download(tickers, start='2024-07-01', end='2024-09-30')['Adj Close']

# 計算每日收益率
returns = data.pct_change().apply(lambda x: np.log(1+x))

# 共變異數矩陣
cov_matrix = returns.cov()

# 平均報酬率
expected_return = returns.mean() * 252  # 年化平均報酬率

# 標準差 (年化)
standard_dev = returns.std() * np.sqrt(252)

# 投資組合模擬
port_ret = []
port_dev = []
port_weights = []
assets_nums = len(tickers)
port_nums = 100000

for port in range(port_nums):
    weights = np.random.random(assets_nums)
    weights = weights / np.sum(weights)
    port_weights.append(weights)

    # 計算投資組合的回報
    returns = np.dot(weights, expected_return)
    port_ret.append(returns)

    # 計算投資組合的風險 (波動度)
    var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()
    sd = np.sqrt(var)
    ann_sd = sd * np.sqrt(252)
    port_dev.append(ann_sd)

# 收集投資組合數據
data = {'Returns': port_ret, 'Standard Dev.': port_dev}
for counter, symbol in enumerate(tickers):
    data[symbol + ' weight'] = [w[counter] for w in port_weights]

portfolios = pd.DataFrame(data)

# 取效率前緣
std = []
ret = [portfolios[portfolios['Standard Dev.'] == portfolios['Standard Dev.'].min()]['Returns'].values[0]]
eff_front_set = pd.DataFrame(columns=['Returns', 'Standard Dev.'] + [symbol + ' weight' for symbol in tickers])

for i in range(800, 1800, 1):
    df = portfolios[(portfolios['Standard Dev.'] >= i/10000) & (portfolios['Standard Dev.'] <= (i+15)/10000)]
    try:
        # 上側
        max_ret = df[df['Returns'] == df['Returns'].max()]['Returns'].values[0]
        if max_ret >= max(ret):
            std.append(df[df['Returns'] == df['Returns'].max()]['Standard Dev.'].values[0])
            ret.append(df[df['Returns'] == df['Returns'].max()]['Returns'].values[0])
            eff_front_set = eff_front_set.append(df[df['Returns'] == df['Returns'].max()], ignore_index=True)
    except:
        pass

ret.pop(0)
eff_front_std = pd.Series(std)
eff_front_ret = pd.Series(ret)

# 繪製散點圖和效率前緣
plt.figure(figsize=(10,7))
plt.scatter(x=portfolios['Standard Dev.'], y=portfolios['Returns'], alpha=0.5, label='Portfolios')

# 標示有效前緣（使用線條連接）
plt.plot(eff_front_std, eff_front_ret, 'r-', linewidth=2, label='Efficient Frontier')

# 顯示圖例和其他設置
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel("Standard Deviation", fontsize=12)
plt.ylabel("Expected Returns", fontsize=12)
plt.title("Portfolio Optimization - Efficient Frontier", fontsize=14)
plt.legend(fontsize=10)
plt.show()

# 顯示效率前緣上的投資組合權重
print("\n效率前緣上的投資組合權重：")
weights_columns = [col for col in eff_front_set.columns if 'weight' in col]
portfolio_weights = eff_front_set[weights_columns]

# 為了更好的可讀性，我們將權重轉換為百分比並保留兩位小數
portfolio_weights = portfolio_weights * 100
portfolio_weights = portfolio_weights.round(2)

# 添加預期報酬率和標準差
portfolio_weights['Expected Return'] = eff_front_set['Returns'].round(4)
portfolio_weights['Standard Dev.'] = eff_front_set['Standard Dev.'].round(4)

# 重新命名列名，移除 ' weight' 後綴
portfolio_weights.columns = [col.replace(' weight', '') for col in portfolio_weights.columns]

# 顯示結果
print("\n投資組合權重矩陣（百分比）：")
print(portfolio_weights.to_string())

# 儲存結果到CSV檔案
portfolio_weights.to_csv('efficient_frontier_weights.csv')
print("\n權重數據已保存到 'efficient_frontier_weights.csv'")