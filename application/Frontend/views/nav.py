from django.shortcuts import render

def index(response):
    return render(response, "index.html")

def home(response):
    return render(response, "home.html")