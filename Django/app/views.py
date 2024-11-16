import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import HistoricalReturn

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
