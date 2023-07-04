from datetime import datetime, timedelta
from calendar import HTMLCalendar
from cat_hotel_admin.models import *
from cat_hotel.models import *

'''
class Calendar(HTMLCalendar): # ใช้ html calendar ที่มีอยู่ในโมดูล calendar python
    def __init__(self, year=None, month=None): # กำหนด year, month จากพารามิเตอร์ี่รับเข้ามา
	    self.year = year
	    self.month = month
	    super(Calendar, self).__init__() # เรียก constructor ของ super class
    
    def formatday(self, day,end_date, events):
        events_per_day = events.filter(start_date__day=day,end_date__day=end_date) # ตรงนี้ คือ กรอกข้อมูลนัดหมายว่าเป็นวันไหน
        d = ''
        end_date = ''

        for event in events_per_day:
            d += f'<li> {event.room} </li>' # มาจัดให้เป็น html unordered list และส่งคืน html string
            end_date += f'<li> {event.room} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul class='day-ul'> {d} </ul></td>"
        return '<td></td>' # ตรงนี้ที่ทำให้เห็น list นัดหมายในแต่ละวัน
    
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events) # เมื่อวนลูปผ่านทุกวันในสัปดาห์ จะเรียกใช้ formatday() สำหรับแต่ละวัน และรวม html string และ return ออกไป
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True): # สร้างแบบฟอร์มปฏิทินของเดือนและปีที่กำหนดโดยผู้ใช้
        events = Booking.objects.filter(start_date__year=self.year, start_date__month=self.month) # filter ดึงข้อมูล Eventจากฐานข้อมูลโดยกรองด้วยปีและเดือนของปฏิทินที่กำลังสร้าง

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n' # HTML table ที่มีการกำหนด border, cellpadding, cellspacing และ class เพื่อให้เป็นตารางแบบปฏิทิน
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
  		# สร้างตารางแบบปฏิทิน ซึ่งจะมีข้อมูลของวันที่ และข้อมูลของเหตุการณ์ที่เกิดขึ้นในแต่ละวัน โดยข้อมูลเหตุการณ์ที่กำลังเก็บไว้ในตัวแปร events
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal
'''




        





    
    
	

