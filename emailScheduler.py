#Thomas Trenholme

import email
import sys
import nmap
import smtplib
import time
from datetime import datetime


class emailScheduler:
     ##(frequency) a frequency of how often youd like to receive network summary emails (in days) ex: frequency = 7: every 7 days email will be sent
    ##(emailList): list of emails to send network stats to

    def __init__(self, frequencyInDays):
        self.frequency = frequencyInDays
        self.gmailAcc = "networkmonitorpi@gmail.com"
        self.emailList = []
        self.gmailAccPassword = "cs578iscool!"

        self.setUpNetworkEmailer()

    def __init__(self, frequencyInDays, emailList):
        self.frequency = frequencyInDays
        self.gmailAcc = "networkmonitorpi@gmail.com"
        self.emailList = emailList
        self.gmailAccPassword = "cs578iscool!"

    def addEmailToSubscriberList(self, email):
        self.emailList.append(email)

    def removeFromSubscriberList(self, email):
        self.emailList.remove(email)
    def setUpNetworkEmailer(self):

        sleepFrq=self.frequency

        while True:
            time.sleep(sleepFrq*60*60*24)

            self.emailSenderFunction(self.emailList)
        




    ##sends email and waits (frq days) and will send another one
    def emailSenderFunction(self, emailList):
        ##Implement every [frequency] days, do this
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.login(gmail_user, gmail_password)

            for addr in emailList:
                ##send email to email
                    sent_from = "Raspberry Pi Network Monitor"
                    to = addr
                    ##Implement subject
                    subject = "Pi Network Scanner Report for: " + datetime.now().strftime("%m/%d/"+"20"+"%y")
                    body = "Network visits: " + "Network statistics: " + " Unusual activity: " + " Fun fact of the day: "

                    email_text = """\
                    From: %s
                    To: %s
                    Subject: %s

                    %s
                    """ % (sent_from, ", ".join(to), subject, body)

                    server.sendmail(self.gmailAcc, emailList[i], email_text)
            
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
        
