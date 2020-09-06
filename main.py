import os, random
import pymongo 
import re
from emailbasics.emailbasics import emailcheck
# clientm = os.getenv("clientm")
clientm = emailcheck()
hello = pymongo.MongoClient(clientm)
import dns
import getkey
from time import sleep
bold = "\033[1m"
reset='\033[0m'
def convert(lst): 
    return ' '.join(lst).split()

def index_in_list(a_list, index):
    return index < len(a_list)

def checkpass(username):
  db = hello["AllUsers"]
  mycol = db["userpass"]
  for doc in mycol.find({}, { "_id": 0, "Username": 1, "Password": 1}):
    x = "'" + str(doc) + "'"
    y = re.sub(r'[^\w\s]','',x)
    lst = [y] 
    d = convert(lst)
    someusername = d[1]
    if username == someusername:
      password = d[3]
      return password

def checkuser(username):
  db = hello["AllUsers"]
  mycol = db["userpass"]
  allusers = []
  for doc in mycol.find({}, { "_id": 0, "Username": 1}):
    xx = str(doc)
    xx = xx.replace("'_id': ", "")
    xx = xx.replace("'Username': ", "")
    xx = xx.replace("'", "")
    xx = xx.replace(",", "")
    xx = xx.replace("{", "")
    xx = xx.replace("}", "")
    allusers.append(xx)
  if username in allusers:
    return True

def login():
  os.system("clear")
  username = input("What is your username?\n")
  hello = checkuser(username)
  if hello == True:
    password = input("What is your password?\n")
    realpass = checkpass(username)
    if password == realpass:
      print("You have logged in!")
      sleep(3)
      return username
    else:
      print("Wrong password!")
      sleep(3)
      return False
  else:
    print("That is not a real username. Maybe you accidently added your tag?")
    return False
def signup():
  os.system("clear")
  username = input("What do you want your username to be?\n")
  db = hello.Inboxes
  collist = db.list_collection_names()
  usernames = []
  for i in collist:
    allletter = list(i)
    allletter.pop(-1)
    allletter.pop(-1)
    allletter.pop(-1)
    allletter.pop(-1)
    allletter.pop(-1)
    allletter.pop(-1)
    allletter.pop(-1)
    thatusername = ""
    for i in allletter:
      thatusername = thatusername + i
    usernames.append(thatusername)
  while username in usernames:
    print("That is already a username! You have to choose another username!")
    username = input("What do you want your username to be?\n")
  while " " in username:
    print("You cannot have a space in your username!")
    username = input("What do you want your username to be?\n")
  password = input("What do you want your password to be?\n")
  while " " in password:
    print("You cannot have a space in your password!")
    password = input("What do you want your password to be?\n")
  while "'" in username:
    print("You cannot have an apostrophe in your username!")
    username = input("What do you want your username to be?\n")
  while "'" in password:
    print("You cannot have a apostrophe in your password!")
    password = input("What do you want your password to be?\n")
  while '"' in username:
    print("You cannot have speech marks in your username!")
    username = input("What do you want your username to be?\n")  
  while '"' in password:
    print("You cannot have speech marks in your password!")
    password = input("What do you want your password to be?\n")  
  tag = ""
  for i in range(6):
    number = random.randint(0,9)
    tag = tag + str(number)
  username2 = username + ":" + tag
  print("If you signup, your username will be and tag will be " + username2 + "\nJust to prevent cyber bullies to bully you online, you have a tag, so if people cannot message you if they do not know your tag.\nBut remember, to login, you will only enter your username, not your username with your tag.\n")
  makeaccount = input("Type in agree to agree to all the rules, and make the account.\n")
  if makeaccount.lower() == "agree":
    db = hello.AllUsers
    mycol = db.userpass
    document = [{
      "Username": username,
      "Password": password
    }]
    mycol.insert_many(document)
    DB = hello.Inboxes
    MYCOL = DB[username2]
    randomid = ""
    for i in range(15):
      number = random.randint(0,9)
      randomid = str(number) + randomid
    DOCUMENT = [{
      "_id": int(randomid),
      "Title": "Welcome to FRANK!",
      "Body": "FRANK is a secure messaging service!",
      "From": "FRANK Team"
    }]
    MYCOL.insert_many(DOCUMENT)
    print("Account made!")
    sleep(3)
    return True
  else:
    print("You don't want to make a FRANK account? Okay. If you feel like making one later, come back!")
    sleep(3)
    return False
  
