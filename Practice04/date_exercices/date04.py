from datetime import datetime

print("Input first date (YYYY-MM-DD HH:MM:SS):")
d1_str = input()

print("Input second date (YYYY-MM-DD HH:MM:SS):")
d2_str = input()

d1 = datetime.strptime(d1_str, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(d2_str, "%Y-%m-%d %H:%M:%S")

diff = d2 - d1

seconds = diff.total_seconds()

print("Seconds:", int(abs(seconds)))