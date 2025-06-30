from django.http import HttpResponse

def bot_status(request):
    return HttpResponse('Телеграм-бот работает!')
