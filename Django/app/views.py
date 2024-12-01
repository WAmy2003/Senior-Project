import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db import connection
from django.shortcuts import render
from .models import HistoricalReturn
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fugle_marketdata import RestClient
import datetime as dt

def main_view(request):
    return render(request, 'main.html')

def portfolio_view(request):
    return render(request, 'portfolio.html')

def analysis_view(request):
    return render(request, 'analysis.html')

def aboutus_view(request):
    return render(request, 'aboutus.html')

# 禁用 CSRF 驗證以允許 API 測試
@csrf_exempt
def historical_return_list_create(request):
    if request.method == "GET":
        # 取得所有 HistoricalReturn 資料
        historical_returns = HistoricalReturn.objects.all().values(
            "date", "market_historical_return", "portfolio_historical_return"
        )
        data = list(historical_returns)
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        # 新增一筆 HistoricalReturn 資料
        try:
            body = json.loads(request.body.decode("utf-8"))
            date = body["date"]
            market_historical_return = body["market_historical_return"]
            portfolio_historical_return = body["portfolio_historical_return"]

            # 建立新的資料
            historical_return = HistoricalReturn.objects.create(
                date=date,
                market_historical_return=market_historical_return,
                portfolio_historical_return=portfolio_historical_return,
            )
            return JsonResponse(
                {
                    "message": "HistoricalReturn created successfully",
                    "data": {
                        "date": historical_return.date,
                        "market_historical_return": historical_return.market_historical_return,
                        "portfolio_historical_return": historical_return.portfolio_historical_return,
                    },
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def historical_return_detail(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
        date = body["date"]
        # 取得指定日期的 HistoricalReturn 資料
        historical_return = HistoricalReturn.objects.get(date=date)

        if request.method == "GET":
            # 回傳資料
            return JsonResponse(
                {
                    "date": historical_return.date,
                    "market_historical_return": historical_return.market_historical_return,
                    "portfolio_historical_return": historical_return.portfolio_historical_return,
                }
            )

        elif request.method == "PUT":
            # 更新指定日期的資料
            body = json.loads(request.body.decode("utf-8"))
            historical_return.market_historical_return = body.get(
                "market_historical_return", historical_return.market_historical_return
            )
            historical_return.portfolio_historical_return = body.get(
                "portfolio_historical_return", historical_return.portfolio_historical_return
            )
            historical_return.save()

            return JsonResponse(
                {
                    "message": "HistoricalReturn updated successfully",
                    "data": {
                        "date": historical_return.date,
                        "market_historical_return": historical_return.market_historical_return,
                        "portfolio_historical_return": historical_return.portfolio_historical_return,
                    },
                }
            )

        elif request.method == "DELETE":
            # 刪除資料
            historical_return.delete()
            return JsonResponse({"message": "HistoricalReturn deleted successfully"}, status=204)

    except HistoricalReturn.DoesNotExist:
        return JsonResponse({"error": "HistoricalReturn not found"}, status=404)



class StockDataView(APIView):
    def get(self, request):
        try:
            # 獲取股票代碼參數
            stock_id = request.GET.get('stock_id', '2330')  # 預設值為2330
            
            # 設置日期範圍
            end_date = dt.date.today()
            start_date = end_date - dt.timedelta(days=365)
            
            # 初始化 Fugle client
            key = "Njg1M2VkY2ItZjQ2NC00M2VjLTk5NjMtODFlMjA3YzA2NzdlIDY3NGQ3ZTRmLWZkNDktNGVkNy1iMTkyLTUzZDk4ODY4YzkwMw"
            client = RestClient(api_key=key)
            stock = client.stock
            
            # 獲取股票數據
            data = stock.historical.candles(**{"symbol": stock_id, "from": start_date.strftime('%Y-%m-%d'), "to": end_date.strftime('%Y-%m-%d'), "fields": "open,high,low,close,volume,change"})
            
            return Response({
                'status': 'success',
                'data': data
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
def get_portfolio_weights(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT stock_id, stock_name, weights 
                FROM portfolio_weights 
                ORDER BY weights DESC
            """)
            rows = cursor.fetchall()
            
            # 將查詢結果轉換為所需格式
            portfolio_data = {
                'stock_ids': [row[0] for row in rows],
                'company_names': [row[1] for row in rows],
                'weights': [float(row[2]) for row in rows]
            }
            
            return JsonResponse({
                'status': 'success',
                'data': portfolio_data
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
    
def get_available_dates(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT date 
                FROM history_returns
                ORDER BY date DESC
            """)
            rows = cursor.fetchall()
            
            # 將日期數據轉換為列表
            dates = [row[0] for row in rows]
            
            return JsonResponse({
                'status': 'success',
                'data': dates
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
def get_available_data(request, date):
    try:
        # 驗證日期格式
        try:
            selected_date = dt.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid date format. Expected YYYY-MM-DD.'
            }, status=400)

        # 驗證股票代號是否存在
        stock_ids = request.GET.get('stock_ids')
        if not stock_ids:
            return JsonResponse({
                'status': 'error',
                'message': 'Stock IDs parameter is missing or empty.'
            }, status=400)

        stock_ids = stock_ids.split(',')  # 將字符串分割為列表
        if not stock_ids:
            return JsonResponse({
                'status': 'error',
                'message': 'No valid stock IDs provided.'
            }, status=400)

        # 模擬數據處理邏輯（替換為你的真實邏輯）
        stock_returns = {}
        for stock_id in stock_ids:
            # 假設邏輯返回的數據
            stock_returns[stock_id] = 0.5  # 模擬數據

        return JsonResponse({
            'status': 'success',
            'data': stock_returns
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)