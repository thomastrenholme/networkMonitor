## Remember to import nmap modualtion for this to work
import email
import sys
import nmap
import smtplib
import time
from datetime import datetime
from emailScheduler import emailScheduler
from networkMonitorGUI import networkMonitorGUI


# iterate over the hosts on the network

class networkMonitor():

        def __init__(self):
                self.emailList = []
                self.frequencyInDays=0
                self.frequencyStr=""
                self.emailScheduler = emailScheduler(self.frequencyInDays, self.emailList)
                networkMonitorGUI.networkMonitorsetup(self)

                
                ##Setup is done, start email timer and monitoring
                self.emailScheduler.setUpNetworkEmailer()

                


        # deviceID, macAddr = initializeNetwork()

                
        
        def initializeNetwork(self):
                ps = nmap.PortScanner()
                port_list = '21,22,23,80,81,8080'
        #Scans a range of hosts ip addresses between 192.168.0.1 and 192.168.0.10 (example ip, we can change this) for multiple devices
                ps.scan('192.168.0.1-10', port_list, arguments='-sS', sudo=True)

        # clear screen
                sys.stdout.write(u"\u001b[2J\u001b[0;0H")
                sys.stdout.flush()
                time.sleep(0.2)
                mac = ""
                print(ps.all_hosts())
                for host in sorted(ps.all_hosts()):

            # blank if not Pi
                        print(ps[host]['addresses']['ipv4'])
                        print(ps[host].hostname())

            # if len(ps[host]['product']) > 0:

            #     # attempt to get mac address
            #     try:
            #         mac = ps[host]['addresses']['mac']
            #     except:
            #         mac = ""

            #     device = tuple(ps[host]['device'].values())
            #     if str(device).find('Raspberry') > 0:
            #         device = "Pi!"
            #         # Sets color to white, results hostname, Ip, and Mac Addresses
            #         print(u"\u001b[37m" + "{} ({}) {}\u001b[0m".format(ps[host].hostname(), host, mac))
            #         return device, mac
            #     else:
            #         device = ""
            #         print(u"\u001b[0m" + "{} ({}) {}\u001b[0m".format(ps[host].hostname(), host, mac))
