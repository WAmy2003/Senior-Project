import pandas as pd
import datetime as dt
import json
import requests
from fugle_marketdata import RestClient
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging

# 建立 JSON 序列化器來處理日期格式
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dt.date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../', static_url_path='')
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# API key設置
key = "Njg1M2VkY2ItZjQ2NC00M2VjLTk5NjMtODFlMjA3YzA2NzdlIDY3NGQ3ZTRmLWZkNDktNGVkNy1iMTkyLTUzZDk4ODY4YzkwMw=="
client = RestClient(api_key=key)

def get_historical_data(stock_no):
    """獲取即時股票數據"""
    try:
        url = f'https://ws.api.cnyes.com/ws/api/v1/charting/history?resolution=D&symbol=TWS:{stock_no}:STOCK&from=1728000015&to=1728000000'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content = response.json()
        
        data = {
            'open': content['data']['o'],
            'high': content['data']['h'],
            'low': content['data']['l'],
            'close': content['data']['c'],
            'volume': content['data']['v']
        }
        df = pd.DataFrame(data=data)
        df_reversed = df.iloc[::-1]
        return df_reversed.tail(1)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching historical data for {stock_no}: {str(e)}")
        return None

def get_stock_data(ticker='2330'):
    """獲取股票歷史數據"""
    try:
        to_date = dt.date.today()
        from_date = to_date - dt.timedelta(days=365)
        
        # 從Fugle API獲取歷史K線資料
        s = client.stock.historical.candles(
            symbol=ticker,
            from_=from_date.strftime('%Y-%m-%d'),
            to=to_date.strftime('%Y-%m-%d'),
            fields="open,high,low,close,volume,change"
        )
        
        stock_data = s['data']
        df = pd.DataFrame(stock_data)
        
        # 處理數據格式
        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Volume'] = df['Volume'] / 1000
        
        # 將日期轉換為字串格式
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        df = df.sort_values(by='Date', ascending=True)

        # 加入今日數據
        last_row_data = get_historical_data(ticker)
        if last_row_data is not None:
            today_str = to_date.strftime('%Y-%m-%d')
            if df.iloc[-1]['Date'] != today_str:
                last_row_df = pd.DataFrame({
                    'Date': [today_str],
                    'Open': last_row_data['open'].values,
                    'High': last_row_data['high'].values,
                    'Low': last_row_data['low'].values,
                    'Close': last_row_data['close'].values,
                    'Volume': last_row_data['volume'].values
                })
                df = pd.concat([df, last_row_df], ignore_index=True)

        return {
            'status': 'success',
            'name': ticker,
            'data': df.to_dict(orient='records')
        }
        
    except Exception as e:
        logger.error(f"Error in get_stock_data for {ticker}: {str(e)}")
        return {
            'status': 'error',
            'name': ticker,
            'message': str(e),
            'data': []
        }

@app.route('/')
def serve_portfolio():
    """服務主頁面"""
    return app.send_static_file('portfolio.html')

@app.route('/api/stock_data')
def api_stock_data():
    """API端點處理股票數據請求"""
    ticker = request.args.get('ticker', '2330')
    try:
        result = get_stock_data(ticker)
        return jsonify(result)
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('../', path)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')