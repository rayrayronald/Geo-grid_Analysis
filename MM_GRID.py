# 2018 - 2019 Imperial College London Biomedical Engineering Year 2 Engineering Design Project Ronald Hsu


import array
import urllib
import os
import struct
import RPi.GPIO as GPIO


N_ROW = 2
N_COL = 3
Radius = 100
#END_Y = 50.720943
START_Y =51.4966478
#END_X =-1.868413
START_X =-0.1736854
#START_Y = 50.712210
END_Y =51.5006107
#START_X = -1.886354
END_X =-0.1640704
X_INT = (END_X - START_X) / N_COL / 2
Y_INT = (END_Y - START_Y) / N_ROW / 2
TOTAL_X_CAP =1016
TOTAL_Y_CAP =762
X_SCALE = (END_X - START_X)/TOTAL_X_CAP
Y_SCALE = (END_Y - START_Y)/TOTAL_Y_CAP
Long = (END_X - START_X) /2 + START_X
Lat = (END_Y - START_Y) /2 + START_Y
NUMBER_READOUTS = 3
name = [0,0,0,0,0,0]
ROAD_BUFFER = 30


GPIO.setmode(GPIO.BOARD)

button_places = 16 #23  OOPS 12 #18
button_roads = 38 #20  OOPS 40 #21
#button_exit = 13 #27 IN LOOP SCRIPT
button_exit = 13 #27 16 #22 TRIGGERS NFC RE-READ
button_UP = 29 #5
button_DOWN = 31 #6
#GPIO.setmode(GPIO.BCM)
#button_places = 18
#button_roads = 21
#button_exit = 22

GPIO.setup(button_places, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_roads, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)


for i in N_ROW:
        for j in N_COL:
                Lat2 = START_Y + (i-0.5)*Y_INT
                Long2 = START_X + (j-0.5)*X_INT
                grid[i][j] = [Long2 , Lat2]
                URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius="+str(Radius)+"&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&location="+str(Lat2)+","+str(Long2)
                html=urllib.urlopen(URL)
                htmltext=html.read()
                postname = 1
                phrase =  "\"name\" : \""
                prename = htmltext.find(phrase,postname)
                postname =  htmltext.find("\"", prename+len(phrase)+1)
                names[i][j] = htmltext[prename+len(phrase):postname]
                print i,", ",j, ": ", names[i][j]


print ("IP Adress for SSH:")
IP = os.system('hostname -I')
os.system('iwgetid')
print IP
os.system('espeak "Welcome to V I map" 2>/dev/null')
file = open( "/dev/input/mice", "rb" );
print ("PROGRAM LOADED!\n")

for i in N_ROW:
    for k in N_COL ;



def places(channel):
        print ("LOADING DATABASE...")
        URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius="+str(Radius)+"&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&location="+str(Lat)+","+str(Long)
        print URL, "\nPLACES DATABASE UPDATED!\n"
	print Lat
	print Long
        html=urllib.urlopen(URL)
        htmltext=html.read()
        postname = 1
        for i in range(NUMBER_READOUTS+1):
                phrase =  "\"name\" : \""
                prename = htmltext.find(phrase,postname)
                postname =  htmltext.find("\"", prename+len(phrase)+1)
                name[i] = htmltext[prename+len(phrase):postname]
                if name[i] == "l_attributions":
                        os.system('espeak "There are no more places nearby" 2>/dev/null ')
                        break
                if i == 0:
                            os.system('espeak "{0}, {1} places within {2} metres" 2>/dev/null '.format(name[i],NUMBER_READOUTS,Radius))
                else:
                        print i,": ", name[i]
                        os.system('espeak "{0}" 2>/dev/null '.format(name[i]))
def exit(channel):
        print ("QUITING PROGRAM...\nIP Adress for SSH:")
        IP = str(os.system('hostname -I'))
        wifi = str(os.system('iwgetid'))
#        os.system('espeak "IP Address {0}, wifi {1}" 2>/dev/null'.format(IP,wifi))
	os.system('espeak "Refreshing" 2>/dev/null ')
        raise SystemExit
def roads(channel):
        global Long
        global Lat
        URL_road = "https://roads.googleapis.com/v1/snapToRoads?&interpolate=true&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&path="
        #URL_road ="https://roads.googleapis.com/v1/nearestRoads?&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&points="
        for i in range(ROAD_BUFFER):
                print "GETTING ROAD DATA BUFFER...",i,"out of", ROAD_BUFFER
                buf = file.read(3)
                x,y = struct.unpack( "bb", buf[1:] );
                Long += x*X_SCALE
                Lat += y*Y_SCALE
                print ("Coord: x: %8f, y: %8f" % (Long, Lat));
                if i > 20:
                        URL_road += str(Lat)+","+str(Long)
                if i < ROAD_BUFFER-1 and i > 20:
                        URL_road += "|"
        print URL_road
        html=urllib.urlopen(URL_road)
        htmltext=html.read()
        print("ROAD SNAPPING LOADED!\n")
        postname = 1
        phrase =  "\"placeId\": \""
        prename = htmltext.find(phrase,postname)
        postname = htmltext.find("\"", prename+len(phrase)+1)
        placeId = htmltext[prename+len(phrase):postname]
        URL = "https://maps.googleapis.com/maps/api/place/details/json?&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&placeid="+placeId
        print "Place Id: ", placeId, "\n" , URL, "\nROAD NAME UPDATED!\n"
        html=urllib.urlopen(URL)
        htmltext=html.read()
        postname = 1
        phrase =  "\"formatted_address\" : \""
        prename = htmltext.find(phrase,postname)
        postname =  htmltext.find(",", prename+len(phrase)+1)
        road_address = htmltext[prename+len(phrase):postname]
        print("Road name: "),
        print(road_address)
        os.system('espeak "{0}" 2>/dev/null '.format(road_address))

GPIO.add_event_detect(button_places, GPIO.FALLING, callback=places, bouncetime=700)
GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=exit, bouncetime=700)
GPIO.add_event_detect(button_roads, GPIO.FALLING, callback=roads, bouncetime=700)
trigger = 0

while True:
        buf = file.read(3)
        x,y = struct.unpack( "bb", buf[1:] );
	triple =  struct.unpack( '3b', buf)
	print triple
	if triple[0] == 8:
		print ("LEFT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
		if trigger >= 0 and x <= TOTAL_X_CAP/10 and y <= TOTAL_Y_CAP/10 :
			print (" DOUBLE CLICKEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
			places(1)
			trigger = -1
		else:
			trigger = 2
	trigger -= 1
        Long += x*X_SCALE
        Lat += y*Y_SCALE
        print ("Coord: x: %8f, y: %8f" % (Long, Lat));
