from django import forms
from cat_hotel.models import *
from datetime import datetime



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









