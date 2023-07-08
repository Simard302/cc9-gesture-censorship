from django.shortcuts import render

def index(response):
    return render(response, "index.html")
def about(response):
    return render(response, "about.html")
def contact(response):
    return render(response, "contact.html")
def uploadPage(response):
    return render(response, "upload-page.html")