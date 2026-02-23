from datetime import datetime

now = datetime.now()
clean = now.replace(microsecond=0)

print(clean)