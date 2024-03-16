from django.urls import  path
import utils.views as views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
  path('refresh-token',TokenRefreshView.as_view()),
  path('register', views.RegisterView.as_view()),
  path('login', views.LoginView.as_view()),
  # path('logout', views.LogoutView.as_view()),
]