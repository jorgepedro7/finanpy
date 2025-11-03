from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignupView, UserLoginView

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
