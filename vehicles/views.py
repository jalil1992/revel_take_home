from django.http import JsonResponse

from vehicles.data import data

# Create your views here.
def list_vehicles(request):
    return JsonResponse(data, safe=False)
