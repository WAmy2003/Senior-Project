from django.urls import path
from . import views
from .views import StockDataView

urlpatterns = [
    path('api/stock-data/', StockDataView.as_view(), name='stock-data'),
    path('api/portfolio-weights/', views.get_portfolio_weights, name='portfolio-weights'),
]