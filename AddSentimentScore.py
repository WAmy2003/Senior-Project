import pandas as pd
import numpy as np
from datetime import datetime

# 股票代碼清單
stock_ids = [
    '2330', '2317', '2454', '2308', '2382', '2891', '2881', '2303', '3711', '2882',
    '2886', '2412', '2884', '1216', '2885', '3034', '2357', '2890', '2892', '3231',
    '2345', '3008', '2327', '5880', '2002', '2880', '2379', '1303', '2883', '6669',
    '1101', '2887', '3037', '2301', '3017', '1301', '4938', '2207', '3661', '2603',
    '2395', '3045', '5876', '1326', '4904', '2912', '1590', '5871', '6505', '2408'
]

# 路徑格式
txt_path_template = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\情感分析結果\\{}.txt'
csv_path_template = 'C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據\\{}_數據蒐集.csv'

# 依序處理每個股票代碼
for stock_id in stock_ids:
    # 動態生成 txt 和 csv 的路徑
    txt_path = txt_path_template.format(stock_id)
    csv_path = csv_path_template.format(stock_id)

    # 讀取 sentiment_score.txt 並處理數據，確保日期格式一致
    sentiment_scores = {}
    with open(txt_path, 'r') as file:
        for line in file:
            date_str, score = line.strip().split(', ')
            date = datetime.strptime(date_str, '%Y/%m/%d').strftime('%Y/%m/%d')  # 標準化日期格式
            if score != 'UNKNOWN':
                sentiment_scores[date] = float(score)

    # 計算已知 sentiment_score 的平均值
    known_scores = [score for score in sentiment_scores.values()]
    average_score = np.mean(known_scores) if known_scores else 0

    # 讀取股票的 CSV 檔案並標準化日期格式
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d').dt.strftime('%Y/%m/%d')

    # 新增 sentiment_score 欄位，根據日期匹配 sentiment_score，若無匹配或為 UNKNOWN 則填入平均值
    df['sentiment_score'] = df['date'].apply(
        lambda date: sentiment_scores.get(date, average_score)
    )

    # 將結果寫回原始的 CSV 檔案
    df.to_csv(csv_path, index=False)
    print(f"已在 {csv_path} 中新增 sentiment_score 欄位。")
