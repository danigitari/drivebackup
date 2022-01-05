import os

HOST='localhost'
PORT='3306'
DB_USER='root'
DB_PASS='UPSupport2021'

os.popen("mysqldump -h %s -P %s -u %s -p%s %s > %s.sql" % (HOST,PORT,DB_USER,DB_PASS,'sevens_abc','backup'))