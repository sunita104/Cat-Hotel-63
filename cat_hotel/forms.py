from django import forms
from cat_hotel.models import *
from cat_hotel_admin.models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserChangeForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ชื่อผู้ใช้', max_length=150)
    password = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='fist Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2',]

class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )
        labels = {
            'username' : 'ชื่อผู้ใช้',
        }

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='รหัสผ่านเดิม', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='รหัสผ่านใหม่', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='ยืนยันรหัสผ่านใหม่', widget=forms.PasswordInput)


class BookingForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='วันที่เข้าฝาก')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='ถึงวันที่')

    class Meta:
        model = Booking
        fields = ['customer','room', 'start_date', 'end_date', 'cat_name', 'phone_number']
        labels = {
            'room': 'ห้อง',
            'cat_name': 'ชื่อแมว',
            'phone_number': 'เบอร์ติดต่อ',
            'total_price': 'ราคารวม',
        }


class SearchForm(forms.Form):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='วันที่เข้าฝาก')
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'format': 'yyyy-mm-dd'}), label='ถึงวันที่')