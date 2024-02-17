import mysql.connector

# Connect to server
cnx = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="user",
    password="password",
    database="mysql")

# Get a cursor
cur = cnx.cursor()

# Dropping IP_RATING table if already exists.
cur.execute("DROP TABLE IF EXISTS BRUTE_FORCE")
cur.execute("DROP TABLE IF EXISTS IP_RATING")

#Creating IP_rating table
sql = '''CREATE TABLE IP_RATING(
	RATING_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	IP CHAR(20) NOT NULL,
	FAILED_LOGINS INT,
	COUNTRY CHAR(20)
)'''

sql2 = '''CREATE TABLE BRUTE_FORCE(
	ATTACK_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	RATING_ID INT NOT NULL,
	IP CHAR (20) NOT NULL,
	START CHAR(20),
	END CHAR(20),
	FOREIGN KEY (RATING_ID) REFERENCES IP_RATING(RATING_ID) on delete cascade
)'''
print("Creating databases...")
cur.execute(sql)
cur.execute(sql2)

# Close connection
cnx.close()
