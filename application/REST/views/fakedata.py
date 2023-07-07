from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def fake_data(request):
    return Response({'data': 'test'}, status=status.HTTP_200_OK)