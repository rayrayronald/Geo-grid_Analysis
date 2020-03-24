import populartimes
import json

START_Y = 48.141000
START_X = 11.577126
END_Y = 48.142199
END_X = 11.580047









def jprint(obj):
# create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text


smth = populartimes.get("AIzaSyA3aYU6UKfZkp8QfafB2WCfouPjxVrFx2A", ["bar"], (START_Y, START_X), (END_Y , END_X))

converted = jprint(smth)

for items in smth:
    print(items["populartimes"][0]["data"])
    print ("HAHA")
