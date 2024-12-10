from django.urls import path
from . import views
from .views import StockDataView, calculate_portfolio_profit_loss

urlpatterns = [
    path('', views.main_view, name='main'),
    path('portfolio.html', views.portfolio_view, name='portfolio'),
    path('analysis.html', views.analysis_view, name='analysis'),
    path('aboutus.html', views.aboutus_view, name='aboutus'),
    path('api/stock-data/', StockDataView.as_view(), name='stock-data'),
    path('api/portfolio-weights/', views.get_portfolio_weights, name='portfolio-weights'),
    path('api/get_available_dates/', views.get_available_dates, name='get_available_dates'),
    path('api/get_available_data/<str:date>', views.get_available_data, name='get_available_data'),
    path('api/chart-data/', views.get_chart_data, name='get_chart_data'),
    path('api/smartpick-weights/', views.get_smartpick_weights, name='smartpick-weights'),
    path('api/0050-weights/', views.get_0050_weights, name='0050-weights'),
    path("api/portfolio-profit-loss/", calculate_portfolio_profit_loss, name="portfolio-profit-loss"),
]