# install mysql connect with pip3 (on ubuntu for python 3)
# here installing globally without a virtual environment
# sudo -H pip3 install --upgrade pip
# sudo -H pip3 install mysqlclient

import MySQLdb as mysql

db = mysql.connect(host="localhost", user="root", passwd="password", db="mydb")

cur = db.cursor()

cur.execute("SELECT * FROM my_table")

for row in cur.fetchall():
    print(row[0])

db.close()
