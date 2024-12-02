import django
import yfinance as yf
import pandas as pd
import sqlite3
import os

def CreateDT(db_path):
    # 連接SQLite數據庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 創建表格
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stocks_daily_return (
        date TEXT,
        stock_id TEXT,
        return REAL,
        PRIMARY KEY (date, stock_id)
    )
    ''')

    # 提交更改並關閉連接
    conn.commit()
    conn.close()
    print("stocks_daily_return 創建完成")

def getPortfolio():
    # 連接SQLite數據庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT stock_id 
        FROM portfolio_weights 
    """)
    rows = cursor.fetchall()
    
    # 將查詢結果轉換為陣列
    stock_ids = [row[0] for row in rows]
    
    # 關閉連接
    conn.close()
    return stock_ids

def getReturns(stock_id):
    # 連接SQLite數據庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 獲得起始日
    cursor.execute("""
        SELECT MIN(date) 
        FROM history_returns
    """)
    min_date = cursor.fetchone()[0]  
    
    # 獲得終止日
    cursor.execute("""
        SELECT MAX(date) 
        FROM history_returns
    """)
    max_date = cursor.fetchone()[0]  
    
    # 關閉連接
    conn.close()
    
    # 抓取stock_id的數據
    data = yf.download(f"{stock_id}.TW", start=min_date, end=max_date)
    
    # 檢查數據是否正確抓取
    if data.empty or 'Close' not in data.columns:
        raise ValueError(f"No valid data found for stock_id: {stock_id}")

    # 計算每一天與 min_date 的報酬率
    min_close = data['Close'].iloc[0]  # 取 min_date 當天的收盤價
    data['Returns'] = ((data['Close'] - min_close) / min_close).round(4)  # 計算報酬率

    # 將結果整理為包含 date 和報酬率的 DataFrame
    results = data[['Returns']].reset_index()  # 重置索引，包含日期
    results.rename(columns={'Date': 'date', 'Returns': 'return_rate'}, inplace=True)

    return results

def saveToDB(stock_id, results, db_path):
    # 連接SQLite數據庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 儲存資料
    for index, row in results.iterrows():
        try:
            # 處理日期 - 直接使用字符串格式
            if isinstance(row['date'], pd.Series):
                date = row['date'].iloc[0]
            else:
                date = row['date']
                
            # 確保日期格式正確
            if isinstance(date, pd.Timestamp):
                date = date.strftime('%Y-%m-%d')
            elif isinstance(date, str):
                date = pd.Timestamp(date).strftime('%Y-%m-%d')
            
            # 確保 return_rate 是浮點數
            if isinstance(row['return_rate'], pd.Series):
                return_rate = float(row['return_rate'].iloc[0])
            else:
                return_rate = float(row['return_rate'])

            cursor.execute('''
                INSERT INTO stocks_daily_return (date, stock_id, return)
                VALUES (?, ?, ?)
            ''', (date, stock_id, return_rate))
        except Exception as e:
            error_date = str(row['date'])  # 為錯誤訊息轉換日期為字符串
            print(f"Error saving data for {stock_id} on {error_date}: {e}")

    # 提交更改並關閉連接
    conn.commit()
    conn.close()
    print(stock_id, " 資料儲存完成")


if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')
    CreateDT(db_path)
    stock_ids = getPortfolio()
    print("獲取投資組合完成")
    for stock_id in stock_ids:
        results = getReturns(stock_id)
        print("計算完報酬率: ", stock_id)
        saveToDB(stock_id, results, db_path)