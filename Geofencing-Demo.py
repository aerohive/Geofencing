#!/usr/bin/env python

### GEO-FENCING DEMO
### THIS APPLICATION WILL ALLOW YOU TO SET A CLIENT LOCATION, THEN BE NOTIFIED IF IT CHANGES.

import requests #to fire off HTTP requests
import datetime #to get the current date, and format dates for the APIs
import csv      #to read & write CSV files
import sys      #to create the progress indicator and print directly to the console.
import time     #to sleep & add timers.
import os       # to clear the screen.


#---Variables you will need to setup for your application:
#See http://developer.aerohive.com and navigate to 'My Applications'
clientID = "XXXXXXXXXXXX"
clientSecret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
redirectURL = "https://mysite.com"


#------Variables for NG interaction
baseUrl = 'https://cloud-va.aerohive.com/xapi'
# These are the headers we will use to interact with the APIs. Authorization will need to be updated with the access token.
headers= {'Authorization':'Bearer ', 'X-AH-API-CLIENT-ID':clientID, 'X-AH-API-CLIENT-SECRET':clientSecret, 'X-AH-API-CLIENT-REDIRECT-URI':redirectURL}



#------Begin Application
print "\n\nAerohive Location Engine Demo - Geofencing"
print "Written by: Daniel O'Rorke (dororke@aerohive.com)"
print "(c) 2016 Aerohive Networks"
print "This application will set a fence around a client, and notify you when it moves location.\n\n"

#---Prompt user for input:
print "We need your VHM ID and access token to fetch data from your Hive Manager instance."
print "For information on how to get yours, look here: https://developer.aerohive.com/docs/authentication\n\n\n"
print "VHM informaiton can be obtained from NG's About section."
ownerID = raw_input('Please enter your VHM: ')
accessToken = raw_input('Please enter your Access Token: ')
headers["Authorization"] = "Bearer "+accessToken
minutesToTrackLocationFor = int(raw_input('How many minutes should this run? '))
secondsToWaitBetweenRequests = int(raw_input('Seconds to wait between updates: '))

##---Query the LocationFolders API for a list of places.
## Use this to get the location we'll monitor.
##https://cloud-va.aerohive.com/xapi/v1/configuration/apLocationFolders?ownerId=1265
#locationFoldersURL = "/v1/configuration/apLocationFolders"
#queryParams = "?ownerId="+ownerID
#url = baseUrl+locationFoldersURL+queryParams
#print "Requesting: "+url
#print "Requesting location data for your VHM:"
## Request Location data for all clients
#response = requests.get(url, headers=headers)
#print "Location Folders API response code: "+str(response.status_code)
#JSON = response.json()
#
## Print the data to screen and request user to select a client.
#print "\nPlease the number that corresponds to the location you'd like to monitor clients in:"
#index = 1
#locationFolders = {} # dictionary we can look up the location ID from the name
#for level1Data in JSON["data"]["folders"]:
#    print level1Data["name"] # print the hierarchy folders.
#    for level2Data in level1Data["folders"]:
#        print "\t"+level2Data["name"]
#        for level3Data in level2Data["folders"]:
#            print "\t\t"+level3Data["name"]
#            for level4Data in level3Data["folders"]:
#                locationFolders[index] = level4Data["id"]
#                print "\t\t\t"+str(index)+": "+level4Data["name"]
#                index += 1
#locationFolderInput = int(raw_input('Enter location number: '))
#
#locationFolder = locationFolders[locationFolderInput]

##--- Get all APs associated w/ the Location Folder the User Selected

##---Query the Device Monitor API for a list of APs.
#https://cloud-va.aerohive.com/xapi/v1/monitor/devices?ownerId=1265
deviceMonURL = "/v1/monitor/devices"
queryParams = "?ownerId="+ownerID
url = baseUrl+deviceMonURL+queryParams
print "Requesting: "+url
print "\nAsking which bees live at your hive:"
# Request Location data for all clients
response = requests.get(url, headers=headers)
print "DEVICE MONITORING API response code: "+str(response.status_code)
JSON = response.json()
# Print the data to screen and request user to select a device.
print "\nPlease select a device to request clients for:"
for i in range(0,len(JSON["data"])):
    print str(i+1)+".\t"+JSON["data"][i]["macAddress"]+" | "+JSON["data"][i]["hostName"]
