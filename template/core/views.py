from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')


def health(request):
    """Health check para o deploy: responde 200 se o banco estiver de pé."""
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    return JsonResponse({'status': 'ok'})
