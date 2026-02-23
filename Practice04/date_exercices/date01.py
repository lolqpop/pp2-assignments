from datetime import date, timedelta

today = date.today()
sub = today - timedelta(days=5)

print(today)
print(sub)