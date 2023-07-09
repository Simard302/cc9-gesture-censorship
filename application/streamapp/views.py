from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def stream_view(request):
    return HttpResponse('<html><body><script src="/static/js/StreamScript.js"></script></body></html>')
