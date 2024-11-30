import glob
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
import sqlite3
import warnings
warnings.filterwarnings('ignore')

def load_and_process_data(path):
    path = os.path.join(path, "*.csv")
    print(f"搜尋路徑: {path}")
    
    all_files = glob.glob(path)
    print(f"找到的檔案數量: {len(all_files)}")
    
    if len(all_files) == 0:
        raise ValueError(f"在路徑 {path} 中沒有找到CSV檔案")
    
    df_list = []
    for filename in all_files:
        try:
            stock_id = os.path.basename(filename)[:4]
            df = pd.read_csv(filename)
            df['stock_id'] = stock_id
            df_list.append(df)
        except Exception as e:
            print(f"處理檔案 {filename} 時發生錯誤: {e}")
    
    data = pd.concat(df_list, axis=0, ignore_index=True)
    data['date'] = pd.to_datetime(data['date'], errors='coerce')
    data.set_index(['date', 'stock_id'], inplace=True)
    
    return data

def enhance_features(data):
    """增強特徵工程"""
    try:
        # 基礎技術指標交叉信號
        data['MACD_Cross'] = np.where(data['MACD'] > data['MACD_Signal'], 1, -1)
        data['KD_Cross'] = np.where(data['KD_K'] > data['KD_D'], 1, -1)
        
        # 價格動量指標 - 使用 fillna 處理開始期間的空值
        data['Price_Momentum_5'] = data.groupby(level='stock_id')['close'].pct_change(5).fillna(0)
        data['Price_Momentum_20'] = data.groupby(level='stock_id')['close'].pct_change(20).fillna(0)
        
        # 波動率指標 - 使用 fillna 處理開始期間的空值
        data['Volatility'] = data.groupby(level='stock_id')['close'].rolling(window=20).std().reset_index(0, drop=True).fillna(method='bfill').fillna(0)
        
        # 機構投資者活動指標
        data['Inst_Activity'] = data['Foreign_Investor'] + data['Investment_Trust'] - data['Dealer']
        
        # RSI強度
        data['RSI_Strength'] = (data['RSI'] - 50) / 50
        
        # 布林通道寬度
        data['Bollinger_Width'] = (data['Bollinger_Upper'] - data['Bollinger_Lower']) / data['Bollinger_Middle']
        
        # 技術指標綜合強度
        data['Technical_Strength'] = (
            (data['RSI_Strength'] + 
             data['MACD_Cross'] + 
             data['KD_Cross']) / 3
        )
        
    except Exception as e:
        print(f"特徵工程過程中發生錯誤: {e}")
        raise
        
    return data

def normalize_data(data):
    """數據標準化"""
    columns_to_normalize = [
        'Dealer', 'Foreign_Investor', 'Investment_Trust', 
        'RSI', 'SMA', 'WMA', 'MACD', 'MACD_Signal', 'KD_K', 'KD_D',
        'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
        'Price_Momentum_5', 'Price_Momentum_20', 'Volatility',
        'Inst_Activity', 'RSI_Strength', 'Bollinger_Width',
        'Technical_Strength'
    ]
    
    normalized_data = data.copy()
    
    # for stock_id in data.index.get_level_values('stock_id').unique():
    #     stock_data = data.xs(stock_id, level='stock_id')
        
    #     for column in columns_to_normalize:
    #         if column in stock_data.columns:
    #             min_value = stock_data[column].min()
    #             max_value = stock_data[column].max()
    #             if max_value != min_value:
    #                 normalized_data.loc[(slice(None), stock_id), column] = (
    #                     (stock_data[column] - min_value) / (max_value - min_value)
    #                 )
    # 對於需要重新計算的欄位，將每個欄位標準化
    for column in columns_to_normalize:
        min_value = normalized_data[column].min()
        max_value = normalized_data[column].max()
        normalized_data[column] = (normalized_data[column] - min_value) / (max_value - min_value)

    
    normalized_data['CK_Index'] = normalized_data['CK_Index'] / 100
    
    return normalized_data

def calculate_optimized_weights(test_data, risk_free_rate=0.02, max_stock_weight=0.15,
                              min_stock_weight=0.01):
    """計算最優化投資組合權重"""
    # 計算每支股票的預期報酬和風險指標
    stock_metrics = {}
    
    for stock_id in test_data.index.get_level_values('stock_id').unique():
        stock_data = test_data.xs(stock_id, level='stock_id')
        
        # 計算預期報酬率
        returns = stock_data['predicted_close'].pct_change()
        exp_return = returns.mean() * 252  # 年化
        volatility = returns.std() * np.sqrt(252)  # 年化
        
        # 技術指標綜合評分
        tech_score = stock_data[['RSI_Strength', 'Technical_Strength']].mean().mean()
        
        # 機構投資者活動評分
        inst_score = stock_data['Inst_Activity'].mean()
        
        # 計算修正夏普比率
        sharpe = (exp_return - risk_free_rate) / volatility if volatility != 0 else 0
        
        # 綜合評分
        total_score = (
            sharpe * 0.4 +          # 夏普比率權重
            tech_score * 0.3 +      # 技術指標權重
            inst_score * 0.3        # 機構投資者權重
        )
        
        stock_metrics[stock_id] = total_score
    
    # 轉換為權重
    weights = pd.Series(stock_metrics)
    weights = weights.clip(lower=0)  # 確保非負
    
    # 應用最小權重限制
    weights[weights < min_stock_weight] = 0
    
    # 標準化權重
    if weights.sum() > 0:
        weights = weights / weights.sum()
    
    # 應用最大權重限制
    weights[weights > max_stock_weight] = max_stock_weight
    
    # 最終標準化
    weights = weights / weights.sum()
    
    return weights

