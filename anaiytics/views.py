from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order
from django.db.models import Sum, Count
from datetime import datetime

@staff_member_required
def daily_report(request):
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = datetime.today().date()
    else:
        selected_date = datetime.today().date()

    orders = Order.objects.filter(created_at__date=selected_date)
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(request, 'analytics/report.html', {
        'selected_date': selected_date,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
    })
