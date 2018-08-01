from django.shortcuts import render

def index(request):
    return render(request, 'landing/landing.html', {'user': request.user})

def faq(request):
    return render(request, 'landing/faq.html', {'user': request.user})

def privacy_policy(request):
    return render(request, 'landing/privacy_policy.html', {'user': request.user})
