import datetime

date = datetime.date.today()
timedate = datetime.datetime.utcfromtimestamp(1659970800)
print(str(datetime.datetime.utcfromtimestamp(1659970800).date()))
print(date > timedate.date())
