import re
import collections
import os
import mysql.connector
import sys

# Connect to server
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="kali",
    password="kali",
    database="mysql")

# Get a cursor
cur = cnx.cursor()

filepath = sys.argv[1]

if os.path.exists(filepath):
    pass
else:
    print("File does not exist try again")
    exit()

# Get IP addressess that had at least one invalid login
def log_file_reader(filepath):
    with open(filepath) as f:
        log = f.read()
        regex = r'Invalid[a-z ]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        ip_list = re.findall(regex, log)
        return ip_list
    
# Get total count of invalid logins and sort ascending
def count_ip(ip_list):
    return dict(sorted(collections.Counter(ip_list).items(), key=lambda x:x[1], reverse=True))

#Write IPs and number of failed logins to database
def write_to_database(counter):
        print("Writing IPs and Failed_login_attempts to IP_RATING table ...")
        for item in counter:
            query = "INSERT INTO IP_RATING (IP, FAILED_LOGINS) VALUES (%s, %s);"
            cur.execute(query, (item, counter[item]))

write_to_database(count_ip(log_file_reader(filepath)))

try:
	cnx.commit()
except:
	cnx.rollback()

cnx.close()

