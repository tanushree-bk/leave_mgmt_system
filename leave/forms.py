#forms.py
from django import forms
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        # Validate that start date is not after end date
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should not come before the start date.")
        return cleaned_data

class ApplicationReviewForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[
        (LeaveApplication.STATUS_APPROVED, "Approved"),
        (LeaveApplication.STATUS_REJECTED, "Rejected"),
    ], label="Action")
    
    class Meta:
        model = LeaveApplication
        fields = ['status']

class TypeLeaveForm(forms.ModelForm):
    class Meta:
        model = Type_leave
        fields = ['name', 'no_days']