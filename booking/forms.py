from django import forms
from .models import Booking, Showtime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seats']
        
    def __init__(self, *args, **kwargs):
        showtime = kwargs.pop('showtime', None)
        super(BookingForm, self).__init__(*args, **kwargs)
        if showtime:
            self.fields['seats'].queryset = showtime.seats.filter(is_available=True)