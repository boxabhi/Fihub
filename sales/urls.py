from django.urls import path
from .views import LeaderBoardAPI,SummaryMetricsAPI,SalesDataAPI,DownloadSalesDataAPI,PublishNotification

urlpatterns = [

    path('leaderboard/', LeaderBoardAPI.as_view()),
    
    path('sales-data/', SalesDataAPI.as_view(), name='sales-data'),
    path('download/sales-data/', DownloadSalesDataAPI.as_view(), name='sales-data'),

    path('summary-metrics/', SummaryMetricsAPI.as_view(), name='summary-metrics'),
]
