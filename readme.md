## Geofencing Demo
The Geofencing Demo will allow you to select a specific client to monitor, then notify you if the client moves away from it's current location.

This application is provided "As-is" by Aerohive free of charge. It is intended to demonstrate a capability using the APIs on the Aerohive Cloud Services platform. It is not intended for mission critical applications, and Aerohive does not provide support for this product. You are free to modify, the source code as you see fit, but appliccation usability and security are your responsibility.

#### Running the Application:
##### Prerequisites:
The binary package includes all 3rd party libraries necessary to run in any environment. If you may need to iunstall the following Python packages:
* requests: http://docs.python-requests.org/en/master/

##### Execution:
In the Binaries folder, execute Geofencing-Demo. You will be prompted for some information:
```sh
We need your VHM ID and access token to fetch data from your Hive Manager instance.
For information on how to get yours, look here: https://developer.aerohive.com/docs/authentication



VHM information can be obtained from NGs About section.
Please enter your VHM: 
```

Navigate to HiveManager NG and click on 'About'. Here you will see your VHM ID. Type that number into the console, and write it down somewhere you will remember.
![about](https://raw.githubusercontent.com/aerohive/Geofencing/master/ScreenShots/About.tiff)

If you don't already have an access token for the demo apps, now is a good time to set that up. Go to the settings page of Hive Manger, select API Token Management, and click the '+' icon.
![TokenManagement](https://raw.githubusercontent.com/aerohive/Geofencing/master/ScreenShots/GenerateToken.tiff)

After generating an access token (or if you have one already), enter it into the console.
You will then be asked how long you want the demo to run, and how frequently the application should request location data from Aerohive Cloud Services. If you will run the demo for a long period of time, increase the wait period between refreshes to reduce the total number of requests.

Now you will be presented a list of access points. Select one which has APs near it in order to find clients with locations:
```sh
Requesting: https://cloud-va.aerohive.com/xapi/v1/monitor/devices?ownerId=1265

Asking which bees live at your hive:
DEVICE MONITORING API response code: 200

Please select a device to request clients for:
1.	9C5D12227B80 | UK1-Basement
2.	E01C41489080 | HQ1-2124p-4
3.	E01C414B5280 | UK1-Oldbuild
4.	9C5D12710080 | HQ1-Shipping21
5.	E01C41506F00 | UK1-Newbuild
6.	9C5D12710C80 | HQ1-Finance25
7.	9C5D12710100 | HQ1-Accounts24
8.	9C5D12021980 | UK1-1stFloor
9.	9C5D12021300 | UK1-Groundfloor
10.	9C5D12227580 | UK1-IT
11.	9C5D12710F40 | HQ1-Jamaica22
12.	9C5D12707180 | HQ1-HR28-2
13.	001977821DC0 | HQ3-Demo
14.	9C5D12015A80 | UK1-2ndFloor
15.	9C5D12227780 | UK1-Marketing
16.	9C5D1270D6C0 | HQ1-Revenue23
17.	E01C41425240 | UK1-OldBuild2
Enter Access Point number: 
```

Now you will be presented with a list of clients connected to that AP.
Select a client and the application will monitor it for changes.
```sh
Requesting: https://cloud-va.aerohive.com/xapi/v1/location/clients/?ownerId=1265&apMacs=9C5D12710080
Requesting clients connected to: 9C5D12710080
Location API response code: 200

Please select a client to monitor location:
1.	247703A34758 | EReyes1-T430	| Intel Corporate
2.	E8B1FCF51905 | egomez-x1	| Intel Corporate
3.	3010E449C53B | yys-iPhone5	| Apple Inc
4.	5C514F7305E6 | poconnell-T440	| Intel Corporate
5.	605718E3846A | ajacquet-x1	| Intel Corporate
6.	00CDFE9B8DF3 | AgnieszasiPhone	| None
7.	28B2BD011CD8 | jowang-t440	| Intel Corporate
8.	340286445C73 | ygaucher-x1	| Intel Corporate
9.	04F13E8F7209 | Pocos-iPhone	| Apple Inc
10.	24770328D578 | jsantaana-t420	| Intel Corporate
11.	00225853F445 | UNASSOCIATED	| None
12.	183A2DB84832 | UNASSOCIATED	| None
13.	5C514F8B87B0 | amansour-t440	| None
14.	8AA18668451D | UNASSOCIATED	| None
Enter client number: 
```
The X & Y coordinates relate to the position of the client in relation to the building floorplan entered in HiveManager. If GPS coodinates are entered for the Access Points, GPS coordinates will be calculated for the clients. If the client moves, you will see a message. If not, the application will continue to search until the time you specified elapses.
```sh
Enter client number: 3
3010E449C53B is at X:15.5208934807x Y: 4.01066588221
The client has not moved. (X:15, Y:4) Will look 1120 more times.
```