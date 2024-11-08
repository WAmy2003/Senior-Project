import glob
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression

# Part 1: 整理數據
# path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據\\' # 日數據
path = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據_週\\' # 週數據
all_files = glob.glob(path + "*.csv")

df_list = []
for filename in all_files:
    stock_id = os.path.basename(filename)[:4]
    df = pd.read_csv(filename)
    df['stock_id'] = stock_id
    df_list.append(df)

data = pd.concat(df_list, axis=0, ignore_index=True)
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data.set_index(['date', 'stock_id'], inplace=True)

# 定義特徵和目標變數
features = ['Dealer', 'Foreign_Investor', 'Investment_Trust', 'RSI', 'SMA', 'WMA', 
            'MACD', 'MACD_Signal', 'KD_K', 'KD_D', 'Bollinger_Upper', 'Bollinger_Middle', 
            'Bollinger_Lower', 'CK_Index', 'sentiment_score']
target = 'close'

# Part 2: 分割訓練和測試數據集（按日期分割）
split_date = '2024-06-01'
train_data = data[data.index.get_level_values('date') <= split_date]
test_data = data[data.index.get_level_values('date') > split_date]
test_data = test_data.copy()

# 確認所有股票在兩個數據集中均存在
train_stock_ids = set(train_data.index.get_level_values('stock_id'))
test_stock_ids = set(test_data.index.get_level_values('stock_id'))

# 基模型：隨機森林和XGBoost
rf = RandomForestRegressor(n_estimators=100, random_state=42)
xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# 預測生成新的特徵集
train_meta_features = pd.DataFrame(index=train_data.index)
test_meta_features = pd.DataFrame(index=test_data.index)

for model, name in zip([rf, xgb], ['rf', 'xgb']):
    train_meta_features[name] = cross_val_predict(model, train_data[features], train_data[target], cv=5)
    model.fit(train_data[features], train_data[target])
    test_meta_features[name] = model.predict(test_data[features])

# 元學習器：線性回歸
meta_learner = LinearRegression()
meta_learner.fit(train_meta_features, train_data[target])

# 使用.loc來避免警告
test_data.loc[:, 'predicted_close'] = meta_learner.predict(test_meta_features)

# 計算報酬率，使用.loc避免警告
test_data.loc[:, 'return'] = test_data['predicted_close'].pct_change()

# 去除空值以避免空結果
test_data = test_data.dropna(subset=['return'])

# 計算夏普比率
risk_free_rate = 0.01  # 假設無風險利率
sharpe_ratio = (test_data['return'].mean() - risk_free_rate) / test_data['return'].std()

# 計算各股票的投資權重（基於夏普值最大化）
weights = (test_data.groupby('stock_id')['return'].mean() / test_data.groupby('stock_id')['return'].std())
weights = weights.dropna()  # 去除可能的NaN值
weights[weights < 0] = 0    # 將負值權重設為 0
weights = weights / weights.sum()  # 標準化至權重總和為 1

# 最終輸出50支股票的投資權重
result = weights.to_frame(name='investment_weight')
print(weights.sum())
print("投資權重結果:")
print(result)

