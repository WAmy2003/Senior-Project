import yfinance as yf
import pandas as pd
import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')
# 抓取台灣加權指數 (^TWII) 的數據
taiex = yf.download("^TWII", start="2024-07-01", end="2024-10-01")

start_price = taiex['Close'].iloc[0]
cumulative_returns = ((taiex['Close'] / start_price) - 1).round(6)

# 將累積報酬率轉換為 DataFrame，並重設索引
cumulative_returns = cumulative_returns.reset_index()
cumulative_returns.columns = ['date', 'return_0000']

# 確保只有 Close 欄位
close_prices = taiex['Close']

# 計算年化報酬率（幾何平均）
total_return = (close_prices.iloc[-1] / close_prices.iloc[0]) - 1
days = len(close_prices)
annual_return_geometric = (1 + total_return) ** (252/days) - 1

# 印出數據
print(close_prices)

# 修正 Series 為單一值的情況
print(f"年化報酬率（幾何平均）: {annual_return_geometric.item() * 100:.2f}%")

# 連接數據庫並更新表格
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# # 添加新列到現有表格（僅在欄位不存在時執行）
# cursor.execute('''
# ALTER TABLE history_returns ADD COLUMN return_0000 REAL DEFAULT NULL;
# ''')

# 更新數據
for _, row in cumulative_returns.iterrows():
    cursor.execute('''
    UPDATE history_returns 
    SET return_0000 = ?
    WHERE date = ?
    ''', (float(row['return_0000']), row['date'].strftime('%Y-%m-%d')))

# 提交更改並關閉連接
conn.commit()