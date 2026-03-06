import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

prices = re.findall(r"\d+\s?\d*,\d{2}", text)

prices = [p.replace(" ", "") for p in prices]

products = re.findall(r"\d+\.\n(.+)", text)

datetime_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

date = None
time = None

if datetime_match:
    dt = datetime_match.group()
    date, time = dt.split()

payment = re.search(r"Банковская карта|Наличные|Карта", text)

payment_method = payment.group() if payment else None

total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)

total = None
if total_match:
    total = total_match.group(1).replace(" ", "")

data = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(data, indent=4, ensure_ascii=False))