def sendmail(userandtag):
  sendto = input("Who do you want to send an email to?\nYou need to enter their username and tag\n")
  db = hello.Inboxes
  collist = db.list_collection_names()
  if sendto in collist:
    title = input("What do you want the title to be?\n")
    body = input("What do you want the body of the mail to be?\n")
    DB = hello["Inboxes"]
    MYCOL = DB[sendto]
    allids = []
    for doc in MYCOL.find({}, { "_id": 1}):
      xx = str(doc)
      xx = xx.replace("'_id': ")
      xx = int(xx)
      allids.append(xx)
    randomid = ""
    for i in range(15):
      number = random.randint(0,9)
      randomid = str(number) + randomid
    while int(randomid) in allids:
      randomid = ""
      for i in range(15):
        number = random.randint(0,9)
        randomid = str(number) + randomid
    DOCUMENT = [{
      "_id": int(randomid),
      "Title": title,
      "Body": body,
      "From": userandtag
    }]
    MYCOL.insert_many(DOCUMENT)
    print("Email sent!")
  else:
    print("That is not a real user!")
    
def checktag(username):
  db = hello.Inboxes
  collist = db.list_collection_names()
  for i in collist:
    if username in i:
      usernameandtag = i
      return usernameandtag

def inbox(userandtag):
  x = 1
  db = hello["Inboxes"]
  mycol = db[userandtag]
  emails = False
  for doc in mycol.find({}, { "_id": 0, "Title": 1, "Body": 1, "From": 1}):
    xx = str(doc)
    xx = xx.replace("'_id': ", "")
    xx = xx.replace("'Title': ", "")
    xx = xx.replace("'Body': ", "")
    xx = xx.replace("'From': ", "")
    xx = xx.replace("{", "")
    xx = xx.replace("}", "")
    everything = xx.split(", ")
    title1 = everything[0]
    titleall = list(title1)
    if titleall[0] == "'" or titleall[0] == '"':
      titleall.pop(0)
    if titleall[-1] == "'" or titleall[-1] == '"':
      titleall.pop(-1)
    title = ""
    for i in titleall:
      title = title + i
    body1 = everything[1]
    bodyall = list(body1)
    if bodyall[0] == "'" or bodyall[0] == '"':
      bodyall.pop(0)
    if bodyall[-1] == "'" or bodyall[-1] == '"':
      bodyall.pop(-1)
    body = ""
    for i in bodyall:
      body = body + i
    fromuser1 = everything[2]
    fromuserall = list(fromuser1)
    if fromuserall[0] == "'" or fromuserall[0] == '"':
      fromuserall.pop(0)
    if fromuserall[-1] == "'" or fromuserall[-1] == '"':
      fromuserall.pop(-1)
    fromuser = ""
    for i in fromuserall:
      fromuser = fromuser + i
    print("Email no. " + str(x))
    print("By: " + fromuser)
    print(bold + title)
    print(reset + body)
    print("")
    x = x + 1
    emails = True
  if emails == False:
    print("You have no emails!")
def deletemail(userandtag):
  inbox(userandtag)
  db = hello["Inboxes"]
  mycol = db[userandtag]
  allemails = []
  for doc in mycol.find({}, { "_id": 1}):
    xx = str(doc)
    xx = xx.replace("'_id': ", "")
    xx = xx.replace("{", "")
    xx = xx.replace("}", "")
    allemails.append(int(xx))
  email = input("Enter the number of the email you want to delete\n")
  try:
    emailno = int(email) - 1
    while index_in_list(allemails, emailno) == False:
      print("That is not a real email number!")
      email = input("Enter the number of the email you want to delete\n")
      emailno = int(email) - 1
    deleteid = allemails[emailno]
    myquery = {"_id": deleteid}
    mycol.delete_one(myquery)
    print("Email deleted!")
  except:
    print("This isn't a number!")

def logged(userandtag):
  while True:
    os.system("clear")
    print("Logged in as " + userandtag)
    print("1. Check inbox")
    print("2. Send email")
    print("3. Delete email")
    print("4. Logout")
    choice = input("Enter the command number you want to do\n")
    if choice == "1":
      os.system("clear")
      inbox(userandtag)
      print("\nPress any key to go back to the main menu")
      getkey.getkey()
    if choice == "2":
      os.system("clear")
      sendmail(userandtag)
      print("\nPress any key to go back to the main menu")
      getkey.getkey()
    if choice == "3":
      os.system("clear")
      deletemail(userandtag)
      print("\nPress any key to go back to the main menu")
      getkey.getkey()
    if choice == "4":
      os.system("clear")
      print("You have logged out!")
      return "Logout"
    
def main():
  print("1. Signup")
  print("2. Login")
  command = input("Enter the command you want to do\n")
  if command == "1":
    sign = signup()
    if sign == True:
      log = login()
      if log is not False:
        print(log)
        userandtag = checktag(log)
        menu = logged(userandtag)
        if menu == "Logout":
          return "Logged out"
      
  elif command == "2":
    log = login()
    if log is not False:
      print(log)
      userandtag = checktag(log)
      menu = logged(userandtag)
      if menu == "Logout":
        return "Logged out"
        
  else:
    print("That is not a command!")
    sleep(2)
    os.system("clear")
    main()
main()