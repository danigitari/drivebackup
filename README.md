1.clone https://github.com/danigitari/drivebackup.git
2.make sure python is installed and added to path in the host computer
3.makesure the scripts folder in pthon is also setup to path to allow usage of the pip command on the terminal
4.go into the rivebackup folder and open a command prompt terminal
5.type powershell to get into a powershell terminal
6.copy and paste the following intented lines.
  pip install python-dotenv
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
7.now edit the dot env file the sender email is the up dev account email, the password is the up dev account
8.password an the client name is the name of the client.
9.now edit the drive backup.py file .. on line 82 fillup the reciever email as support@uzapoint.com or as
 directed by uzapoint staff.
10.create a folder on the updev account google drive account copy the folder id on the url and paste it
 on the folder_id variable on line 56 of the drivebackup.py file.
   
11.edit the dbdump file ..edit the file to make sure the mysql credentials are those od the host machine. 
in the os.popen line edit the dbuser which will be filled in as 'sevens_abc' to the db_user of the host
machine but leave the backup as it is.
12.now run the dbdumb to generate the backup.sql and then the drivebackup which will redirect u to the browser
..follow the steps it takes u through and make sure the file is backed up in google drive.
12. Setup sysem scheduler ..test if it works then thats it



