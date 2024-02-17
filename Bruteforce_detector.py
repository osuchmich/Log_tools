from datetime import datetime, timedelta
import os
import mysql.connector

# Connect to server
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="kali",
    password="kali",
    database="mysql")

# Get a cursor
cur = cnx.cursor()

filepath = 'tmp.txt'

if os.path.exists(filepath):
    pass
else:
    print("File does not exist try again")
    exit()
    
#Getting RATING_ID from IP_RATING table
def get_rating_id(IP):
    cur.execute("SELECT RATING_ID FROM IP_RATING WHERE IP = '%s';" % IP)
    return cur.fetchone()

# Read the lines in the parsed log
def get_failed_logins(filepath):
    failed_logins=[]
    f = open(filepath, 'r')
    for line in f:
        log = line
        failed_logins.append(log)
    f.close()
    return failed_logins

#Convert and strip log lines into 2d-list [[datetime,IP Address]]
def get_time_and_ip(failed_logins):
    tmp = ''
    time_and_ip_list = []
    l = []
    for line in failed_logins:
        splitted_line = line.split()
        for i in range(3):
            tmp += splitted_line[i]
            tmp += " "
        
        l.append(datetime.strptime(tmp,"%b %d %H:%M:%S "))
        l.append(splitted_line[len(splitted_line)-1])
        time_and_ip_list.append(l)
        l=[]
        tmp=''

    return sorted(time_and_ip_list)

# Detecting Bruteforce by iterating through IPs and searching for failed logins from the same IP in ten minutes
def detect_Bruteforce(time_and_ip_list):
    ten_minutes = timedelta(minutes=10)
    k=1
    counter_of_failed_logins = 0
    flagged_ip = ''
    index_of_time_end_of_attack = 0
    start_of_attack = False
    for i in range(len(time_and_ip_list)-1):
        time=time_and_ip_list[i][0]
        ip=time_and_ip_list[i][1]

        while time_and_ip_list[i+k][0] - time < ten_minutes:
            if time_and_ip_list[i][1] == time_and_ip_list[i+k][1] :
                counter_of_failed_logins+=1
                index_of_time_end_of_attack = i+k # saving the last index that was caught in order to roughly tell when the attack has ended (i will be one log after the last failed login)
            k+=1
            if i+k > len(time_and_ip_list)-1:
                break
        
        if counter_of_failed_logins > 6: # if there are more than 6 logins in 10 minutes script realizes that the attack has started
            if flagged_ip == ip:
                pass
            else:
                start_of_attack = True
                print("Bruteforce attack detected at "+f"{time_and_ip_list[i][0]:%b %d %H:%M:%S}")
                flagged_ip = ip
                query = "INSERT INTO BRUTE_FORCE (RATING_ID, IP, START) VALUES ({0}, '{1}', '{2}');"
                cur.execute(query.format(get_rating_id(flagged_ip)[0], flagged_ip, f"{time_and_ip_list[i][0]:%b %d %H:%M:%S}")) # writing the IP, RATING_IP(from IP_RATING table) and start of attack to BRUTE_FORCE table
        elif flagged_ip != ip and start_of_attack == True:
            query = "UPDATE BRUTE_FORCE SET END = '{0}' WHERE IP = '{1}'"
            cur.execute(query.format(f"{time_and_ip_list[index_of_time_end_of_attack][0]:%b %d %H:%M:%S}", flagged_ip)) # writing the end of the brute force attack to BRUTE_FORCE table
            start_of_attack = False
        
        k=1
        counter_of_failed_logins = 0

detect_Bruteforce(get_time_and_ip(get_failed_logins(filepath)))

cnx.commit()

# Close connection
cnx.close()

exit()

