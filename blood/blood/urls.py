from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about-us/', views.about_us, name='about_us'),
    path('article/', views.article_detail, name='article_detail'),
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
