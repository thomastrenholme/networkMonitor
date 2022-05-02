## Remember to import nmap modualtion for this to work
import email
import sys
from threading import Thread
import nmap
import smtplib
import time
import datetime
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

                


      

                
        
        def initializeNetwork(self):
                # Ping scan to network to get list of ip addresses connected to network
                        # port_list = '21,22,23,80,81,8080'
                self.ps.scan(hosts='192.168.0.1/24', arguments='-sS -v -n -PE -PA21,23,80,3389', sudo=True) 
                # generate lists of Malicious IPs and Yesterdays IPs based on associated text files and logs
                self.generateMaliciousIPList()
                self.generateYesterdaysIPList()
        
                
                

                # clear screen
                sys.stdout.write(u"\u001b[2J\u001b[0;0H")
                sys.stdout.flush()
                time.sleep(0.2)
                
                # after completing scan, iterate through all hosts, or IPs and access data
                        # print(self.ps.all_hosts())
                for host in sorted(self.ps.all_hosts()):

                        # get IP address, and add it to string for logging
                                # print(self.ps[host])
                        ip = str(self.ps[host]['addresses']['ipv4'])
                        ip_string = "IP: "+ip
                                # print(ip_string)
                        
                        self.nLogger.add_text(ip_string+"\n")
                        # check to see if the ip address is in the list of malicious ips 
                        if ip in self.malicious:
                                # if so, send notification to logger
                                self.nLogger.add_text("POTENTIALLY MALICIOUS IP ADDRESS DETECTED")
                                # print("POTENTIALLY MALICIOUS IP ADDRESS DETECTED")
                        # check if this ip was on yesterday's log, if not log it as a new connection
                        if ip_string not in self.yesterdays_ips:
                                self.nLogger.add_text("NETWORK HAS RECEIVED A NEW CONNECTION\n")
                        # if the scan picks up tcp data for this ip
                        if 'tcp' in self.ps[host].keys():
                                # get list of tcp ports associated
                                tcplist = self.ps[host]['tcp']
                                # for each tcp port
                                for tcp in tcplist:
                                        # add the port number, name, state, and reason to the logger
                                        output = "Port #"+str(tcp)+"- Name: "+str(tcplist[tcp]['name'])+"; State: "+str(tcplist[tcp]["state"])+"; Reason: "+tcplist[tcp]["reason"]+"\n"
                                        # print(output) 
                                        self.nLogger.add_text(output)
                # write everything stored in logger to file
                self.nLogger.write_to_file()   
           
        # open text file of malicious ip addresses, and store each ip into a list
        def generateMaliciousIPList(self):
                with open("malicious-ips.txt",'r+') as ipFile:
                        self.malicious = []
                        for line in ipFile:
                                self.malicious.append(line)

        # open yesterday's log, and store each ip into a list to see what connections are new
        def generateYesterdaysIPList(self):
                yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%m-%d-"+"20"+"%y")
                with open("Network_Monitor_Logs/"+yesterday+"-Network_Monitor_Log.txt", "r") as yesterday:
                        for line in yesterday:
                                if line[0:3] == "IP:":
                                        self.yesterdays_ips.append(line[0:len(line)-1])

