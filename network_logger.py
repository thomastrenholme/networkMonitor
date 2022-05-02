from datetime import datetime as dt
import sys


class network_logger:
    def __init__(self):
        self.date = dt.now().strftime("%m-%d-"+"20"+"%y")
        self.pathname = "Network_Monitor_Logs/"
        self.filename = self.date + "-Network_Monitor_Log"
        self.data = "Report for: "+str(self.date)+"\n"

    def write_to_file(self):
        with open(self.pathname+self.filename+".txt", 'w') as output:
            output.write(self.data)


    def add_text(self, text_to_add):  
        self.data+=text_to_add 
