from django.contrib.auth import login
from django.shortcuts import render
from users.forms import RegisterForm, LoginForm
from users.models import CustomUser

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("valid form")
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                error_message = 'Invalid email or password'
                return render(request, 'users/login.html', {'form':form, 'error_message':error_message})
            if user.check_password(password):
                request.session['user_id']=user.id
                return render(request, 'users/success_register.html')
            else:
                error_message = 'Invalid email or password'
                return render(request, 'users/login.html', {'form': form, 'error_message': error_message})
        else:
            return render(request, 'users/login.html', {'form': form})

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return render(request, 'users/success_register.html')
        else:
            return render(request, 'users/register.html', {'form': form})
