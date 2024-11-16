import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os
import glob

def normalizeCSV(inputDir, outputDir, scaler_type='minmax'):
    print("當前工作目錄:", os.getcwd())
    print(f"輸入目錄: {inputDir}")
    print(f"輸出目錄: {outputDir}")
    
    # 創建輸出目錄
    os.makedirs(outputDir, exist_ok=True)
    
    # 尋找符合模式的CSV文件
    pattern = os.path.join(inputDir, '*_數據蒐集.csv')
    print(f"使用的文件匹配模式: {pattern}")
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        print(f"在目錄 '{inputDir}' 中未找到符合模式 '*_數據蒐集.csv' 的文件。")
        return
    
    print(f"找到 {len(csv_files)} 個文件，開始處理...")
    
    # 定義需要正規化的欄位
    normalize_columns = ['Dealer', 'Foreign_Investor', 'Investment_Trust', 
                        'RSI', 'SMA', 'WMA', 'MACD', 'MACD_Signal',
                        'KD_K', 'KD_D', 'Bollinger_Upper', 'Bollinger_Middle', 
                        'Bollinger_Lower']
    
    # 不處理的欄位
    skip_columns = ['date', 'sentiment_score', 'close']
    
    for file_path in csv_files:
        try:
            file_name = os.path.basename(file_path)
            print(f"\n處理文件: {file_name}")
            
            # 讀取CSV文件
            df = pd.read_csv(file_path)
            print(f"讀取文件 '{file_name}' 成功，行數: {len(df)}")
            
            if 'date' not in df.columns:
                print(f"警告: 文件 '{file_name}' 中未找到 'date' 欄位，跳過此文件。")
                continue
            
            # 分離需要處理和不需要處理的欄位
            to_normalize = df[normalize_columns].copy()
            skipped = df[skip_columns].copy()
            
            # 處理CK_Index（除以100）
            if 'CK_Index' in df.columns:
                df['CK_Index'] = df['CK_Index'] / 100
            
            # 轉換數據為數值型
            to_normalize = to_normalize.apply(pd.to_numeric, errors='coerce')
            print("轉換數據為數值型成功")
            
            # 處理缺失值
            if to_normalize.isnull().values.any():
                print("數據中存在缺失值，將使用均值填補缺失值。")
                to_normalize = to_normalize.fillna(to_normalize.mean())
                print("填補缺失值成功")
            
            # 選擇正規化方法
            if scaler_type.lower() == 'minmax':
                scaler = MinMaxScaler()
            elif scaler_type.lower() == 'standard':
                scaler = StandardScaler()
            else:
                print(f"未知的 scaler_type '{scaler_type}'，預設使用 'minmax'。")
                scaler = MinMaxScaler()
            
            # 正規化數據
            normalized_data = scaler.fit_transform(to_normalize)
            print("正規化數據成功")
            
            # 轉換回DataFrame
            normalized_df = pd.DataFrame(normalized_data, columns=to_normalize.columns)
            print("轉換為 DataFrame 成功")
            
            # 合併所有欄位
            final_df = pd.concat([skipped, normalized_df], axis=1)
            if 'CK_Index' in df.columns:
                final_df['CK_Index'] = df['CK_Index']
            
            # 確保欄位順序與原始檔案相同
            final_df = final_df.reindex(columns=df.columns)
            
            # 生成輸出文件名
            stock_code = file_name.split('_')[0]
            output_file_name = f"{stock_code}_normalized.csv"
            output_file_path = os.path.join(outputDir, output_file_name)
            
            # 儲存檔案
            final_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
            print(f"已保存正規化後的數據到 '{output_file_name}'")
            
        except Exception as e:
            print(f"處理文件 '{file_name}' 時發生錯誤: {e}")
    
    print("\n所有文件處理完畢。")

if __name__ == "__main__":
    input_directory = "C:\\Users\\user\\OneDrive\\桌面\\畢業專題\\資料蒐集\\原始數據"
    output_directory = 'normalized_data'
    scaler_choice = 'minmax'  # 正規化方法：'minmax' 或 'standard'
    
    # 執行正規化
    normalizeCSV(input_directory, output_directory, scaler_type=scaler_choice)