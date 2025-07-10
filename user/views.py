from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            messages.add_message(request,messages.SUCCESS,"Oturum Açıldı")
            return redirect("index")
        else:
            messages.add_message(request,messages.ERROR,"Kullanıcı Adı ya da Şifre Yanlış")
            return redirect("login")
    else:
        return render(request,"user/login.html")
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if password == repassword:
            if User.objects.filter(username=username):
                messages.add_message(request,messages.WARNING,"Bu kullaıcı adı daha önce alınmış")
                return redirect("register")
            else:
                if User.objects.filter(email=email):
                    messages.add_message(request,messages.WARNING,"Bu email daha önce alınmış")
                    return redirect("register")
                else:
                    user = User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    messages.add_message(request,messages.SUCCESS,"Kullanıcı Oluşturuldu")
                    return redirect("login")
        else:
            print("parolalar eşleşmiyor")
            return redirect("register")
        
        return redirect("/")
    return render(request,"user/register.html")
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS, "Başarıyla çıkış yapıldı")
    return redirect('index')
