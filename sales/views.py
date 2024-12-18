from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from sales.models import Order, Category,Platform
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.db.models import Sum, F, Q, Count
from sales.serializers import CategorySerialier,PlatformSerializer
import sys, os
from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .utils import PlainExcelGenerator

from django.core.cache import cache
from .rate_limiter import rate_limit
import redis
r = redis.Redis()




def index(request):
    return render(request, 'index.html')

def sumary(request):
    return render(request, 'summary.html')


class PublishNotification(APIView):
    def post(self , request):
        message = request.data.get('message', "no message")
        r.publish("notifications",message)
        return Response({"message" : "Notification sent"})


class LeaderBoardAPI(APIView):
    def get(self , request):
        top_users = r.zrevrange("leaderboard", 0, 4, withscores=True)
        return Response({"top_users" : top_users})

    def post(self , request):
        user = request.data.get('user')
        score = request.data.get('score', 0)
        r.zadd("leaderboard", {user: score})
        return Response({"message" : "Score addded"})




class DownloadSalesDataAPI(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            data = [
                {
                    "order_id": order.order_id,
                    "product": order.product.product_name,
                    "customer": order.customer.customer_name,
                    "quantity_sold": order.quantity_sold,
                    "selling_price": order.selling_price,
                    "total_sale_value": order.total_sale_value,
                    "date_of_sale": order.date_of_sale,
                    "prime_delivery": order.prime_delivery,
                    "warehouse_location": order.warehouse_location,
                    "reseller_name": order.reseller_name,
                    "commission_percentage": order.commission_percentage,
                    "coupon_used": order.coupon_used,
                    "return_window": order.return_window,
                    "platform": order.platform,
                }
                for order in orders
            ]
            excel = PlainExcelGenerator(data, "Sales-Data")
            _status , file_url = excel.generateExcel()

            return Response({
                "status" : True,
                "file_url" : file_url
            })

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno,e)

            return Response({})



class SalesDataAPI(APIView):
    """
    API to fetch monthly sales volume (Quantity Sold) with filters.
    """


    @rate_limit(max_requests=5, time_window=60)
    def get(self, request):
        try:
            cache_key = 'sales-data'
            if cache.get(cache_key):
                return Response(cache.get(cache_key))

            orders = Order.objects.all()

            monthly_sales = orders.annotate(
                month_of_sale=TruncMonth('date_of_sale')  # Truncate to month
            ).values(
                'month_of_sale'
            ).annotate(
                total_quantity_sold=Sum('quantity_sold')
            ).order_by('month_of_sale')

            # Format the response as per your requirement
            result = []
            for sale in monthly_sales:
                month_name = sale['month_of_sale'].strftime('%b,%Y')  # Get the month and year in desired format
                result.append({
                    'month_of_sale': month_name,
                    'total_quantity_sold': sale['total_quantity_sold']
                })



            category_data = CategorySerialier(Category.objects.all().order_by('name'), many = True)
            platform_data = PlatformSerializer(Platform.objects.all(), many = True)
            data = {
                "sales_data" : result,
                "category_data" : category_data.data,
                "platform_data" : platform_data.data
            }

            cache.set(cache_key,data, timeout=60 * 5)
            return Response(data)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno,e)

            return Response({})








class SummaryMetricsAPI(APIView):
    """
    API to fetch summary metrics.
    """

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
      
        total_revenue = orders.aggregate(
            total_revenue=Sum(F('quantity_sold') * F('selling_price'))
        )['total_revenue'] or 0

        # Calculate total orders
        total_orders = orders.count()

        # Calculate total products sold (sum of quantity_sold)
        total_products_sold = orders.aggregate(
            total_products_sold=Sum('quantity_sold')
        )['total_products_sold'] or 0

        # Calculate canceled orders and the canceled order percentage
        canceled_orders = orders.filter(order_delivery__delivery_status="Cancelled").count()
        canceled_order_percentage = (canceled_orders / total_orders) * 100 if total_orders > 0 else 0

        # Prepare the response data
        summary_data = {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_products_sold': total_products_sold,
            'canceled_order_percentage': canceled_order_percentage
        }

        monthly_revenue = orders.annotate(
            month_of_sale=TruncMonth('date_of_sale')
        ).values('month_of_sale').annotate(
            total_monthly_revenue=Sum(F('quantity_sold') * F('selling_price'))
        ).order_by('month_of_sale')

        # Format the monthly revenue data to return in the response
        monthly_revenue_data = [
            {
                "month_of_sale": month['month_of_sale'].strftime('%b,%Y'),
                "total_revenue": month['total_monthly_revenue']
            }
            for month in monthly_revenue
        ]

        # Return both summary metrics and monthly revenue data
        category_data = CategorySerialier(Category.objects.all().order_by('name'), many = True)
        platform_data = PlatformSerializer(Platform.objects.all(), many = True)
        return Response({
            'summary_metrics': summary_data,
            'monthly_revenue': monthly_revenue_data,
            "category_data" : category_data.data,
            "platform_data" : platform_data.data
        })