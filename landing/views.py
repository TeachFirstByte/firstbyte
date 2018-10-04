from django.shortcuts import render, redirect

def index(request):
    return render(request, 'landing/landing.html', {'user': request.user})

def faq(request):
    return render(request, 'landing/faq.html', {'user': request.user})

def privacy_policy(request):
    return render(request, 'landing/privacy_policy.html', {'user': request.user})

def loaner_program(request):
    return render(request, 'landing/loaner_program.html', {'user': request.user})

def get_involved(request):
    return render(request, 'landing/get_involved.html', {'user': request.user})

def volunteer_redirect(request):
    return redirect('https://goo.gl/forms/TOgxhucxMKVaPFqD3')
