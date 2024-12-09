import pandas as pd
import sqlite3
import os

def import_data_from_csv(path):
    # 讀取 CSV 檔案
    df = pd.read_csv(path, encoding='utf-8')
        
    # 重新命名欄位以符合資料庫欄位名稱
    df.columns = ['stock_id', 'stock_name', 'quantity', 'weights']

    # 將權重從百分比轉換為小數（除以 100）
    df['weights'] = df['weights'].apply(lambda x: float(x) / 100)

    return df

def data_to_db(db_path, data):
    # 連接SQLite數據庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 創建表格
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio_weights_0050 (
        stock_id TEXT PRIMARY KEY,
        stock_name TEXT,
        weights REAL
    )
    ''')

    for _, row in data.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO portfolio_weights_0050 (stock_id, stock_name, weights)
        VALUES (?, ?, ?)
        ''', (row['stock_id'], row['stock_name'], float(row['weights'])))

    # 提交更改並關閉連接
    conn.commit()
    conn.close()
def main():
    try:
        # CSV 檔案路徑
        path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\0050Q3權重.csv'

        data = import_data_from_csv(path)
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')
        
        # 匯入資料
        data_to_db(db_path, data)
        
    except Exception as e:
        print(f"程式執行失敗: {str(e)}")
        raise

if __name__ == "__main__":
    main()