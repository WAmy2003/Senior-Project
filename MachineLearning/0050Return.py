import requests
import json
import pandas as pd
import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')

code = '0050'
s_date = "2024-07-01"
e_date = "2024-09-30"

url = "https://tool.yp-finance.com/api/openInvestment/stockcompare/"
payload = {
    "stocks": [code],
    "startDate": s_date,
    "endDate": e_date,
    "isAdj": True
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
results = data.get('results', [])
if results:
    stock_result = results[0].get('result', {})
    total_return = stock_result.get('total_return', None)
    cagr = stock_result.get('cagr', None)
    sharpe_ratio = stock_result.get('sharpe_ratio', None)
    history = stock_result.get('history', [])

    # 顯示提取的資料
    print(f"總報酬率 (Total Return): {total_return}")
    print(f"年化報酬率 (CAGR): {cagr}")
    print(f"夏普比率 (Sharpe Ratio): {sharpe_ratio}")
    # print(f"歷史報酬率 (History): {history}") 

    # Convert to DataFrame
    df = pd.DataFrame(history, columns=['date', '0050'])

    df['0050'] = ((df['0050'] - 100) / 100).round(6)
    # print(df)

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
    for index, row in df.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO history_returns (date, return_0050)
        VALUES (?, ?)
        ''', (row['date'], float(row['0050'])))
    
    # 提交更改並關閉連接
    conn.commit()
    print(f"數據已成功寫入{db_path}")



        # csv_path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\HistoryReturn.csv'
        # df.to_csv(csv_path, index=False)
        # print(f"資料已存入{csv_path}")