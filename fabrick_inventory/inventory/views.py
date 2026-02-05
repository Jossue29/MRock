from django.http import JsonResponse
from .models import GlobalInventory
from django.shortcuts import render

def test_inventory(request):
    data = list(
        GlobalInventory.objects.all().values()[:10]
    )
    return JsonResponse(data, safe=False)

def inventory_list(request):
    inventory = GlobalInventory.objects.all()[:100]
    return render(request, 'inventory/list.html', {
        'inventory': inventory
    })