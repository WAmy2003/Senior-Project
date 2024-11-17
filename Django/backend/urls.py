from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("create-historical-returns/", historical_return_list_create, name="create-historical-returns"),
    path("historical-returns/", historical_return_detail, name="historicalreturn-detail"),
    path('', include('app.urls')),
]