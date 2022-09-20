import datetime

dt = 1662747683333 / 1000

now = datetime.datetime.now()

timestamp = datetime.datetime.timestamp(now)
print("timestamp =", timestamp)

tm = 1663162477614 // 1000

print(datetime.datetime.fromtimestamp(tm))