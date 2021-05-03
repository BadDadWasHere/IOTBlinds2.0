#import libraries
from datetime import datetime  #imports datatime
from dateutil.tz import UTC  #import timezone of UTC
from time import sleep  #import sleep from time
import requests  #imports requests

#create vars and lists
ipaddrs = []  #ipaddrs list, store ip addresses
print("Created list ipaddrs")
calURL = ""  #calURL, link for the iCalender
# {"END": time, "uid": uid}
print("Created string calURL")
already_Used = []  #list of used but not ended events
print("Created list already_Used")


#sets ipaddrs and calURL to = the corrillating to whats in a yaml file
def loadConfig(configfilename):  #in the config file, load ipaddrs's and calURL into the repective variables and lists
    print("running loadConfig")
    import yaml  #import yaml library
    data_loaded = {}  #creates dictionary to load yaml file into data_loaded
    print("created dictionary data_loaded")

    with open(configfilename, "r") as file:  # opens file as file
        data_loaded = yaml.safe_load(file)  # puts file into data_loaded
        print("loaded yaml file into data_loaded")

        global ipaddrs  #loads ipaddrs from outside loadConfig
        ipaddrs = data_loaded.get(
            "ipaddrs")  #puts every ip address into ipaddrs
        print("imported all ip addresses into ipaddrs:", ipaddrs)

        global calURL  #load calURL from outside loadConfig
        calURL = data_loaded.get("calurl")  # puts that URL into calURL
        print("imported calenderURL from yaml file into calURL:", calURL)


#run send command if events happened now
def doCalEvents(calenderURL):
    from icalevents.icalevents import events  #import events for icalevents
    calEvents = events(
        url=calenderURL
    )  #creates dictionary call calEvents, import all of the events on the calender
    print("created dictionary calevents, imported all events from calender")
    # print(calEvents)
    for i in calEvents:
        #run of calEvents to the number of events, i is equal to each event
        if i.start <= datetime.now(UTC):
            activated = False  #assume false
            #if already used, sets to true
            for a in already_Used:  #runs the number of entries in already_Used, a = current entry
                if i.uid == a["uid"]:  #does the uid of i, then activated = true
                    activated = True
                    print(i.uid + " has been already used")
                    
            if not activated:  #if not used, run sendCommand and put it in the already_Used
                if (i.summary.lower() == "up" or i.summary.lower() == "down" or i.summary.lower() == "stop"):
                  sendCommand(i.summary.lower())  #run send command, remember to uncomment
                  print(i.summary.lower())
                  already_Used.append({"END": i.end, "uid": i.uid})
                  print("Running " + i.uid)


def cleanupAlreadyUsed():  #remove excess already_Used events
    for i in already_Used:  #runs to the number of entries, i = to current entry
        if i["END"] <= datetime.now(UTC):  #runs code if the end time for entry is less than current time
            print("Removeing " + i["uid"] + ", Its time has past")  #says its removing i event from already used
            already_Used.remove(i)  #remove the i entry completely


#sends requests.get to all the websites with the ipaddrs ip addresses
def sendCommand(cmdstring):
    cmdstring = cmdstring.lower()

    if (cmdstring == "up" or cmdstring == "down"
            or cmdstring == "stop"):  #check to see if it up down or stop

        try:  #try and except to manage errors
            for i in ipaddrs:  #this will run through every ip address, change print to get
                requests.get("http://" + i + "/" + cmdstring)  #sends command
                print("sending " + cmdstring + " to " + i)
        except:
            print("Couldn't Connect")  #print error


loadConfig("config.yaml")  #loadConfig the config.yaml file

while True:  #always run
    doCalEvents(calURL)  #insert calURL and run doCalEvents
    cleanupAlreadyUsed()  #cleanupAlreadyUsed
    print(datetime.now(UTC))  #print current time

    sleep(5)  #wait 1 second befor running again
