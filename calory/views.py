from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .models import UserInfo, CalorieInfo, CustomUser
from .forms import RegistrationForm, LoginForm, CalorieInfoForm, UserInfoForm


def calculate_bmr(gender, age, height, weight):
    if gender and age is not None and height is not None and weight is not None:
        if gender.lower() == "male":
            return 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
        else:
            return 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    return None



@login_required
def bmr(request):
    today = timezone.localdate()
    daily_items = CalorieInfo.objects.filter(users=request.user, date=today)
   
    for i in daily_items:
        print(i.Item_Name)
        
    total_calorie = daily_items.aggregate(total=Sum('Calorie_Consumed'))['total'] or 0

    info = request.user.userinfo
    bmr_value = calculate_bmr(info.Gender, info.Age, info.Height, info.Weight)

    msg = ""
    none_msg = ""

    if bmr_value is not None:
        if bmr_value > total_calorie:
            msg = "Your calorie intake is below your BMR."
        elif bmr_value < total_calorie:
            msg = "Your calorie intake is above your BMR."
        else:
            msg = "Your calorie intake equals your BMR."
    else:
        none_msg = "Please input height, weight, age, and gender."

    request.user.userinfo.bmr = bmr_value
    request.user.userinfo.save()
   
    context = {
        'bmr': bmr_value,
        'msg': msg,
        'none_msg': none_msg,
        'total_calorie': total_calorie,
        'daily_items': daily_items,
    }
    return render(request, 'bmr.html', context)


@login_required
def userInfo(request):
    info = request.user.userinfo
    bmr_value = calculate_bmr(info.Gender, info.Age, info.Height, info.Weight)
    
    request.user.userinfo.bmr = bmr_value
    request.user.userinfo.save()
    return render(request, 'userInfo.html')


@login_required
def calorieInfo(request):
    total_calory = CalorieInfo.objects.filter(users=request.user).aggregate(
        total=Sum('Calorie_Consumed')
    )['total'] or 0
    
    context = {
        'total_calory': total_calory,
    }
    return render(request, 'calorieInfo.html', context)


@login_required
def editUserInfo(request):
    user = CustomUser.objects.get(id=request.user.id)
    userInfo_obj = user.userinfo  
    
    if request.method == "POST":
        form = UserInfoForm(request.POST, instance=userInfo_obj)
        if form.is_valid():
            form.save()
            return redirect('userInfo')
    else:
        form = UserInfoForm(instance=userInfo_obj)
    return render(request, 'editUserInfo.html', {'form': form}) 


@login_required
def addCalorie(request):
    if request.method == "POST":
        form = CalorieInfoForm(request.POST)
        if form.is_valid():
            calorieinfo = form.save(commit=False)
            calorieinfo.users = request.user
            calorieinfo.save()                
            return redirect('bmr')
    else:
        form = CalorieInfoForm()
    return render(request, 'addCalorie.html', {'form': form}) 


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])            
            user.save()
            
            userinfo = UserInfo(users=user)
            userinfo.save()
            
            calorieinfo = CalorieInfo(users=user)
            calorieinfo.save()
            
            return redirect('userlogin')
    else:
        form = RegistrationForm()
    return render(request, 'registrationform.html', {'form': form})


def userlogin(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
        
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('bmr')
    else:
        form = LoginForm()
    return render(request, 'loginForm.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('registration')
