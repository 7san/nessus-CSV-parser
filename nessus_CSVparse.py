# goal; given nessus finding ID value, extract associated IP/hosts
'''
usage:
primarily built to take 1, nessus output in the form of a CSV, 2, a plugin ID, and then pull out all of hosts associated with that plugin ID. 
can also be convinced to spit out a list of all hosts(&ports) nessus marked as being a web server for ease at throwing at another script somewhere. 

warning: has some hardcoded values and does VERY LITTLE error checking. the hardcoded values won't bother you as long as you provide a PID and a CSV.

usage example: 
-most commonly,
python nessus_CSVparse.py -f <filename> -p <plugin_ID> 

-or, if you want multiple plugins at once,
python nessus_CSVparse.py -f <filename> -pl <file where plugin IDs are listed (deliminated by \n)> 

(note: -pl is currently a pipe dream, its currently just taking in straight commandline input in the form of "deliminated by ','" and doesn't handle whitespace.) 

-print a list of hosts (and ports) of web servers
python nessus_CSVparse.py -w -f <filename> 


todo:
-make -pl actually take a file, maybe. idk if i actually care about -pl. 
-make -pl parsing better (again, do we care)
-include port option? 
-if NOT including ports, should probably be sort -u'ing
'''

# libraries
import csv
import argparse 


#main should maybe exist but i am a fundamentally a bad person.


# grab hosts corresponding to requested plugin ID and print to screen
# (**should eventually make pID into a list. )
def get_ips_from_pID(field, row, field_index, pID):

  j=0
  while j < len(row):
    #print(row[j][plugin_index])
    if pID in row[j][field_index['plugin']]:
      print(row[j][field_index['host']])
  
    j = j+1
    

#handles -w; spits out all of the hosts (and ports) noted as being webservers.
#incidentially, should line up with pID 10107? 
def get_webserver_list(field, row, field_index):
  j=0
  #print("made it to webserver list function")
  #print(field_index['host'], field_index['port'])
  while j < len(row):
    #print(row[j][plugin_index])
    if "HTTP Server Type " in row[j][field_index['name']]:
      print(row[j][field_index['host']] + ":" + row[j][field_index['port']])
  
    j = j+1
  


#arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="(CSV) file name/location.")
parser.add_argument("-p","--plugin", help="Plugin ID from Nessus.")
parser.add_argument("-pl","--pluginlist", help="List of plugin IDs from Nessus. (ie, ID,ID2,ID3)")
parser.add_argument("-w","--webservers_list", action="store_true", help="Generate list of web servers. (format: host:port)")
args = parser.parse_args()



# get file from user/args
# temp measure of reading from local directory 
f = "test.csv"

#wanting to say 'if exists'; seems to work, despite how i thought this would go.
if args.file: #does this work like you think it does #it does appear to, yes. curious.
  f = args.file


#***in progress
#might just die here.
'''usinglist = False 
plugins = []
if args.pluginlist:
  #plugin_f = 
  with open(args.pluginlist) as p:
    plugins = p.read().splitlines()
  usinglist = True
'''
  

# read in CSV file
row = []
field = []

#wait, does this just make a seperate list of the first row for the field names? i think it does. thats. dumb. but readable. but duummbbb.
with open (f, 'r') as csvfile: 
  csvreader = csv.reader(csvfile)
  field = csvreader.next()
  for i in csvreader:
    row.append(i)
    
    
    
# grab correct indexes from csv file
field_index = {'name':-1, 'host':-1, 'port':-1, 'plugin':-1}
i=0
while i < len(field):
  #print(field[i])
  if "Name" in field[i]:
    #print(i, field[i])
    field_index['name'] = i
  if "Plugin ID" in field[i]:
    #print(i, field[i])
    field_index['plugin'] = i
  if "Host" in field[i]:
    #print(i, field[i])
    field_index['host'] = i
  if "Port" in field[i]:
    #print("(field_index) port:")
    #print(i, field[i])
    field_index['port'] = i
    
  i = i+1


if args.webservers_list:
  get_webserver_list(field, row, field_index)


# grab from args the plugin ID we care about 
#should we be feeding this in through a file instead? feels that way.   
#maybe later. 
pID = "19506"
if args.plugin:
  pID = args.plugin
  get_ips_from_pID(field, row, field_index, pID)

#pluginlist is currently a commandline list, "1,2,3" type list. remove your own spaces.
if args.pluginlist: 
  plist = args.pluginlist.split(",")
  for p in plist:
    print(p)
    get_ips_from_pID(field, row, field_index, p)

exit()

