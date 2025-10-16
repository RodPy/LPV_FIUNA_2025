from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import signup_view
from control.views import panel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('control/', include('control.urls')),
    path('', panel, name='panel'),
]
