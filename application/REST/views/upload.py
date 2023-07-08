from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from sys import getsizeof



# @api_view(['GET'])
# def onLoad(request):
#     Response({}, status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def main(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)

    print("Received something")

    # if getsizeof(request.body) >= 1073741824: return Response(None, status=status.HTTP_)

    with open("tempFile.txt",'wb+') as f:
        f.write(request.body)

    return Response({'data': 'Complete'}, status=status.HTTP_200_OK)
