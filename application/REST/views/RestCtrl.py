from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import FileResponse
from sys import getsizeof

@api_view(['GET'])
def about(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def contact(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def index(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST','GET'])
def upload(request):
    if request.method == 'GET': 
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    print("Received something")

    if getsizeof(request.body) >= 1073741824: 
        return Response(
            {
                'Upload Status': 'Complete', 
                'Error': "File size is too large. Max size is 1GB."
            }, 
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    with open("tempFile.mp4",'wb+') as f:
        f.write(request.body)
    
    return Response({'Upload Status': 'Complete'}, status=status.HTTP_200_OK)

@api_view(["GET"])
def uploadResponse(request):
    with open("tempFile.mp4", 'rb+') as f:
        print("This is what I'm sending back:")
        print(bool(f.read()))
    return FileResponse(open("tempFile.mp4", 'rb+'), content_type="video/mp4")