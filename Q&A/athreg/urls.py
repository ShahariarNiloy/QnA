from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('',views.home, name="home"),

    path('register/',views.registerPage, name="register"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('detail/<int:id>',views.detail,name='detail'),
    path('save-comment',views.save_comment,name='save-comment'),
    path('save-upvote',views.save_upvote,name='save-upvote'),
    path('save-downvote',views.save_downvote,name='save-downvote'),
    path('ask-question',views.ask_form,name='ask-question'),
    path('tag/<str:tag>',views.tag,name='tag'),
    path('tags/',views.tags,name='tags'),

    path('profile/',views.profile,name='profile'),
    path('profileinfo/',views.profileinfo,name='profileinfo'),
    path('otheruser/<str:name>',views.otheruser,name='otheruser'),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),

]