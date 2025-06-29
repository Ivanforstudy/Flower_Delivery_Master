from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.timezone import now
import json

from .models import TelegramOrder


@csrf_exempt
@require_POST
def update_telegram_order_status(request):
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        new_status = data.get('status')

        if not order_id or not new_status:
            return JsonResponse({'error': 'order_id и status обязательны.'}, status=400)

        order = TelegramOrder.objects.filter(id=order_id).first()
        if not order:
            return JsonResponse({'error': 'Заказ не найден.'}, status=404)

        order.status = new_status
        order.save()

        return JsonResponse({'success': True, 'order_id': order.id, 'new_status': order.status})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректный JSON.'}, status=400)
