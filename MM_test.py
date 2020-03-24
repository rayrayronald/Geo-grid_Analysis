# 2018 - 2019 Imperial College London Biomedical Engineering Year 2 Engineering Design Project Ronald Hsu


import array
import urllib
import os
import struct
import numpy
import requests
import json



N_ROW = 2
N_COL = 2
grid_x = numpy.empty((N_COL),dtype=str)
grid_y = numpy.empty((N_ROW),dtype=str)
names = numpy.zeros((N_ROW,N_COL),dtype=(str,50))
Radius = 75
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


def jprint(obj):
# create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

for i in range(N_ROW):
        for j in range(N_COL):
                Lat2 = START_Y + (i-0.5)*Y_INT
                Long2 = START_X + (j-0.5)*X_INT
                grid_x[j] = Long2
                grid_y[i] = Lat2
                URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius="+str(Radius)+"&key=AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A&location="+str(Lat2)+","+str(Long2)
                print (URL)
                r = requests.get(URL)
                htmltext = jprint(r.json())
                #print(htmltext)
                postname = 1
                for k in range(2):
                        phrase =  "\"name\": \""
                        prename = htmltext.find(phrase,postname)
                        postname =  htmltext.find("\"", prename+len(phrase)+1)
                        if k == 1:
                                    names[i][j] = str(htmltext[prename+len(phrase):postname])
                                    print (i,", ",j, ": ", names[i][j])




