from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *


urlpatterns = [
    path('upload_images/', upload_images, name="images"),
    path('upload_under_images/', upload_under_images, name="under_images"),
    path('edit_images/', edit_images, name="edit_images"),
    path('deleteTask/', views.deleteTask, name='deleteTask'),
    path('deleteTaskUnder/', views.deleteTaskUnder, name='deleteTaskUnder'),
    path('redactTask/', views.redactTask, name='redactTask'),
    path('redactTaskUnder/', views.redactTaskUnder, name='redactTaskUnder'),
    # path('redactTask', views.ImageUpdateView.as_view(), name='redactTask'),
    path('checkTask/', views.checkTask, name='checkTask'),
    path('checkTaskUnder/', views.checkTaskUnder, name='checkTaskUnder'),
    path('', gallery, name="gallery"),
    path('image/<part>/', oneimage, name="oneimage"),
    path('done/', gallery_done, name="gallery_done"),
    path('todo/', gallery_todo, name="gallery_todo"),
#    path('login/', views.user_login, name='login'),
#     path('account/', include('django.contrib.auth.urls')),
    path('files', include('django.contrib.auth.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
# reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]