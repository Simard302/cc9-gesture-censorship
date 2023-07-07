from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def fake_data(request):
    return Response({'data': 'test'}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def my_data(request, mynum=None):
    data = {}

    data['name'] = request.GET.get('name')
    if request.method == 'POST':
        data['body'] = request.data
    
    if mynum is not None:
        data['path_param'] = mynum

    return Response({'data': data}, status=status.HTTP_200_OK)