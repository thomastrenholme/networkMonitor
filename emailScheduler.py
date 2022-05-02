#Thomas Trenholme

import email
import os
import sys
import nmap
import smtplib
import time
from datetime import datetime
from datetime import timedelta
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import randfacts


class emailScheduler:
     ##(frequency) a frequency of how often youd like to receive network summary emails (in days) ex: frequency = 7: every 7 days email will be sent
    ##(emailList): list of emails to send network stats to

    def __init__(self, frequencyInDays):
        self.frequency = frequencyInDays
        self.gmailAcc = "networkmonitorpi@gmail.com"
        self.emailList = []
        self.gmailAccPassword = "cs578iscool!"


    def __init__(self, frequencyInDays, emailList):
        self.frequency = frequencyInDays
        self.gmailAcc = "networkmonitorpi@gmail.com"
        self.emailList = emailList
        self.gmailAccPassword = "cs578iscool!"

    def addEmailToSubscriberList(self, emails):

        for email in emails:
            if email not in self.emailList:
                    self.emailList.append(email)


    def removeEmailFromSubscriberList(self, emails):

        for email in emails:
            if email in self.emailList:
                    self.emailList.remove(email)
        
    ##called once gui setup has completed


    ##Threaded function called from networkMonitor
    def setUpNetworkEmailer(networkMonitor):

        sleepFrq = networkMonitor.emailScheduler.frequency


        counter = 0
        ##counter will count minutes. Once counter reaches email interval, send email and reset counter.
        ##sleep for one minute, then recheck to see if frequency has been updated.

        print("Entering threaded func")

        while True:
            while counter < sleepFrq*24*60: ##sleep Frq in minutes. conversion:  sleepFrq(days) * 24 hour/day * 60 min/hour
                
                ##If exit flag
                if networkMonitor.exitThreads:
                    exit(0)
                sleepFrq=networkMonitor.emailScheduler.frequency

                time.sleep(60)##sleep for a minute

                print("Waited: " + str(counter) + " minute." + " Waiting till: " + str(sleepFrq) + " Days have passed to send out email.")
                print("Email list: " + str(networkMonitor.emailScheduler.emailList))
                counter+=1 ##increment counter by one minute
            
            ##Finished cycle. Send out email(s) and Reset counter to 0.
            networkMonitor.emailScheduler.emailSenderFunction(networkMonitor.emailScheduler, networkMonitor.emailScheduler.emailList)
            counter = 0



    ##sends email and waits (frq days) and will send another one
    def emailSenderFunction(self, emailList):

        ##Get email body
        report_text = ""
        yesterdayString = (datetime.now() + timedelta(days=-1)).strftime("%m-%d-"+"20"+"%y") + "-Network_Monitor_Log.txt" ##Gets 05-01-2022-Network_Monitor_Log.txt format
        print(yesterdayString)
        with open(os.path.join(os.path.dirname(__file__), 'Network_Monitor_Logs/' + yesterdayString), 'r') as f:
            for line in f:
                report_text+=line+"\n"
        report_text += "\nFun Fact of the Day: " + randfacts.get_fact()

            
        try:
            

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()

            server.starttls()

            server.ehlo()

            server.login("networkmonitorpi@gmail.com", "cs578iscool!")

            for addr in emailList:
                ##send email to email
                    email_text = self.getNetworkReportsForEmail(addr, report_text)

                    server.sendmail("networkmonitorpi@gmail.com", addr, email_text)
            
            ##Close connection after all emails sent
            server.close()
            print("Successfully sent out emails.")
        except:
            print("Server smtp setup returned error")
    

    ##Return email text for sending
    def getNetworkReportsForEmail(self, sendToEmail, bodyText):
        msg = MIMEMultipart()
        msg['From']="networkmonitorpi@gmail.com"
        msg['To']=sendToEmail
        msg['Subject'] = "Pi Network Scanner Report for: " + datetime.now().strftime("%m/%d/"+"20"+"%y")
        ##Implement subject
        msg.attach(MIMEText(bodyText))
        body = bodyText
        
        return msg.as_string()
        
