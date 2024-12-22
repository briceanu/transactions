from datetime import datetime, timedelta

# today = datetime.now()
# future = today + timedelta(days=10)
# print(future) 

today = datetime.now()
# yesterday = today - timedelta(days=1)
# print(yesterday)
print(today)

now = datetime.now()
formatted_date = now.strftime("%H:%M")
print("Formatted:", formatted_date)