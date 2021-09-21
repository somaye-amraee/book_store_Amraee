"""
import here
"""
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import UpdateView, CreateView, DetailView
from sqlparse.compat import text_type
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, AddressForm
from .decorators import allowed_users,admin_only,unauthenticated_user
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from  django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import views as auth_views



"""
global scope
"""



class EmailToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.id)+text_type(timestamp))

email_generator=EmailToken()


"""
a view for signing up users and adding them the customer access level by default
"""
@unauthenticated_user
def user_register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # clean
            data = form.cleaned_data
            group = Group.objects.get(name='customer')
            user = CustomUser.objects._create_user(username=data['username'], email=data['email'],
                                     first_name=data['first_name'],
                                     last_name=data['last_name'],
                                     password=data['password2'])

            user.groups.add(group)
            user.is_active = False
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            url = reverse('active', kwargs={'uidb64': uidb64, 'token': email_generator.make_token(user)})
            link = 'http://' + domain + url
            user.save()
            email = EmailMessage(
                'active user',
                link,
                'test<samraee1@gmail.com>',
                [data['email']],
            )
            email.send(fail_silently=False)
            messages.warning(request, 'کاربر محترم لطفا برای فعالسازی به ایمیل خود مراجعه کنید', 'warning')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'register.html', context )



class RegisterEmail(View):
    def get(self,request,uidb64,token):
        id= force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=id)
        if user and email_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('login')


"""
for loging users
"""

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, username=CustomUser.objects.get(email=data['user']),
                                    password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'به فروشگاه کتاب  خوش آمدید', 'primary')
                return redirect('home')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور شتباه است', 'danger')

    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})



"""
خارج شدن یوزر
"""
def user_logout(request):
    logout(request)
    messages.success(request,'با موفقیت خارج شدید', 'warning')
    return redirect('home')
#--------------------------------------------------------------


@login_required(login_url='login')
def user_profile(request):
    profile = Profile.objects.get(user_id = request.user.id)
    return render(request, 'profile.html', {'profile':profile})



class UpdateProfile(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'update.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return Profile.objects.all()


# ///////////////////////

def AddressCreateView(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            user = request.user
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            street_2 = form.cleaned_data['street_2']
            postal_code = form.cleaned_data['postal_code']
            address = Address(user=user,country=country,state=state,city=city,street=street,
                              street_2=street_2,postal_code=postal_code)
            address.save()
    else:
        form = AddressForm()
    context={'form':form}
    return render(request, 'address_new.html',  context)

#



# from django.contrib.auth.mixins import LoginRequiredMixin
#
# class AddressCreateView(LoginRequiredMixin,CreateView):
#     model = Address
#     template_name = 'address_new.html'
#     fields = ['country', 'state', 'city', 'street', 'street_2','postal_code']
#     success_url = reverse_lazy('profile')


class UpdateAddress(UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'update.html'
    success_url = reverse_lazy('profile')


class AddressDeleteView(CreateView):
    model = Address
    template_name = 'address_delete.html'
    success_url = reverse_lazy('profile')
#
#
# def list_address(request):
#     users=request.user
#     address=Address.objects.filter(u)
#     context={}
#     return render(request, 'address_list.html', context)


def list_address(request):
    address= Address.objects.filter(user=request.user
                                 )

    return render(request,'address_list.html',{'address':address})

class AddressDetailView(DetailView):
    model = Address
    template_name = 'address_detail.html'


"""
change password phases
"""

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        # صحت اطلاعات چک میکنیم که مخرب نباشن
        if form.is_valid():
            form.save()
            # با استفاده از form.user
            # session قبلی حدف می شود و session  جدید می گیرد
            update_session_auth_hash(request, form.user)
            messages.success(request, 'پسورد با موفقیت تغییر کرد', 'success')
            return redirect('profile')
        else:
            messages.error(request,'پسورد اشتباه وارد شده است', 'danger')
            return redirect('change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'change.html', {'form':form})
# ///////////////////////////////////////////////////



"""
forget password phases
"""

class ResetPassword (auth_views.PasswordResetView):
    template_name = 'reset.html'
    success_url = reverse_lazy('reset_done')
    email_template_name = 'link.html'


class ResetDonePassword(auth_views.PasswordResetDoneView):
    template_name = 'done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'confirm.html'
    success_url = reverse_lazy('complete')


class Complete(auth_views.PasswordResetCompleteView):
    template_name = 'complete.html'
