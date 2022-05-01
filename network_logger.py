from datetime import datetime as dt
import sys
from networkMonitor import networkMonitor

date = dt.now().strftime("%m-%d-"+"20"+"%y")
pathname = "Network_Monitor_Logs/"
filename = date + "-Network_Monitor_Log"
print(filename)

with open(pathname+filename+".txt", 'w') as output:
    nm = networkMonitor()
    nm.initializeNetwork()
