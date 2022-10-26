
from datetime import date,datetime

import calendar
import numpy as np
calendar.setfirstweekday(6)

def get_week_of_month(year, month, day):
    x = np.array(calendar.monthcalendar(year, month))
    week_of_month = np.where(x==day)[0][0] + 1
    return(week_of_month)



def get_days(start_date,finis_date=None,days=[1,3,5]):
    data = calendar.monthcalendar(finis_date.year,finis_date.month) 
    datas = []
    formas = {
        1:1,
        2:2,
        3:3,
        4:4,
        5:5,
        6:6,
        7:0
    }
    if finis_date and start_date and finis_date.year==start_date.year and finis_date.month==start_date.month:
        for week in data:
            for day in days:
                day = int(day)
                if week[day] != 0 and start_date.day<=week[day]:
                    datas.append(datetime(finis_date.year, finis_date.month, week[day]).strftime('%Y-%m-%d'))  
        return datas
    for week in data:
        for day in days:
            day = formas[int(day)]
            if week[day] != 0:
                datas.append(datetime.strptime(f'{finis_date.year}-{finis_date.month}-{week[day]}', "%Y-%m-%d"))  
    return datas 

def get_attendace_days(start_date,finis_date=None,days=[1,3,5]):
    data = calendar.monthcalendar(finis_date.year,finis_date.month) 
    datas = []
    print(finis_date)
    if finis_date.year==start_date.year and finis_date.month==start_date.month:
        for week in data:
            for day in days:
                day = int(day)
                if week[day-1] != 0 and start_date.day<=week[day-1]:
                    datas.append(datetime(finis_date.year, finis_date.month, week[day]).strftime('%Y-%m-%d'))  
        return datas
    for week in data:
        for day in days:
            day = int(day)
            if week[day-1] != 0:
                datas.append(datetime.strptime(f'{finis_date.year}-{finis_date.month}-{week[day-1]}', "%Y-%m-%d"))  
    return datas  

def get_month(start_date,end_date):
    months = []
    objs = {
        '1':'Yanvar',
        '2':'Fevral',
        '3':'Mart',
        '4':'Aprel',
        '5':'May',
        '6':'Iyun',
        '7':'Iyul',
        '8':'Avgust',
        '9':'Sentabr',
        '10':'Oktabr',
        '11':'Noyabr',
        '12':'Dekabr',
    }
    for y in range(start_date.year, end_date.year+1):
        for m in range(start_date.month, end_date.month+1):
            # if (y == start_date.year) and m < 8:
            #     continue
            # if (y == end_date.year+1) and m > 2:
            #     continue
            months.append({'key':f'{start_date.year}-{m}','value':objs[str(m)]})     
    return {
        'current':objs[str(end_date.month)],
        'old':months
    }          
    # while d.year < 2023: 
    #     dat=get_week_of_month(date.year,date.month,date.day)
    #     print(dat)
    #     if str(dat)=="Fri":                          # This will go *through* 2012
    #         print((d).strftime('%a, %d %b %Y'))
    #     elif dat=="Mon":
    #         print((d+datetime.timedelta(days=1)).strftime('%a, %d %b %Y'))
    #     d += datetime.timedelta(days=7) 
