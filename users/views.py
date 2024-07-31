from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterCustomerForm
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def register_customer(request):
    if request.method == "POST":
        print("Hello")
        form = RegisterCustomerForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            var = form.save()
            var.is_customer = True
            var.save()
            print("form got saved")
            messages.info(request, "Your account has been successfully registered. Please login to continue.")
            return redirect("login")
        else:
            messages.warning(request, "Something went wrong. Please check for inputs.")
            return redirect("register-customer")
    else:
        form = RegisterCustomerForm()
        context = {"form": form}
        return render(request, "users/register_customer.html", context)

#login user
@csrf_exempt

def login_user(request):
    if request.method == "POST":
        print("hello")
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        print(password)

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None and user.is_active:
            login(request, user)
            print("user is present")
            messages.info(request, "Login successful. Please enjoy your session.")
            return redirect('dashboard')
            # return render(request, "dashboard.html")
            # return redirect(reverse('dash:dashboard'))
            # return redirect(reverse('dashboard:dashboard'))

        else:
            messages.warning(request, "Something went wrong. Please check form input.")
            # return redirect("login/")
            return render(request, "users/login.html")
    else:
        return render(request, "users/login.html")
    
#logout

def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended. Please log in to continue')
    return redirect('login')