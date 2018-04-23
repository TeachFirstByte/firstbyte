from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def me(request):
    return render(request, 'accounts/user_me.html', {'user': request.user})
