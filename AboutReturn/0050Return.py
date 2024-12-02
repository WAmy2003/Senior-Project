import requests
import json
import pandas as pd
import sqlite3
import os
import yfinance as yf

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')

# 從 yfinance 獲取歷史價格數據
prices = yf.download('0050.TW', start='2024-07-01', end='2024-10-01')['Adj Close']

start_price = prices.iloc[0]
cumulative_returns = ((prices / start_price) - 1).round(6)

# 將累積報酬率轉換為 DataFrame，並重設索引
cumulative_returns = cumulative_returns.reset_index()
cumulative_returns.columns = ['date', 'return_0050']

# 年化報酬率（簡單算術）
annual_return = cumulative_returns['return_0050'].iloc[-1] * 4

print(f"算術: {annual_return}")

# 連接SQLite數據庫
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
    
# 創建表格 - 只有date和0050兩欄
cursor.execute('''
CREATE TABLE IF NOT EXISTS history_returns (
    date TEXT PRIMARY KEY,
    return_0050 REAL
)
''')
    
# 插入數據
for _, row in cumulative_returns.iterrows():
    cursor.execute('''
    INSERT OR REPLACE INTO history_returns (date, return_0050)
    VALUES (?, ?)
    ''', (row['date'].strftime('%Y-%m-%d'), row['return_0050']))
# for _, row in cumulative_returns.iterrows():
#     cursor.execute('''
#     UPDATE history_returns 
#     SET return_0050 = ?
#     WHERE date = ?
#     ''', (float(row['return_0050']), row['date'].strftime('%Y-%m-%d')))
    
# 提交更改並關閉連接
conn.commit()
conn.close()
print(f"數據已成功寫入{db_path}")

# code = '0050'
# s_date = "2024-07-01"
# e_date = "2024-09-30"

# url = "https://tool.yp-finance.com/api/openInvestment/stockcompare/"
# payload = {
#     "stocks": [code],
#     "startDate": s_date,
#     "endDate": e_date,
#     "isAdj": True
# }
# headers = {
#     "Content-Type": "application/json"
# }

# response = requests.post(url, headers=headers, json=payload)
# data = response.json()
# results = data.get('results', [])
# if results:
#     stock_result = results[0].get('result', {})
#     total_return = stock_result.get('total_return', None)
#     cagr = stock_result.get('cagr', None)
#     sharpe_ratio = stock_result.get('sharpe_ratio', None)
#     history = stock_result.get('history', [])

#     # 顯示提取的資料
#     print(f"總報酬率 (Total Return): {total_return}")
#     print(f"年化報酬率 (CAGR): {cagr}")
#     print(f"夏普比率 (Sharpe Ratio): {sharpe_ratio}")
#     # print(f"歷史報酬率 (History): {history}") 

#     # Convert to DataFrame
#     df = pd.DataFrame(history, columns=['date', '0050'])

#     df['0050'] = ((df['0050'] - 100) / 100).round(6)
#     # print(df)

#     # 連接SQLite數據庫
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # 創建表格 - 只有date和0050兩欄
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS history_returns (
#         date TEXT PRIMARY KEY,
#         return_0050 REAL
#     )
#     ''')
    
#     # 插入數據
#     for index, row in df.iterrows():
#         cursor.execute('''
#         INSERT OR REPLACE INTO history_returns (date, return_0050)
#         VALUES (?, ?)
#         ''', (row['date'], float(row['0050'])))
    
#     # 提交更改並關閉連接
#     conn.commit()
#     print(f"數據已成功寫入{db_path}")

