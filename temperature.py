from math import ceil, sqrt, log, e

lin_it = lambda temp, time : temp+time
lin_dt = lambda temp, time : max(0, temp-time)

q_it = lambda temp, time : temp+time**2
q_dt = lambda temp, time: max(0, temp-time**2)

e_it = lambda temp, time: temp+e**time
e_dt = lambda temp, time: max(0, temp-e**time) if time < 10 else 0

lin_max_pt = lambda temp: temp
q_max_pt = lambda temp: max(int(sqrt(temp)),1)
e_max_pt = lambda temp: max(int(log(temp)),1)

lin_wait = lambda ctemp, temp: max(temp - ctemp, 0)
q_wait = lambda ctemp, temp: sqrt(temp - ctemp) if temp > ctemp else 0
e_wait = lambda ctemp, temp: log(temp -ctemp) if temp > ctemp else 0