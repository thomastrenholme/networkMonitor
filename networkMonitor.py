## Remember to import nmap modualtion for this to work
import email
import sys
from threading import Thread
import nmap
import smtplib
import time
from datetime import datetime
from emailScheduler import emailScheduler
from network_logger import network_logger
from networkMonitorGUI import networkMonitorGUI


# iterate over the hosts on the network

class networkMonitor():

        def __init__(self):
                ##Initialize network logger
                self.ps = nmap.PortScanner()
                self.nLogger = network_logger()
                self.initializeNetwork()
                

                ##Initialize GUI Thread
                self.exitThreads=False
                self.emailScheduler = emailScheduler(1, [])
                guiThread = Thread(target=networkMonitorGUI.networkMonitorsetup, args=(self, ))
                guiThread.start()
                
                ##Setup is done, start email timer and monitoring thread
                emailSendingThread = Thread(target=emailScheduler.setUpNetworkEmailer, args=(self, ))
                emailSendingThread.start()

                


        # deviceID, macAddr = initializeNetwork()

                
        
        def initializeNetwork(self):

                port_list = '21,22,23,80,81,8080'
                self.ps.scan('192.168.0.1-13', port_list, arguments='-sS -v', sudo=True)
                self.generateMaliciousIPList()
                
        #Scans a range of hosts ip addresses between 192.168.0.1 and 192.168.0.10 (example ip, we can change this) for multiple devices
                self.ps.scan('192.168.0.1-10', port_list, arguments='-sS', sudo=True)

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
                        self.nLogger.add_text(ip_string+"\n")
                        if ip_string in self.malicious:
                                self.nLogger.add_text("POTENTIALLY MALICIOUS IP ADDRESS DETECTED")
                                print("POTENTIALLY MALICIOUS IP ADDRESS DETECTED")
                        if 'tcp' in self.ps[host].keys():
                                tcplist = self.ps[host]['tcp']
                                for tcp in tcplist:
                                        output = "Port #"+str(tcp)+"- Name: "+str(tcplist[tcp]['name'])+"; State: "+str(tcplist[tcp]["state"])+"; Reason: "+tcplist[tcp]["reason"]+"\n"
                                        # print(output) 
                                        self.nLogger.add_text(output)
                self.nLogger.write_to_file()   
            # if len(ps[host]['product']) 

        def generateMaliciousIPList(self):
                with open("malicious-ips.txt",'r+') as ipFile:
                        self.malicious = []
                        for line in ipFile:

                                self.malicious.append(line)