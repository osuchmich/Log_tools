#!/bin/bash

echo "Write the path to the log file"

read LOGFILE

LINE=0

python Create_databases.py

python Failed_logins.py $LOGFILE

echo "Requesting information about IP origin..."

for i in $(cat $LOGFILE | awk "NR>$LINE"  | grep Invalid | awk '{print $(NF-0)}' | uniq) # extracting falied logins logs and IP Address to $i
do
        LOCATION=$(curl ipinfo.io/$i | grep country | grep -o '[A-Z][A-Z]') # Country search
        echo "UPDATE mysql.IP_RATING SET COUNTRY = '$LOCATION' WHERE IP = '$i';"
done | mysql --user=kali --password=kali
