from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view, name='registration'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_view,
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view,
         name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view,
         name='password_reset_complete'),
]
