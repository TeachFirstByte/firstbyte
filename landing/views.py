from django.shortcuts import render

def index(request):
    return render(request, 'landing/landing.html', {'user': request.user})
