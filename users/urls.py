
from django.urls import path , include
from users.views import *
urlpatterns = [
    path('login/',sign_in,name='login'),
    path('register/',sign_up, name='register'),

]