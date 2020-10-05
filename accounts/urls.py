from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.login_view),
    path('register/',views.register_view,name="register_view"),
    path('verify-otp/',views.verify,name="verify_otp")
]