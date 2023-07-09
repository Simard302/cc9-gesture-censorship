from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view



@api_view(['POST','GET'])
def stream(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)

    print("Received something")

    return Response({'Upload Status': 'Complete'}, status=status.HTTP_200_OK)
