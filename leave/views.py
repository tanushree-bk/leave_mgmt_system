#views.py
from django.contrib.auth.views import LoginView as DefaultLoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView  # Make sure FormView is imported here
from django.shortcuts import render, redirect
from .models import LeaveApplication, LeaveBalance, Type_leave
from .forms import LeaveApplicationForm, ApplicationReviewForm, TypeLeaveForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Register View
class RegisterView(FormView):
    template_name = 'register.html'
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Custom Login View
class CustomLoginView(DefaultLoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('home')

# Logout View
class LogoutView(LogoutView):
    success_url = reverse_lazy('login')

# Home Page View (Login required)
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

# Application View (For creating leave applications - Login required)
class ApplicationView(LoginRequiredMixin, CreateView):
    model = LeaveApplication
    form_class = LeaveApplicationForm
    template_name = 'apply_leave.html'
    success_url = reverse_lazy('leave_status')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Leave Status View (Login required)
class LeaveStatusView(LoginRequiredMixin, TemplateView):
    template_name = 'leave_status.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = LeaveApplication.objects.filter(user=self.request.user)
        leave_balances = LeaveBalance.objects.filter(user=self.request.user)

        # Update leave balance for approved applications
        for application in applications:
            if application.status == 'Approved':
                leave_balance = leave_balances.filter(leave_type=application.leave_type).first()
                if leave_balance:
                    # Update remaining balance after approval
                    leave_balance.balance -= application.duration()
                    leave_balance.save()

        context['applications'] = applications
        context['leave_balances'] = leave_balances
        return context

# Type Leave Form View (Login required)
class TypeLeaveView(LoginRequiredMixin, FormView):
    template_name = "leave_type.html"
    form_class = TypeLeaveForm
    success_url = reverse_lazy('leave_type')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)