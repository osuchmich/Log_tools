*********************************************
Scripts need root permission to function properly
*********************************************
There must be a local user in the mysql database run this command: mysql> CREATE USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
*********************************************
Secure.2 file consists of example logs
*********************************************
ipinfo.io allowes limited requests without a token, so in order to get the whole database filled with countries you need to:
change the 18th line in the file RUNFRIST.sh to:

LOCATION=$(curl -u TOKEN ipinfo.io/$i | grep country | grep -o '[A-Z][A-Z]') # Country search

If you don't provide the TOKEN the scrip will run just fine, but there will be empty cells in the COUNTRY column
*********************************************
RUNFIRST.sh needs to be run first as the name implies, it creates databases and fills the IP_RATING table with IPs, number of failed login attemps and country, and orders this table by the most amount of failed login attempts.
*********************************************
In order to monitor brute force attacks just run Bruteforce_monitor.sh it'll run through the whole file and then update every 15 minutes. You can canncel it by doing CTRL+C.


