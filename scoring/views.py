from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer, ClientDetailSerializer

class ClientListView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

class ClientDetailView(APIView):
    def get(self, request, id):
        try:
            client = Client.objects.get(id=id)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data)

class ClientsToDoFollowUpView(APIView):
    def get(self, request):
        seven_days = timezone.now() - timedelta(days=7)
        clients = Client.objects.filter(messages__sent_at__lt=seven_days).distinct()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)


class ClientCreateView(APIView):
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            detail_serializer = ClientDetailSerializer(client)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)