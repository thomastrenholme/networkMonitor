import easygui







class networkMonitorGUI:
    frequency = ""
    frequencies = ["Every hour", "Every two hours", "Every 6 hours", "Every 12 Hours", "Every 24 hours (1 Day)", "Every 48 hours (2 days)", "Every 168 Hours (1 Week)"]
    frequenciesInDaysArr = [float(1)/24, float(1)/12, float(1)/4, float(1)/2, 1, 2, 7]
    possibleActions = ["Update frequency of emails.", "Add email to emailList", "Remove email from emailList", "Send network report to email list right now", "Turn network monitor off"]

    def networkMonitorsetup(networkMonitorpi):
        easygui.msgbox(msg="Welcome to the networkMonitorPi, developed by CS578 group 3", title="networkMonitorPi v1.1")

        frequency = easygui.buttonbox(msg="Please enter how frequently you would like to receive email updates from the network monitor",title="networkMonitorPi v1.1",choices=networkMonitorGUI.frequencies)

        networkMonitorpi.emailScheduler.frequency=networkMonitorGUI.frequenciesInDaysArr[networkMonitorGUI.frequencies.index(frequency)]
        networkMonitorpi.emailScheduler.frequencyStr=frequency

        emails = str(easygui.enterbox(msg="Please enter the email address or email addresses (seperated by a space) you would like the network monitor to send updates to. ",title="networkMonitorPi v1.1"))

        listOfEmailsToAdd = emails.split()

        networkMonitorpi.emailScheduler.addEmailToSubscriberList(listOfEmailsToAdd)


        networkMonitorGUI.networkMonitorMainMenu(networkMonitorpi)


    def networkMonitorMainMenu(networkMonitorpi):
        choice = easygui.buttonbox(msg="NetworkMonitorPi main menu.",title="networkMonitorPi v1.1",choices=networkMonitorGUI.possibleActions)

        if choice == "Update frequency of emails.":

            frequency = easygui.buttonbox(msg="Current frequency: " + networkMonitorpi.emailScheduler.frequencyStr + "\nPlease enter how frequently you would like to receive email updates from the network monitor",title="networkMonitorPi v1.1",choices=networkMonitorGUI.frequencies)

            networkMonitorpi.emailScheduler.frequency=networkMonitorGUI.frequenciesInDaysArr[networkMonitorGUI.frequencies.index(frequency)]
            networkMonitorpi.emailScheduler.frequencyStr=frequency

        if choice == "Add email to emailList":

            bigStrEmailList = ""
            for email in networkMonitorpi.emailScheduler.emailList:
                bigStrEmailList+= email + "\n"
            

            emailToAdd = str(easygui.enterbox(msg= "Emails are currently being sent to:\n" + bigStrEmailList + "Please enter the email address or email addresses (seperated by a space) you would like the network monitor to send updates to. ",title="networkMonitorPi v1.1"))

            listOfEmailsToAdd =emailToAdd.split()

            networkMonitorpi.emailScheduler.addEmailToSubscriberList(listOfEmailsToAdd)
            

        if choice == "Remove email from emailList":

            bigStrEmailList = ""
            for email in networkMonitorpi.emailScheduler.emailList:
                bigStrEmailList+= email + "\n"
            
            
            emailToRemove = str(easygui.enterbox(msg= "Emails are currently being sent to:\n" + bigStrEmailList + "Please enter the email address or email addresses (seperated by a space) you would like to remove from the receiving network updates. ",title="networkMonitorPi v1.1"))

            listOfEmailsToRemove=emailToRemove.split()

            networkMonitorpi.emailScheduler.removeEmailFromSubscriberList(listOfEmailsToRemove)

        if choice == "Send network report to email list right now": 

            bigStrEmailList = ""
            for email in networkMonitorpi.emailScheduler.emailList:
                bigStrEmailList+= email + "\n"
            choice = easygui.buttonbox(msg="Are you sure? Emails will be sent to the following email addresses:"+bigStrEmailList,title="networkMonitorPi v1.1",choices=["Yes", "No"])
            if choice == "Yes":
                networkMonitorpi.emailScheduler.emailSenderFunction(networkMonitorpi.emailScheduler.emailList)
                print("Sent out emails to: ")
                for email in networkMonitorpi.emailScheduler.emailList:
                    print(email)

        if choice == "Turn network monitor off":
            networkMonitorpi.exitThreads=True
            exit(0)
        
        ##Reopen main menu


        networkMonitorGUI.networkMonitorMainMenu(networkMonitorpi)















