from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django import forms
from sys import getsizeof
from REST.calc.video import VideoCensor
import os
import cv2
import tempfile


@api_view(['GET'])
def about(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def contact(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def index(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

@api_view(['POST','GET'])
def upload(request):
    if request.method == 'GET': return Response(None, status=status.HTTP_204_NO_CONTENT)

    print("Received something")

    upf = request.FILES['file']

    # if getsizeof(request.body) >= 1073741824: 
    #     return Response(
    #         {
    #             'Upload Status': 'Complete', 
    #             'Error': "File size is too large. Max size is 1GB."
    #         }, 
    #         status=status.HTTP_422_UNPROCESSABLE_ENTITY
    #     )

    file_src = os.path.join(tempfile._get_default_tempdir(), str(next(tempfile._get_candidate_names()))+'.avi')
    with open(file_src, 'wb+') as f:
        for chunk in upf.chunks():
            f.write(chunk)
    print(file_src)
    print(getsizeof(file_src))

    cap = cv2.VideoCapture(file_src, cv2.CAP_FFMPEG)
    print(cap.isOpened())
    censorer = VideoCensor()
    file = censorer.calc_image(cap)
    with open(file, 'rb') as f:
        byte = f.read()
    print(len(byte))
    print('responded')
    res = HttpResponse(byte, status=status.HTTP_200_OK, content_type='application/octet-stream')
    res['Content-Disposition'] = 'attachment; filename="video.mp4"'  # Set the desired filename
    return res
