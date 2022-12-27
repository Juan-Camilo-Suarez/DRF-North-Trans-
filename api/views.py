from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import ApplicationsTransport, ApplicationRegister
from api.serializers import (
    ApplicationsTransportSerializer,
    ApplicationsRegisterSerializer,
)


# Create your views here.


@api_view()
def main_api(request):
    return JsonResponse({"status": "ok"})


@api_view()
def application_register_list(request):
    applications_register = ApplicationRegister.objects.all()
    serializer = ApplicationsRegisterSerializer(applications_register, many=True)
    return Response(serializer.data)


@api_view()
def application_transport_list(request):
    applications_transport = ApplicationsTransport.objects.all()
    serializer = ApplicationsTransportSerializer(applications_transport, many=True)
    return Response(serializer.data)


@api_view()
def application_transport(request, id):
    applications_transport = get_object_or_404(
        ApplicationsTransport.objects.all(), id=id
    )
    serializer = ApplicationsTransportSerializer(applications_transport)
    return Response(serializer.data)