deviceToTrack = int(raw_input('Enter client number: '))
deviceToTrackIndex = deviceToTrack - 1 # Remember indexes start at 0, so we need to reduce the user input by 1 to get the index of the machine they are referring to.
apMacs = JSON["data"][deviceToTrackIndex]["macAddress"] # Set the mac address for the Location Monitoring Query

#---Query the Monitoring API for a list of clients.
# We will only use this to build a table of the hostnames & user names to look up from MAC address in the next query
# Build Client Monitoring API URL
#https://cloud-va.aerohive.com/xapi/v1/location/clients/?ownerId=1265&apMacs=9C5D12710100
clientNames = {} # where we will store the client hostName to lookup.
clientMonURL = "/v1/monitor/clients/"
queryParams = "?ownerId="+ownerID
url = baseUrl+clientMonURL+queryParams
print "Requesting: "+url
print "Requesting clients connected to: "+apMacs
# Request Location data for all clients
response = requests.get(url, headers=headers)
print "Location API response code: "+str(response.status_code)
JSON = response.json()
for client in JSON["data"]:
    clientNames[client["clientMac"]] = client["hostName"]
print "Saved all the host names for clients connected."




os.system("clear") #clear the screen
# Build Client Location Monitoring API URL
#https://cloud-va.aerohive.com/xapi/v1/location/clients/?ownerId=1265&apMacs=9C5D12710100
clientLocationURL = "/v1/location/clients/"
queryParams = "?ownerId="+ownerID+"&apMacs="+apMacs
url = baseUrl+clientLocationURL+queryParams
print "Requesting: "+url
print "Requesting clients connected to: "+apMacs
# Request Location data for all clients
response = requests.get(url, headers=headers)
print "Location API response code: "+str(response.status_code)
JSON = response.json()

# Print the data to screen and request user to select a client.
print "\nPlease select a client to monitor location:"
for i in range (0, len(JSON["data"][0]["observations"])): # Using 0 assumes that the 1st element will be the AP we filtered to.
    # To make this more robust, you scan the returned array for the AP MAC to ensure the APIs are doing what we expect & don't silently fail or return incorrect data.

    # Handle unassociated clients that will be reported in Location APIs
    if JSON["data"][0]["observations"][i]["clientMac"] not in clientNames:
        clientNames[JSON["data"][0]["observations"][i]["clientMac"]] = "UNASSOCIATED"
    
    print str(i+1)+".\t"+str(printClientMac)+" | "+clientNames[JSON["data"][0]["observations"][i]["clientMac"]]+"\t| "+str(JSON["data"][0]["observations"][i]["manufacturer"])
clientToTrack = int(raw_input('Enter client number: '))
clientToTrackIndex = clientToTrack - 1 # Remember indexes start at 0, so we need to reduce the user input by 1 to get the index of the machine they are referring to.

# Start monitoring the client's location
clientMAC = JSON["data"][0]["observations"][clientToTrackIndex]["clientMac"]
clientPositionX = JSON["data"][0]["observations"][clientToTrackIndex]["x"]
clientPositionY = JSON["data"][0]["observations"][clientToTrackIndex]["y"]
print clientMAC+" is at X:"+str(clientPositionX)+"x Y: "+str(clientPositionY)
for i in range (0,((minutesToTrackLocationFor*60)/secondsToWaitBetweenRequests)): #repeat this for the number of times corresponding to the minutes to track.
    response = requests.get(url, headers=headers)
    JSON = response.json() #convert the response to a JSON object we can work with.
    found = False
    for client in JSON["data"][0]["observations"]: # Using 0 assumes that the 1st element will be the AP we filtered to.
        if client["clientMac"] == clientMAC: # find the client in the current data
            xDiff = abs(clientPositionX - JSON["data"][0]["observations"][clientToTrackIndex]["x"])
            yDiff = abs(clientPositionY - JSON["data"][0]["observations"][clientToTrackIndex]["y"])
            if xDiff + yDiff > 0: #if the client moved
                print "Client moved X: "+str(xDiff)+" Y: "+str(+yDiff)
            else:
                sys.stdout.write("\rThe client has not moved. %d %d Will look %d more times." %(JSON["data"][0]["observations"][clientToTrackIndex]["x"], JSON["data"][0]["observations"][clientToTrackIndex]["y"], ((minutesToTrackLocationFor*60)/secondsToWaitBetweenRequests)-i))
                sys.stdout.flush()
            found = True
    if not found:
        print "The client is no longer connected."
        break
    i += 1
    time.sleep(secondsToWaitBetweenRequests)
print "The set time period to monitor has elapsed. Please change the settings or restart the demo if you would like to try again."