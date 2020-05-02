from django.shortcuts import render, redirect
from loaner_program.models import Technology, Kit

def index(request):
    return render(request, 'landing/landing.html', {'user': request.user})

def team(request):
    return render(request, 'landing/team.html', {'user': request.user})

def faq(request):
    return render(request, 'landing/faq.html', {'user': request.user})

def privacy_policy(request):
    return render(request, 'landing/privacy_policy.html', {'user': request.user})

def loaner_program(request):
    res = []
    technologies = Technology.objects.all()
    for tech in technologies:
        q = Kit.objects.filter(technology_id=tech.id)
        res.append({
            'name': tech.name,
            'quantity': len(q),
            'boards': 0 if len(q) == 0 else q[0].num_boards
        })
    return render(request, 'landing/loaner_program.html', {'user': request.user, 'inventory': res})

def volunteer_redirect(request):
    return redirect('https://goo.gl/forms/TOgxhucxMKVaPFqD3')

def events_redirect(request):
    return redirect('list-event')

def media_release_form_redirect(request):
    return redirect('https://goo.gl/forms/xl6wKPi10uQJSUJ82')

def inventory_form_redirect(request):
    return redirect('https://goo.gl/forms/VAFYcFb8w8wgSlzL2')

def student_feedback_form_redirect(request):
    return redirect('https://goo.gl/forms/vOd23wkQDfkUs7Ll1')

def teacher_pre_survey_redirect(request):
    return redirect('https://goo.gl/forms/gDBYkGJZpHAaEZeF2')

def teacher_check_in_1_redirect(request):
    return redirect('https://goo.gl/forms/smuSP47wdoFEBB5J2')

def teacher_check_in_2_redirect(request):
    return redirect('https://goo.gl/forms/yDHFSkGJdCugbnXB3')

def teacher_post_survey(request):
    return redirect('https://goo.gl/forms/HtfioFTHK8FDuClA2')
