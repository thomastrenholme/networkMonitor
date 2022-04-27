## Remember to import nmap modualtion for this to work
import sys
import nmap
import smtplib
import time
from datetime import datetime
ps = nmap.PortScanner()
#Scans a range of hosts ip addresses between 192.168.0.1 and 192.168.0.10 (example ip, we can change this) for multiple devices
ps.scan(hosts = '192.168.0.1-10')

# clear screen
sys.stdout.write(u"\u001b[2J\u001b[0;0H")
sys.stdout.flush()
time.sleep(0.2)

# iterate over the hosts on the network

class networkMonitor():


    device, macAddr = initializeNetwork()
    

    def initializeNetwork():

        mac = ""
        for host in sorted(ps.all_hosts()):

            # blank if not Pi
            device = ""

            if len(ps[host]['device']) > 0:

                # attempt to get mac address
                try:
                    mac = ps[host]['addresses']['mac']
                except:
                    mac = ""

                device = tuple(ps[host]['device'].values())
                if str(device).find('Raspberry') > 0:
                    device = "Pi!"
                    # Sets color to white, results hostname, Ip, and Mac Addresses
                    print(u"\u001b[37m" + "{} ({}) {}\u001b[0m".format(ps[host].hostname(), host, mac))
                    return device, mac
                else:
                    device = ""
                    print(u"\u001b[0m" + "{} ({}) {}\u001b[0m".format(ps[host].hostname(), host, mac))

    
    ##(frequency) a frequency of how often youd like to receive network summary emails (in days) ex: frequency = 7: every 7 days email will be sent
    ##(emailList): list of emails to send network stats to
    def setUpNetworkEmailer(self, frequency, emailList):
       
        gmail_user = 'networkmonitorpi@gmail.com'
        gmail_password = 'cs578iscool!'


        ##Implement every [frequency] days, do this
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.login(gmail_user, gmail_password)

            for i in range(len(emailList)):
                ##send email to email
                email = self.getNetworkReportsForEmail(emailList[i])

                server.login(gmail_user, gmail_password)
                server.sendmail(gmail_user, emailList[i], email)
            
            ##Close connection after all emails sent
            server.close()
        except:
            print("Server smtp setup returned error")
    

    ##Return list of email text for setUpNetworkEmailer
    def getNetworkReportsForEmail(self, sendToEmail):
        sent_from = "Raspberry Pi Network Monitor"
        to = sendToEmail
        ##Implement subject
        subject = "Pi Network Scanner Report for: " + datetime.now().strftime("%m/%d/"+"20"+"%y")
        body = "Network visits: " + "Network statistics: " + " Unusual activity: " + " Fun fact of the day: "

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        return email_text
        
