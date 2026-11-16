from django.urls import path
from calory import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('login/', views.userlogin, name='userlogin'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.bmr, name='bmr'),
    path('add-calorie/', views.addCalorie, name='addCalorie'),
    path('profile/', views.userInfo, name='userInfo'),
    path('profile/edit/', views.editUserInfo, name='editUserInfo'),
    path('history/', views.calorieInfo, name='calorieInfo'),
]
