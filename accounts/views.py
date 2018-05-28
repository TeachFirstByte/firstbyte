import hashlib

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def me(request):
    email_clean = request.user.email.strip().lower()
    email_hash = hashlib.md5(email_clean.encode('utf-8')).hexdigest()
    return render(request, 'account/user_detail.html',
                  {'user': request.user, 'email_hash': email_hash})


def user_display(user):
    return user.first_name or user.username
