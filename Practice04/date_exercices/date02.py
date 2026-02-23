from datetime import date, timedelta

today = date.today()

tomorrow = today + timedelta(days=1)
yesterday = today - timedelta(days=1)

print(yesterday)
print(today)
print(tomorrow)