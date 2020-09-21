# nessus CSV parser
given nessus finding ID value, extract associated IP(s)


(the following is copy pasta'd from the main .py file) 

# usage
primarily built to take 1, nessus output in the form of a CSV, 2, a plugin ID, and then pull out all of hosts associated with that plugin ID. 
can also be convinced to spit out a list of all hosts(&ports) nessus marked as being a web server for ease at throwing at another script somewhere. 

warning: has some hardcoded values and does VERY LITTLE error checking. the hardcoded values won't bother you as long as you provide a PID and a CSV.

# usage example
-most commonly,

python nessus_CSVparse.py -f <filename> -p <plugin_ID> 


-or, if you want multiple plugins at once,

python nessus_CSVparse.py -f <filename> -pl <file where plugin IDs are listed (deliminated by \n)> 


(note: -pl is currently a pipe dream, its currently just taking in straight commandline input in the form of "deliminated by ','" and doesn't handle whitespace.) 


-print a list of hosts (and ports) of web servers

python nessus_CSVparse.py -w -f <filename> 

