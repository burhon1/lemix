import calendar
calendar_obj = calendar.Calendar()

DAYS = [
    "Dushanba",
    "Seshanba",
    "Chorshanba",
    "Payshanba",
    "Juma",
    "Shanba",
    "Yakshanba",
    ]

def week_dates(year: int, month: int):
    counter = 0
    data = list()
    for i in calendar_obj.itermonthdates(2022,12):
        data.append(
            dict((('day', DAYS[counter%7]), ('date', i)))
        )
        counter += 1

    weeks = list()
    for i in range(len(data)//7):
        weeks.append(data[7*i:7*(i+1)])
    try:
        return weeks
    except:
        return []