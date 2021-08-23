from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# from .forms import LoginForm, RegisterForm


# Create your views here.
# def login_user(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#
#     login_form = LoginForm(request.POST or None)
#     if login_form.is_valid():
#         user_name = login_form.cleaned_data.get('user_name')
#         password = login_form.cleaned_data.get('password')
#         user = authenticate(request, username=user_name, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/')
#         else:
#             login_form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')
#
#     context = {
#         'login_form': login_form
#     }
#     return render(request, 'account/login.html', context)
#
#
# def register(request):
#     if request.user.is_authenticated:
#         return redirect('/')
#     register_form = RegisterForm(request.POST or None)
#
#     if register_form.is_valid():
#         user_name = register_form.cleaned_data.get('user_name')
#         password = register_form.cleaned_data.get('password')
#         email = register_form.cleaned_data.get('email')
#         User.objects.create_user(username=user_name, email=email, password=password)
#         return redirect('/login')
#
#     context = {
#         'register_form': register_form
#     }
#     return render(request, 'account/signup.html', context)
#
#
# def log_out(request):
#     logout(request)
#     return redirect('/login')
from django.views import View

from accounts.models import CustomUser


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = CustomUser.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('homepage')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        username = postData.get ('username')
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'username':username,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
            'password':password,
        }
        error_message = None

        customer =CustomUser (username=username,
                            first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (username,first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
