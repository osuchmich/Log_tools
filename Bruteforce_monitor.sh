#!/bin/bash

echo "Write the path to the log file"

read LOGFILE

LINE=0
#LINE=$1 # Unccoment this and you'll be able to tell the script on which line to start (ex. ./Bruteforce_monitor.sh 120)
while true
do
	cat $LOGFILE | awk "NR>$LINE"  | grep Invalid >> tmp.txt # parsing logs for python script and putting it in a temporary file
	python Bruteforce_detector.py # running python script 
	wait
	rm tmp.txt
	LINE=$(cat $LOGFILE | wc -l) # ensuring that the next search is started from the last checked line
        sleep 15m #Iverval of searching for attacks is 15 minutes
done