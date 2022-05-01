import easygui







class networkMonitorGUI:
    frequency = ""
    frequencies = ["Every hour", "Every two hours", "Every 6 hours", "Every 12 Hours", "Every 24 hours (1 Day)", "Every 48 hours (2 days)", "Every 168 Hours (1 Week)"]
    frequenciesInDaysArr = [float(1)/24, float(1)/12, float(1)/4, float(1)/2, 1, 2, 7]
    possibleActions = ["Update frequency of emails.", "Add email to emailList", "Remove email from emailList", "Turn on or off firewall", "Turn network monitor off"]

    def networkMonitorsetup(networkMonitorpi):
        easygui.msgbox(msg="Welcome to the networkMonitorPi, developed by CS578 group 3", title="networkMonitorPi v1.1")

        frequency = easygui.buttonbox(msg="Please enter how frequently you would like to receive email updates from the network monitor",title="networkMonitorPi v1.1",choices=networkMonitorGUI.frequencies)

        networkMonitorpi.frequencyInDays=networkMonitorGUI.frequenciesInDaysArr[networkMonitorGUI.frequencies.index(frequency)]
        networkMonitorpi.frequencyStr=frequency

        emails = str(easygui.enterbox(msg="Please enter the email address or email addresses (seperated by a space) you would like the network monitor to send updates to. ",title="networkMonitorPi v1.1"))

        listOfEmailsToAdd = emails.split()

        for email in listOfEmailsToAdd:
                networkMonitorpi.emailList.append(email)

        networkMonitorGUI.networkMonitorMainMenu(networkMonitorpi)


    def networkMonitorMainMenu(networkMonitorpi):
        choice = easygui.buttonbox(msg="NetworkMonitorPi main menu.",title="networkMonitorPi v1.1",choices=networkMonitorGUI.possibleActions)

        if choice == "Update frequency of emails.":

            frequency = easygui.buttonbox(msg="Current frequency: " + networkMonitorpi.frequencyStr + "\nPlease enter how frequently you would like to receive email updates from the network monitor",title="networkMonitorPi v1.1",choices=networkMonitorGUI.frequencies)

            networkMonitorpi.frequencyInDays=networkMonitorGUI.frequenciesInDaysArr[networkMonitorGUI.frequencies.index(frequency)]
            networkMonitorpi.frequencyStr=frequency

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

        if choice == "Turn on or off firewall":

            print("Firewall is currently: " + "off")

        if choice == "Turn network monitor off":
            exit(0)
        
        ##Reopen main menu


        networkMonitorGUI.networkMonitorMainMenu(networkMonitorpi)















