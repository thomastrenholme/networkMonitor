## Remember to import nmap modualtion for this to work
import email
import sys
import nmap
import smtplib
import time
from datetime import datetime
from emailScheduler import emailScheduler
from networkMonitorGUI import networkMonitorGUI
from network_logger import network_logger

# iterate over the hosts on the network

class networkMonitor():

        def __init__(self):
                self.ps = nmap.PortScanner()
                self.nl = network_logger()
        #         self.emailList = []
        #         self.frequencyInDays=0
        #         self.frequencyStr=""
        #         self.emailScheduler = emailScheduler(self.frequencyInDays, self.emailList)
        #         networkMonitorGUI.networkMonitorsetup(self)

                
        #         ##Setup is done, start email timer and monitoring
        #         self.emailScheduler.setUpNetworkEmailer()

                


        def generateMaliciousIPList(self):
                with open("malicious-ips.txt",'r+') as ipFile:
                        self.malicious = []
                        for line in ipFile:
                        
                                self.malicious.append(line)

                
        
        def initializeNetwork(self):
                
                port_list = '21,22,23,80,81,8080'
        #Scans a range of hosts ip addresses between 192.168.0.1 and 192.168.0.10 (example ip, we can change this) for multiple devices
                # ps.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389')
                self.ps.scan('192.168.0.1-13', port_list, arguments='-sS -v', sudo=True)
                self.generateMaliciousIPList()
        # clear screen
                sys.stdout.write(u"\u001b[2J\u001b[0;0H")
                sys.stdout.flush()
                time.sleep(0.2)
                mac = ""
                print(self.ps.all_hosts())
                for host in sorted(self.ps.all_hosts()):

                        
            # blank if not Pi
                        
                        print(self.ps[host])
                        ip_string = "IP: "+str(self.ps[host]['addresses']['ipv4'])
                        # print(ip_string)
                        self.nl.add_text(ip_string+"\n")
                        if ip_string in self.malicious:
                                self.nl.add_text("POTENTIALLY MALICIOUS IP ADDRESS DETECTED")
                                print("POTENTIALLY MALICIOUS IP ADDRESS DETECTED")
                        if 'tcp' in self.ps[host].keys():
                                tcplist = self.ps[host]['tcp']
                                for tcp in tcplist:
                                        output = "Port #"+str(tcp)+"- Name: "+str(tcplist[tcp]['name'])+"; State: "+str(tcplist[tcp]["state"])+"; Reason: "+tcplist[tcp]["reason"]+"\n"
                                        # print(output) 
                                        self.nl.add_text(output)
                self.nl.write_to_file()   
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
netwrol = networkMonitor()
netwrol.initializeNetwork()