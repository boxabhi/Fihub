from django.urls import path
from .views import SummaryMetricsAPI,SalesDataAPI,DownloadSalesDataAPI

urlpatterns = [
    
    path('sales-data/', SalesDataAPI.as_view(), name='sales-data'),
    path('download/sales-data/', DownloadSalesDataAPI.as_view(), name='sales-data'),

    path('summary-metrics/', SummaryMetricsAPI.as_view(), name='summary-metrics'),
]
