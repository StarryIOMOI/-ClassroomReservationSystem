import datetime

now = datetime.datetime.now()

year_now = int(now.strftime("%Y"))
month_now = int(now.strftime("%m"))
day_now = int(now.strftime("%d"))
week_now = now.strftime("%A")

def now():
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

