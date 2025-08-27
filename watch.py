#Current time: 2025-08-25 14:26:56.371, Time difference from previous: 0.504441 seconds

import os
import json
import fileinput

def is_decimal(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def update_values(themax,themin,theline,thecount):
    data = {
        "min": 0.0,
        "max": 0.0
         }

    data['min'] = themin
    data['max'] = themax
    json_str = json.dumps(data, indent=4)
    with open('minmax.json','a') as hfile:
         history = {}
         history['min'] = themin
         history['max'] = themax
         history['line'] = theline
         history['lineno'] = thecount
         history_str = json.dumps(history, indent=4)
         hfile.write(history_str)
         hfile.close()
    with open(".maxmin","w") as f:
         f.write(json_str)
         f.close()

def watch_file(theargs):
    if os.path.exists(".maxmin"):
       with open(".maxmin","r") as f:
            data = json.load(f)
            themin = data['min']
            themax = data['max']
            f.close()
    else:
       themin = 100.0
       themax = -100.0
    linecount = 0
    for line in fileinput.input(theargs):
        linecount = linecount + 1
        if line.startswith("Current time:"):
           theline = line
           theidx = line.find("previous:")
           theend = line.find('seconds') 
           theidx = theidx + 10
           thestring = line[theidx:theend].strip()
           # print(thestring)
           if (is_decimal(thestring)):
              thevalue = float(thestring)
              if (thevalue > themax):
                 themax = thevalue
                 print("Max Value Line: " + theline)
                 update_values(themax,themin,theline,linecount)
              if (thevalue < themin):
                 themin = thevalue
                 print("Min Value Line: " + theline)
                 update_values(themax,themin,theline,linecount)
  print("Min = " + str(themin) + " Max = " + str(themax) + " Linex = " + str(linecount))

watch_file(args)
