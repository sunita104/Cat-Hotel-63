from django import forms
from cat_hotel.models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label='ชื่อผู้ใช้', max_length=150)
    password = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2',)


class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='วันที่เข้าฝาก')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='ถึงวันที่')

    class Meta:
        model = Booking
        fields = ['customer', 'room', 'start_date', 'end_date','cat_name', 'phone_number']
        labels = {
            'room' : 'ห้อง',
            'cat_name': 'ชื่อแมว',
            'phone_number': 'เบอร์ติดต่อ',
        }

class SearchForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='วันที่เข้าฝาก')
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='ถึงวันที่')









