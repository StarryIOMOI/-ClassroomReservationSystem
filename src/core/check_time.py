import datetime

now = datetime.datetime.now()

year = int(now.strftime("%Y"))
month = int(now.strftime("%m"))
day = int(now.strftime("%d"))
week = now.strftime("%A")

def now():
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time