import glob
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
import sqlite3
import os

def load_and_process_data(path):
    # 確保路徑格式正確
    path = os.path.join(path, "*.csv")
    print(f"搜尋路徑: {path}")
    
    # 獲取所有CSV檔案
    all_files = glob.glob(path)
    print(f"找到的檔案數量: {len(all_files)}")
    
    if len(all_files) == 0:
        raise ValueError(f"在路徑 {path} 中沒有找到CSV檔案")
    
    # 讀取所有檔案
    df_list = []
    for filename in all_files:
        try:
            stock_id = os.path.basename(filename)[:4]
            df = pd.read_csv(filename)
            df['stock_id'] = stock_id
            df_list.append(df)
        except Exception as e:
            print(f"處理檔案 {filename} 時發生錯誤: {e}")
    
    # 合併所有數據
    data = pd.concat(df_list, axis=0, ignore_index=True)
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.set_index(['date', 'stock_id'], inplace=True)
    
    return data

def normalize_data(data):
    columns_to_normalize = ['RSI', 'SMA', 'WMA', 'MACD', 'MACD_Signal', 'KD_K', 'KD_D', 
                        'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower']

    # 對於需要重新計算的欄位，將每個欄位標準化
    for column in columns_to_normalize:
        min_value = data[column].min()
        max_value = data[column].max()
        data[column] = (data[column] - min_value) / (max_value - min_value)

    # 將 CK_Index 欄位除以 100
    data['CK_Index'] = data['CK_Index'] / 100

    return data

def train_and_predict(data, features, target, split_date):
    # 分割訓練和測試數據集
    train_data = data[data.index.get_level_values('date') <= split_date]
    test_data = data[data.index.get_level_values('date') > split_date]
    test_data = test_data.copy()
    
    print(f"訓練數據大小: {train_data.shape}")
    print(f"測試數據大小: {test_data.shape}")
    
    # 基礎模型
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    
    # 生成元特徵
    train_meta_features = pd.DataFrame(index=train_data.index)
    test_meta_features = pd.DataFrame(index=test_data.index)
    
    for model, name in zip([rf, xgb], ['rf', 'xgb']):
        print(f"訓練 {name} 模型...")
        train_meta_features[name] = cross_val_predict(model, train_data[features], train_data[target], cv=5)
        model.fit(train_data[features], train_data[target])
        test_meta_features[name] = model.predict(test_data[features])
    
    # 元學習器
    meta_learner = LinearRegression()
    meta_learner.fit(train_meta_features, train_data[target])
    
    return test_data, test_meta_features, meta_learner

def calculate_portfolio_weights(test_data, test_meta_features, meta_learner, risk_free_rate=0.01):
    # 預測收盤價
    test_data.loc[:, 'predicted_close'] = meta_learner.predict(test_meta_features)
    
    # 計算報酬率
    test_data.loc[:, 'return'] = test_data['predicted_close'].pct_change()
    
    # 去除空值
    test_data = test_data.dropna(subset=['return'])
    
    # 計算夏普比率
    sharpe_ratio = (test_data['return'].mean() - risk_free_rate) / test_data['return'].std()
    print(f"投資組合夏普比率: {sharpe_ratio}")
    
    # 計算各股票權重
    weights = (test_data.groupby('stock_id')['return'].mean() / 
              test_data.groupby('stock_id')['return'].std())
    weights = weights.dropna()
    weights[weights < 0] = 0
    weights = weights / weights.sum()
    weights = weights.round(4)
    
    return weights

def data_to_sql(results, db_path, stock_dict):

    # 過濾掉權重為 0 的資料
    results = results[results['investment_weight'] > 0]

    # 連接SQLite數據庫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 創建表格
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio_weights (
        stock_id TEXT PRIMARY KEY,
        stock_name TEXT,
        weights REAL
    )
    ''')
    
    # 插入數據
    for stock_id, row in results.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO portfolio_weights (stock_id, stock_name, weights)
        VALUES (?, ?, ?)
        ''', (stock_id, stock_dict[stock_id], float(row['investment_weight'])))
    
    # 提交更改並關閉連接
    conn.commit()
    print(f"數據已成功寫入{db_path}")

def main(isNormalized):
    # 設定路徑和參數
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')
    path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據'
    features = ['Dealer', 'Foreign_Investor', 'Investment_Trust', 
                'RSI', 'SMA', 'WMA', 'MACD', 'MACD_Signal', 
                'KD_K', 'KD_D', 'Bollinger_Upper', 'Bollinger_Middle', 
                'Bollinger_Lower', 'CK_Index', 'sentiment_score']
    stock_dict = {
    '2330': '台積電', '2317': '鴻海', '2454': '聯發科', '2308': '台達電', '2382': '廣達',
    '2891': '中信金', '2881': '富邦金', '2303': '聯華電子', '3711': '日月光投控', '2882': '國泰金',
    '2886': '兆豐金', '2412': '中華電', '2884': '玉山金', '1216': '統一', '2885': '元大金',
    '3034': '聯詠', '2357': '華碩', '2890': '永豐金', '2892': '第一金', '3231': '緯創',
    '2345': '智邦', '3008': '大立光', '2327': '國巨', '5880': '合庫金', '2002': '中鋼',
    '2880': '華南金', '2379': '瑞昱', '1303': '南亞', '2883': '凱基', '6669': '緯穎',
    '1101': '台泥', '2887': '台新金', '3037': '欣興', '2301': '光寶', '3017': '奇鋐',
    '1301': '台塑', '4938': '和碩', '2207': '和泰', '3661': '世芯', '2603': '長榮',
    '2395': '研華', '3045': '台灣大哥大', '5876': '上海商銀', '1326': '台化', '4904': '遠傳',
    '2912': '統一超', '1590': '亞德客', '5871': '中租-KY', '6505': '台塑', '2408': '南亞科'
    }
    target = 'close'
    split_date = '2024-06-01'
    
    try:
        # Part 1: 載入和處理數據
        print("開始載入數據...")
        data = load_and_process_data(path)

        if isNormalized == True:
            data = normalize_data(data)
        
        # 訓練模型和預測
        print("開始訓練模型...")
        test_data, test_meta_features, meta_learner = train_and_predict(
            data, features, target, split_date)
        
        # 計算投資組合權重
        print("計算投資組合權重...")
        weights = calculate_portfolio_weights(test_data, test_meta_features, meta_learner)
        
        # 輸出結果
        result = weights.to_frame(name='investment_weight')
        print("\n總權重:", weights.sum())
        # print("\n投資權重結果:")
        # print(result)
        
        # 儲存結果
        data_to_sql(result, db_path, stock_dict)
        # output_path = os.path.join(os.path.dirname(path), 'portfolio_weights.csv')
        # result.to_csv(output_path)
        # print(f"\n結果已儲存至: {output_path}")
        
    except Exception as e:
        print(f"程式執行過程中發生錯誤: {e}")

if __name__ == "__main__":
    main(True)