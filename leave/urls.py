#urls.py
from django.urls import path
from .views import CustomLoginView, HomePageView, RegisterView, LogoutView, ApplicationView, LeaveStatusView, TypeLeaveView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Use the custom LoginView
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', HomePageView.as_view(), name='home'),
    path('apply_leave/', ApplicationView.as_view(), name='apply_leave'),
    path('leave_status/', LeaveStatusView.as_view(), name='leave_status'),  # Using class-based view for leave status
    path('leave_type/', TypeLeaveView.as_view(), name='leave_type'),
]