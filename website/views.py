from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from myproject import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from .email_tokens import generate_token
from django.contrib.auth.decorators import login_required


from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy



# Create your views here.
@ login_required(login_url="/signin")
def HomePage(request):
    return render(request, "mainmenu/home.html")

def SignupPage(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist!! Please try some other username...")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to Education For All - Site Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Education For All..!!\nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address.\n\nThanking You\nShiv Kumar Mandal"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Education For All - Site Login!!"
        message2 = render_to_string('loginsystem/email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "loginsystem/signup.html")

def ActivatePage(request,uidb64,token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

def SigninPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return render(request, "mainmenu/home.html",{"fname":fname})
        else:
            messages.error(request, "Password No Match Plz Try Again...")
            return redirect('signin')
    
    return render(request, "loginsystem/signin.html")




class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'loginsystem/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'loginsystem/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'loginsystem/password_reset_complete.html'





def SignoutPage(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('signin')

@ login_required(login_url="/signin")
def ContactPage(request):
    return render(request, "mainmenu/contact.html")


@ login_required(login_url="/signin")
def AboutPage(request):
    return render(request, "mainmenu/about.html")

@ login_required(login_url="/signin")
def CoursePage(request):
    return render(request, "mainmenu/course.html")

@ login_required(login_url="/signin")
def Civil_Main_Page(request):
    return render(request, "course/civil/civil_main.html")

@ login_required(login_url="/signin")
def Electronic_Main_Page(request):
    return render(request, "course/electronic/electronic_main.html")

@ login_required(login_url="/signin")
def Info_Technology_Main_Page(request):
    return render(request, "course/info_technology/info_technology_main.html")