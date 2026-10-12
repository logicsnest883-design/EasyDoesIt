from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('resume_list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = AuthenticationForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.update({
                'class': 'w-full border rounded-lg px-3 py-2'
            })
        return form

    def get_success_url(self):
        return super().get_success_url()


def logout_view(request):
    logout(request)
    return redirect('home')