from django.shortcuts import render, redirect
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Акквунт создан')
            return redirect('login')
        else: messages.error(request, 'Ошибки в форме')
    else:
        form = RegisterForm()
    context = {
        'form': form,
        'page_title': 'Регистрацтя'
    }
    return render(request, 'userAcc/register.html', context)