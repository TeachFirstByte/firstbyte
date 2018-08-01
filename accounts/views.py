import hashlib

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect


@login_required()
def me(request):
    return redirect('user-detail', pk=request.user.id)

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.profile.hide_profile and request.user != user:
        # Not authenticated
        return HttpResponseForbidden('Not allowed')

    email_clean = user.email.strip().lower()
    email_hash = hashlib.md5(email_clean.encode('utf-8')).hexdigest()
    return render(request, 'account/user_detail.html',
                  {'user': user, 'email_hash': email_hash})


def user_display(user):
    return user.first_name or user.username
