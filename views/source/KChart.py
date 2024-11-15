import pandas as pd
import datetime as dt
import json
import requests
from fugle_marketdata import RestClient

# 輸入您的 API key
key = "Njg1M2VkY2ItZjQ2NC00M2VjLTk5NjMtODFlMjA3YzA2NzdlIDY3NGQ3ZTRmLWZkNDktNGVkNy1iMTkyLTUzZDk4ODY4YzkwMw=="
client = RestClient(api_key=key)

# 定義獲取歷史數據的函數
def get_historical_data(stock_no):
    html = requests.get('https://ws.api.cnyes.com/ws/api/v1/charting/history?resolution=D&symbol=TWS:%s:STOCK&from=1728000015&to=1728000000' % (stock_no))
    content = json.loads(html.text)
    open = content['data']['o']
    high = content['data']['h']
    low = content['data']['l']
    close = content['data']['c']
    volume = content['data']['v']
    data = {
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    }
    df = pd.DataFrame(data=data)
    df_reversed = df.iloc[::-1]
    d = df_reversed.tail(1)
    return d

# 主函數，模擬 `get_data` 的功能
def get_data(ticker='2330'):
    to_date = dt.date.today().strftime('%Y-%m-%d')
    from_date = (dt.date.today() - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    stock = client.stock

    try:
        # 從 Fugle API 獲取歷史 K 線資料
        s = stock.historical.candles(**{"symbol": ticker, "from": from_date, "to": to_date, "fields": "open,high,low,close,volume,change"})
        stock_data = s['data']
        
        df = pd.DataFrame(stock_data)
        
        # 保留需要的列並重命名以符合圖表格式
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Volume'] = df['Volume'] / 1000  # 將成交量除以1000
        df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d").dt.date
        df = df.sort_values(by='Date', ascending=True)

        # 加上今日的數據
        last_row_data = get_historical_data(ticker)
        today_date = dt.date.today()

        if df.iloc[-1]['Date'] != today_date:
            last_row_data['Date'] = today_date
            last_row_df = pd.DataFrame({
                'Date': [today_date],
                'Open': last_row_data['open'].values,
                'High': last_row_data['high'].values,
                'Low': last_row_data['low'].values,
                'Close': last_row_data['close'].values,
                'Volume': last_row_data['volume'].values
            })

            # 合併最後一行數據
            df = pd.concat([df, last_row_df], ignore_index=True)

        # 將數據轉換為 JSON 格式並返回
        data_json = {
            'name': ticker,
            'data': df.to_dict(orient='records')
        }
        
        # 打印 JSON 結果
        print(json.dumps(data_json, indent=4, ensure_ascii=False))
    
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")

# 輸入股票代碼並執行
ticker = input("請輸入股票代碼 (預設為 2330): ") or "2330"
get_data(ticker)