def data_to_sql(portfolio_weights, db_path, stock_dict):
    portfolio_weights = portfolio_weights.round(4)  # 先四捨五入到4位小數
    # 將 portfolio_weights Series 轉換為 DataFrame
    results = pd.DataFrame(portfolio_weights, columns=['weights'])
    results.index.name = 'stock_id'
    results.reset_index(inplace=True)

    # 過濾掉權重為 0 的資料
    results = results[results['weights'] > 0]

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
    for _, row in results.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO portfolio_weights (stock_id, stock_name, weights)
        VALUES (?, ?, ?)
        ''', (row['stock_id'], stock_dict[row['stock_id']], float(row['weights'])))
    
    # 提交更改並關閉連接
    conn.commit()
    conn.close()
    print(f"數據已成功寫入{db_path}")

def main(isNormalized=True, use_train_set=False):
    # 設定路徑和參數
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Django', 'db.sqlite3')
    path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據'
    
    # 特徵集
    features = [
        'Dealer', 'Foreign_Investor', 'Investment_Trust',
        'RSI', 'SMA', 'WMA', 'MACD', 'MACD_Signal',
        'KD_K', 'KD_D', 'Bollinger_Upper', 'Bollinger_Middle',
        'Bollinger_Lower', 'CK_Index', 'sentiment_score',
        'MACD_Cross', 'KD_Cross', 'Price_Momentum_5', 'Price_Momentum_20',
        'Volatility', 'RSI_Strength', 'Technical_Strength', 'Inst_Activity',
        'Bollinger_Width'
    ]

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
        # 1. 載入和處理數據
        print("開始載入數據...")
        data = load_and_process_data(path)
        
        # 2. 特徵增強
        print("進行特徵工程...")
        data = enhance_features(data)       
        
        if isNormalized:
            print("進行數據標準化...")
            data = normalize_data(data)
        
        # 3. 時間序列分割
        train_data = data[data.index.get_level_values('date') <= split_date]
        test_data = data[data.index.get_level_values('date') > split_date].copy()
        
        
        print(f"訓練資料大小: {train_data.shape}")
        print(f"測試資料大小: {test_data.shape}")
        
        # 4. 模型訓練與預測
        print("開始訓練模型集成...")
        models = {
            'rf': RandomForestRegressor(n_estimators=200, max_depth=10, min_samples_split=5, random_state=42),
            'xgb': XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42),
            'gbm': GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=6, random_state=42)
        }
        
        predictions = {}
        feature_importance = {}
        
        for name, model in models.items():
            print(f"訓練 {name} 模型...")
            model.fit(train_data[features], train_data[target])
            predictions[name] = model.predict(test_data[features])
            
            if hasattr(model, 'feature_importances_'):
                feature_importance[name] = dict(zip(features, model.feature_importances_))
                top_features = sorted(feature_importance[name].items(), key=lambda x: x[1], reverse=True)[:5]
                print(f"\n{name} 模型前5大重要特徵:")
                for feature, importance in top_features:
                    print(f"{feature}: {importance:.4f}")
        
        # 5. 集成預測結果
        model_weights = {'rf': 0.5, 'xgb': 0.35, 'gbm': 0.15}
        # 根據開關選擇使用訓練集或測試集
        if use_train_set:
            train_data['predicted_close'] = sum(
                model.predict(train_data[features]) * weight 
                for (name, model), weight in zip(models.items(), model_weights.values())
            )
            prediction_data = train_data
            print("\n使用訓練集計算權重...")
        else:
            test_data['predicted_close'] = sum(
                predictions[model] * weight 
                for model, weight in model_weights.items()
            )
            prediction_data = test_data
            print("\n使用測試集計算權重...")
        
        # 6. 計算最優投資組合權重
        print("\n計算最優投資組合權重...")
        portfolio_weights = calculate_optimized_weights(
            prediction_data,
            risk_free_rate=0.02,
            max_stock_weight=0.15,
            min_stock_weight=0.01
        )
        
        # 7. 輸出結果與存入DB
        print("\n====== 投資組合權重分配 ======")
        for stock_id, weight in portfolio_weights.items():
            if weight >= 0.01:  # 只顯示權重大於1%的股票
                print(f"股票 {stock_id}: {weight:.4f}")
        
        print(f"\n總權重: {portfolio_weights.sum():.4f}")
        # 存入DB
        data_to_sql(portfolio_weights, db_path, stock_dict)
        
    except Exception as e:
        print(f"程式執行過程中發生錯誤: {e}")
        raise

if __name__ == "__main__":
    # 使用測試集
    main(True, True)  # 第二個參數 False 表示使用測試集