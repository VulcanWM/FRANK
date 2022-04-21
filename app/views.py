from app import app
from flask import url_for, render_template, send_file, request, redirect
from asyncio import run, sleep
import pymongo
import os
import re
import random
clientm = os.getenv("clientm")
mongoclient = pymongo.MongoClient(clientm)


def checktag(username):
  db = mongoclient.Inboxes
  collist = db.list_collection_names()
  for ok in collist:
    something = list(ok)
    del something[-1]
    del something[-1]
    del something[-1]
    del something[-1]
    del something[-1]
    del something[-1]
    del something[-1]
    seperator = ""
    user = seperator.join(something)
    if username == user:
      usernameandtag = ok
      return usernameandtag


def testflask(userandtag):
  db = mongoclient["Inboxes"]
  mycol = db[userandtag]
  emails = False
  variable = []
  for doc in mycol.find({}, {"_id": 1, "Title": 1, "Body": 1, "From": 1}):
    variable.append(doc)
    emails = True
  if emails == False:
    variable = "NOEMAIL"

  return variable


@app.route('/')
def index():
  return render_template("main.html")


@app.route('/login')
def login():
  return render_template("login.html", text="")


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404


@app.route('/login', methods=['POST', 'GET'])
def loginemail():
  if request.method == "POST":
    username = request.form['name']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)

    if username not in allusers:
      return render_template(
          "login.html", text="That is not a real username!")
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    for doc in mycol.find({}, {"_id": 0, "Username": 1, "Password": 1}):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
    if password == passwordnew:
      userandtag = checktag(username)
      variable = testflask(userandtag)
      return render_template(
          "index.html", value=variable, userandtag=userandtag, text="")
    else:
      return render_template("login.html", text="Wrong password!")


@app.route('/signup')
def signup():
  return render_template("signup.html", text="")


@app.route('/signup', methods=['POST', 'GET'])
def signupdef():
  if request.method == "POST":
    username = request.form['name']
    password = request.form['password']
    db = mongoclient.Inboxes
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
    if username in usernames:
      return render_template(
          "signup.html",
          text=
          "That is already a username, you have to choose another username!"
      )
    if " " in username:
      return render_template(
          "signup.html",
          text="You cannot have a space in your username!")
    if " " in password:
      return render_template(
          "signup.html",
          text="You cannot have a space in your password!")
    if "'" in username:
      return render_template(
          "signup.html",
          text="You cannot have an apostrophe in your username!")
    if "'" in password:
      return render_template(
          "signup.html",
          text="You cannot have an apostrophe in your username!")
    if '"' in username:
      return render_template(
          "signup.html",
          text="You cannot have a speech mark in your username!")
    if '"' in password:
      return render_template(
          "signup.html",
          text="You cannot have a speech mark in your password!")
    tag = ""
    for i in range(6):
      number = random.randint(0, 9)
      tag = tag + str(number)
    username2 = username + ":" + tag
    db = mongoclient.AllUsers
    mycol = db.userpass
    document = [{
        "Username": username,
        "Password": password,
        "Votes": 0,
        "Description": "",
        "Admin": False,
        "MOD": False,
        "discordusername": "",
        "statusdiscordusername": "NODISCORDUSERNAME"
    }]
    mycol.insert_many(document)
    DB = mongoclient.Inboxes
    MYCOL = DB[username2]
    randomid = ""
    for i in range(15):
      number = random.randint(0, 9)
      randomid = str(number) + randomid
    DOCUMENT = [{
        "_id": int(randomid),
        "Title": "Welcome to FRANK!",
        "Body": "FRANK is a secure messaging service!",
        "From": "FRANK Team"
    }]
    MYCOL.insert_many(DOCUMENT)
    variable = testflask(username2)
    return render_template(
        "index.html", value=variable, userandtag=username2, text="")


@app.route('/sendmail')
def sendmailalways():
  return render_template("sendmail.html", text="")


@app.route('/sendmail', methods=['POST', 'GET'])
def sendmail():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "sendmail.html", text="That is not a real username!")
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    for doc in mycol.find({}, {"_id": 0, "Username": 1, "Password": 1}):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
    if password == passwordnew:
      userandtag = checktag(username)
      variable = testflask(userandtag)
    else:
      return render_template("sendmail.html", text="Wrong password!")
    #############
    sendto = request.form['sendto']
    db = mongoclient.Inboxes
    collist = db.list_collection_names()
    if sendto in collist:
      title = request.form['title']
      body = request.form['body']
      DB = mongoclient["Inboxes"]
      MYCOL = DB[sendto]
      allids = []
      for doc in MYCOL.find({}, {"_id": 1}):
        xx = doc['_id']
        allids.append(xx)
      randomid = ""
      for i in range(15):
        number = random.randint(0, 9)
        randomid = str(number) + randomid
      while int(randomid) in allids:
        randomid = ""
        for i in range(15):
          number = random.randint(0, 9)
          randomid = str(number) + randomid
      DOCUMENT = [{
          "_id": int(randomid),
          "Title": title,
          "Body": body,
          "From": userandtag
      }]
      MYCOL.insert_many(DOCUMENT)
      return render_template(
          "index.html",
          value=variable,
          userandtag=userandtag,
          text=
          "Email sent. If the user you sent to logs in now, they will see the email."
      )
    else:
      return render_template(
          "sendmail.html", text="That is not a real user!")


@app.route('/deletemail')
def deletemailroot():
  return render_template("deletemail.html", text="")


@app.route('/deletemail', methods=['POST', 'GET'])
def deletemail():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "deletemail.html", text="That is not a real username!")
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    for doc in mycol.find({}, {"_id": 0, "Username": 1, "Password": 1}):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
    if password == passwordnew:
      userandtag = checktag(username)
      variable = testflask(userandtag)
    else:
      return render_template("deletemail.html", text="Wrong password!")
    db = mongoclient["Inboxes"]
    mycol = db[userandtag]
    allemails = []
    for doc in mycol.find({}, {"_id": 1}):
      something = doc['_id']
      allemails.append(something)
    emailid = int(request.form['id'])
    if emailid not in allemails:
      return render_template(
          "deletemail.html",
          text="You don't have that email id in your emails!")
    myquery = {"_id": emailid}
    mycol.delete_one(myquery)
    return render_template(
        "index.html",
        value=variable,
        userandtag=userandtag,
        text=
        "Email deleted. If you log out and log in now, you will see that the email has been deleted"
    )


@app.route("/makethread")
def makethreadmain():
  return render_template("makethread.html", text="")


@app.route("/makethread", methods=['POST', 'GET'])
def makethread():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "makethread.html", text="That is not a real username!")
    for doc in mycol.find({}, {"_id": 0, "Username": 1, "Password": 1}):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
    if password == passwordnew:
      userandtag = checktag(username)
    else:
      return render_template("makethread.html", text="Wrong password!")
    db = mongoclient.Threads
    mycol = db.Community
    title = request.form['title']
    body = request.form['body']
    allids = []
    for doc in mycol.find({}, {"_id": 1}):
      xx = doc['_id']
      allids.append(xx)
    randomid = ""
    for i in range(15):
      number = random.randint(0, 9)
      randomid = str(number) + randomid
    while int(randomid) in allids:
      randomid = ""
      for i in range(15):
        number = random.randint(0, 9)
        randomid = str(number) + randomid
    document = [{
        '_id': int(randomid),
        'Title': title,
        'Body': body,
        'Author': userandtag,
        "Votes": 0,
        "Voteslist": []
    }]
    mycol.insert_many(document)
    url = "https://frank.vulcanwm.com/threads/" + randomid
    print(url)
    log = username + " made a thread!"
    db = mongoclient["Logs"]
    mycol = db["Logs"]
    document = [{
      "Type": "Thread",
      "Log": log,
      "Url": url
    }]
    mycol.insert_many(document)
    return redirect(url)


@app.route('/threads/<threadid>')
def checkthread(threadid):
  db = mongoclient.Threads
  mycol = db.Community
  allids = []
  for doc in mycol.find({}, {"_id": 1}):
    xx = doc['_id']
    allids.append(xx)
  if int(threadid) in allids:
    for something in mycol.find({}, {
        "_id": 1,
        "Title": 1,
        "Body": 1,
        "Author": 1,
        "Votes": 1,
        "Voteslist": 1
    }):
      author = something['Author']
      del something['Author']
      author = list(author)
      del author[-1]
      del author[-1]
      del author[-1]
      del author[-1]
      del author[-1]
      del author[-1]
      del author[-1]
      seperator = ""
      author = seperator.join(author)
      something['Author'] = author
      if something['_id'] == int(threadid):
        variable = something
        return render_template("thread.html", dictname=variable)
  else:
    return render_template("404.html")


@app.route("/allthreads")
def allthreads():
  db = mongoclient.Threads
  mycol = db.Community
  alldicts = []
  for doc in mycol.find({}, {
      "_id": 1,
      "Title": 1,
      "Body": 1,
      "Author": 1,
      "Votes": 1
  }).sort("Votes", -1):
    theid = doc["_id"]
    url = "https://frank.vulcanwm.com/threads/" + str(theid)
    del doc['_id']
    doc['Url'] = url
    author = doc['Author']
    del doc['Author']
    author = list(author)
    del author[-1]
    del author[-1]
    del author[-1]
    del author[-1]
    del author[-1]
    del author[-1]
    del author[-1]
    seperator = ""
    author = seperator.join(author)
    doc['Author'] = author
    title = doc['Title']
    del doc['Title']
    if len(title) > 10:
      title = title[ 0 : 10 ]
      title = title + "..."
    doc['Title'] = title
    alldicts.append(doc)
  if alldicts == []:
    alldicts = "NO"
  return render_template("allthreads.html", somelist=alldicts)


@app.route("/users/<username>")
def userprof(username):
  db = mongoclient.AllUsers
  allcol = db.userpass
  allusers = []
  for doc in allcol.find({}, {"_id": 0, "Username": 1}):
    theusername = doc['Username']
    allusers.append(theusername)
  if username in allusers:
    user = {}
    user['userandtag'] = username
    userandtag = checktag(username)
    DB = mongoclient.Threads
    MYCOL = DB.Community
    threads = 0
    for doc in MYCOL.find({}, {"_id": 0, "Author": 1}):
      author = doc['Author']
      if author == userandtag:
        threads = threads + 1
    user['threadnumber'] = threads
    something = mongoclient.AllUsers
    themycol = something.userpass
    for doc in themycol.find({}, {
        "_id": 0,
        "Username": 1,
        "Description": 1,
        "Admin": 1,
        "MOD": 1,
        "Votes": 1
    }):
      if doc['Username'] == username:
        desc = doc['Description']
        user['Description'] = desc
        admin = doc['Admin']
        user['Admin'] = admin
        MOD = doc['MOD']
        user['MOD'] = MOD
        votes = doc['Votes']
        user['Votes'] = votes
    return render_template("user.html", user=user)
  else:
    return render_template("404.html")


@app.route("/changedesc")
def changedesc():
  return render_template("changedesc.html", text="")


@app.route("/changedesc", methods=['POST', 'GET'])
def changedescmain():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "changedesc.html", text="That is not a real username!")
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    for doc in mycol.find({}, {
        "_id": 1,
        "Username": 1,
        "Password": 1,
        "Votes": 1,
        "Admin": 1,
        "MOD": 1,
        "discordusername": 1,
        "statusdiscordusername": 1
    }):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          theid = doc['_id']
          votes = doc['Votes']
          admin = doc['Admin']
          mod = doc['MOD']
          discordusername = doc['discordusername']
          statusdiscordusername = doc["statusdiscordusername"]
        else:
          return render_template(
              "changedesc.html", text="Wrong password!")
    DB = mongoclient.AllUsers
    MYCOL = DB.userpass
    description = request.form['description']
    delete = {"_id": theid}
    MYCOL.delete_one(delete)
    document = [{
        "Username": username,
        "Password": password,
        "Votes": votes,
        "Description": description,
        "Admin": admin,
        "MOD": mod,
        "discordusername": discordusername,
        "statusdiscordusername": statusdiscordusername
    }]
    MYCOL.insert_many(document)
    return redirect("https://frank.vulcanwm.com/users/" + username)


@app.route("/changepass")
def changepassmain():
  return render_template("changepass.html", text="")


@app.route("/changepass", methods=['POST', 'GET'])
def changepass():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "changepass.html", text="That is not a real username!")
    for doc in mycol.find({}, {
        "_id": 1,
        "Username": 1,
        "Password": 1,
        "Votes": 1,
        "Admin": 1,
        "Description": 1,
        "MOD": 1,
        "discordusername": 1,
        "statusdiscordusername": 1
    }):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          theid = doc['_id']
          votes = doc['Votes']
          admin = doc['Admin']
          mod = doc['MOD']
          desc = doc['Description']
          authordiscordusername = doc['discordusername']
          authorstatusdiscordusername = doc["statusdiscordusername"]
          userandtag = checktag(username)
        else:
          return render_template(
              "changepass.html", text="Wrong password!")
    newpass = request.form['newpassword']
    delete = {"_id": theid}
    mycol.delete_one(delete)
    document = [{
        "Username": username,
        "Password": newpass,
        "Votes": votes,
        "Description": desc,
        "Admin": admin,
        "MOD": mod,
        "discordusername": authordiscordusername,
        "statusdiscordusername": authorstatusdiscordusername
    }]
    mycol.insert_many(document)
    variable = testflask(userandtag)
    return render_template(
        "index.html",
        text=
        "Your password has been changed. The next time you log in, you will have to log in with your new password.",
        userandtag=userandtag,
        value=variable)


@app.route("/deleteaccount")
def deleteaccountmain():
  return render_template("deleteaccount.html", text="")


@app.route("/deleteaccount", methods=['POST', 'GET'])
def deleteaccount():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "changepass.html", text="That is not a real username!")
    for doc in mycol.find({}, {"_id": 1, "Username": 1, "Password": 1}):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          theid = doc['_id']
          userandtag = checktag(username)
        else:
          return render_template(
              "changepass.html", text="Wrong password!")
    delete = {"_id": theid}
    mycol.delete_one(delete)
    DB = mongoclient.Inboxes
    MYCOL = DB[userandtag]
    MYCOL.drop()
    thedb = mongoclient.Threads
    thecol = thedb.Community
    for doc in thecol.find({}, {"_id": 1, "Author": 1}):
      docid = doc['_id']
      docauthor = doc['Author']
      if docauthor == userandtag:
        delete = {"_id": docid}
        thecol.delete_one(delete)
    mainclient = os.getenv("mainclient")
    mainclient = pymongo.MongoClient(mainclient)
    db = mainclient.Blogs
    mycol = db[userandtag]
    mycol.drop()
    return render_template(
        "main.html",
        text=
        "Your account has been successfully deleted. All your threads, fmails and have also been deleted."
    )


@app.route("/deletethread")
def deletethreadmain():
  return render_template("deletethread.html", text="")


@app.route("/deletethread", methods=['POST', 'GET'])
def deletethread():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "deletethread.html", text="That is not a real username!")
    for doc in mycol.find({}, {
        "_id": 0,
        "Username": 1,
        "Password": 1,
        "Admin": 1
    }):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          userandtag = checktag(username)
          admin = doc['Admin']
        else:
          return render_template(
              "deletethread.html", text="Wrong password!")
    print("Got up to checking the username")
    threadid = int(request.form['id'])
    DB = mongoclient.Threads
    MYCOL = DB.Community
    ids = []
    for thread in MYCOL.find({}, {"_id": 1}):
      thisid = thread['_id']
      ids.append(thisid)
    if int(threadid) in ids:
      print("Checked that this thread is a real thread!")
      for thread in MYCOL.find({}, {"_id": 1, "Author": 1, "Votes": 1}):
        randomid = thread['_id']
        threadvotes = thread['Votes']
        if randomid == threadid:
          print("This is the thread!")
          author = thread['Author']
          justauthor = list(author)
          del justauthor[-1]
          del justauthor[-1]
          del justauthor[-1]
          del justauthor[-1]
          del justauthor[-1]
          del justauthor[-1]
          del justauthor[-1]
          seperator = ""
          seperator.join(justauthor)
          justauthor2 = ""
          for i in justauthor:
            justauthor2 = justauthor2 + i
          justauthor = justauthor2
          for user in mycol.find({}, {
              "_id": 1,
              "Username": 1,
              "Password": 1,
              "Votes": 1,
              "Description": 1,
              "Admin": 1,
              "MOD": 1,
              "discordusername": 1,
              "statusdiscordusername": 1
          }):
            if doc['Username'] == justauthor:
              userid = user['_id']
              uservotes = user['Votes']
              uservotes = uservotes - threadvotes
              userpass = user['Password']
              userusername = user['Username']
              userdesc = user['Description']
              useradmin = user['Admin']
              userMOD = user['MOD']
              userdiscordusername = user['discordusername']
              userstatusdiscordusername = user[
                  "statusdiscordusername"]
          if author == userandtag:
            for user in mycol.find({}, {
              "_id": 1,
              "Username": 1,
              "Password": 1,
              "Votes": 1,
              "Description": 1,
              "Admin": 1,
              "MOD": 1,
              "discordusername": 1,
              "statusdiscordusername": 1
          }):
              if doc['Username'] == justauthor:
                theuserid = user['_id']
                uservotes = user['Votes']
                uservotes = uservotes - threadvotes
                userpass = user['Password']
                userusername = user['Username']
                userdesc = user['Description']
                useradmin = user['Admin']
                userMOD = user['MOD']
                userdiscordusername = user['discordusername']
                userstatusdiscordusername = user[
                  "statusdiscordusername"]
            delete = {"_id": threadid}
            MYCOL.delete_one(delete)
            deleteuser = {"_id": theuserid}
            mycol.delete_one(deleteuser)
            print("Deleted the old profile")
            userdocument = [{
                "Username":
                userusername,
                "Password":
                userpass,
                "Votes":
                uservotes,
                "Description":
                userdesc,
                "Admin":
                useradmin,
                "MOD":
                userMOD,
                "discordusername":
                userdiscordusername,
                "statusdiscordusername":
                userstatusdiscordusername
            }]
            mycol.insert_many(userdocument)
            print("Added the new user profile")
            return render_template(
                "main.html",
                text="The thread has been successfully deleted!")
          elif admin == True:
            author = list(author)
            del author[-1]
            del author[-1]
            del author[-1]
            del author[-1]
            del author[-1]
            del author[-1]
            del author[-1]
            author2 = ""
            for i in author:
              author2 = author2 + i
            author = author2
            for doc in mycol.find({}, {
                "_id": 0,
                "Username": 1,
                "Admin": 1,
                "Votes": 1
            }):
              uservotes = doc['Votes']
              if doc['Username'] == author:
                if doc['Admin'] == True:
                  return render_template(
                      "deletethread.html",
                      text=
                      "The author of that thread is an admin! You cannot delete an admin's thread!"
                  )
                else:
                  delete = {"_id": threadid}
                  MYCOL.delete_one(delete)
                  return render_template(
                      "main.html",
                      text=
                      "The thread has been successfully deleted!"
                  )
                  deleteuser = {"_id": userid}
                  mycol.delete_one(deleteuser)
                  print("Deleted old profile")
                  userdocument = [{
                      "Username":
                      userusername,
                      "Password":
                      userpass,
                      "Votes":
                      uservotes,
                      "Description":
                      userdesc,
                      "Admin":
                      useradmin,
                      "MOD":
                      userMOD,
                      "discordusername":
                      userdiscordusername,
                      "statusdiscordusername":
                      userstatusdiscordusername
                  }]
                  mycol.insert_many(userdocument)
                  print("Inserted new profile")
          else:
            return render_template(
                "deletethread.html",
                text="You cannot delete this thread!")
    else:
      return render_template(
          "deletethread.html", text="That is not a real thread!")


@app.route("/likethread")
def likethreadmain():
  return render_template("likethread.html")


@app.route("/likethread", methods=['POST', 'GET'])
def likethread():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "likethread.html", text="That is not a real username!")
    for doc in mycol.find({}, {
        "_id": 0,
        "Username": 1,
        "Password": 1,
        "Votes": 1,
        "Description": 1,
        "Admin": 1,
        "MOD": 1,
        "discordusername": 1,
        "statusdiscordusername": 1
    }):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          userandtag = checktag(username)
        else:
          return render_template(
              "likethread.html", text="Wrong password!")
    threadid = int(request.form['id'])
    DB = mongoclient.Threads
    MYCOL = DB.Community
    ids = []
    for thread in MYCOL.find({}, {"_id": 1, "Voteslist": 1}):
      thisid = thread['_id']
      ids.append(thisid)
    if int(threadid) in ids:
      if username in thread['Voteslist']:
        return render_template(
            "likethread.html",
            text="You cannot like a post more than once!")
    else:
      return render_template(
          "likethread.html", text="That is not a real thread!")
    for thread in MYCOL.find({}, {
        "_id": 1,
        "Author": 1,
        "Votes": 1,
        "Body": 1,
        "Title": 1,
        "Voteslist": 1
    }):
      randomid = thread['_id']
      if randomid == threadid:
        author = thread['Author']
        if author == userandtag:
          return render_template(
              "likethread.html",
              text="You cannot like your own thread!")
        else:
          title = thread['Title']
          body = thread['Body']
          votes = thread['Votes']
          voteslistwork = thread['Voteslist']
          voteslistwork.append(username)
          votes = votes + 1
          document = [{
              "_id": threadid,
              "Title": title,
              "Body": body,
              "Author": author,
              "Votes": votes,
              "Voteslist": voteslistwork
          }]
          delete = {"_id": threadid}
          MYCOL.delete_one(delete)
          MYCOL.insert_many(document)
          authorname = list(author)
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          authorname2 = ""
          for i in authorname:
            authorname2 = authorname2 + i
          authorname = authorname2
          for doc in mycol.find({}, {
              "_id": 1,
              "Username": 1,
              "Password": 1,
              "Votes": 1,
              "Description": 1,
              "Admin": 1,
              "MOD": 1,
              "discordusername": 1,
              "statusdiscordusername": 1
          }):
            someusername = doc['Username']
            print(someusername)
            if authorname == someusername:
              print(authorname)
              authorid = doc["_id"]
              authorpass = doc['Password']
              authorvotes = doc['Votes']
              authordesc = doc['Description']
              authoradmin = doc['Admin']
              authorMOD = doc['MOD']
              authordiscordusername = doc['discordusername']
              authorstatusdiscordusername = doc[
                  "statusdiscordusername"]
              authorvotes = authorvotes + 1
              authordelete = {"_id": authorid}
              mycol.delete_one(authordelete)
              document = [{
                  "Username":
                  authorname,
                  "Password":
                  authorpass,
                  "Votes":
                  authorvotes,
                  "Description":
                  authordesc,
                  "Admin":
                  authoradmin,
                  "MOD":
                  authorMOD,
                  "discordusername":
                  authordiscordusername,
                  "statusdiscordusername":
                  authorstatusdiscordusername
              }]
              mycol.insert_many(document)
              print("Added the new user profile")
              url = "https://frank.vulcanwm.com/threads/" + str(
                  threadid)
              return redirect(url)
            else:
              pass


@app.route("/unlikethread")
def unlikethreadmain():
  return render_template("unlikethread.html")


@app.route("/unlikethread", methods=['POST', 'GET'])
def unlikethread():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "unlikethread.html", text="That is not a real username!")
    for doc in mycol.find({}, {
        "_id": 0,
        "Username": 1,
        "Password": 1,
        "Votes": 1,
        "Description": 1,
        "Admin": 1,
        "MOD": 1,
        "discordusername": 1
    }):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          userandtag = checktag(username)
        else:
          return render_template(
              "unlikethread.html", text="Wrong password!")
    threadid = int(request.form['id'])
    DB = mongoclient.Threads
    MYCOL = DB.Community
    ids = []
    for thread in MYCOL.find({}, {"_id": 1, "Voteslist": 1}):
      thisid = thread['_id']
      ids.append(thisid)
    if int(threadid) in ids:
      if username in thread['Voteslist']:
        pass
      else:
        return render_template(
            "unlikethread.html", text="You haven't liked the thread!")
    else:
      return render_template(
          "deletethread.html", text="That is not a real thread!")
    for thread in MYCOL.find({}, {
        "_id": 1,
        "Author": 1,
        "Votes": 1,
        "Body": 1,
        "Title": 1,
        "Voteslist": 1
    }):
      randomid = thread['_id']
      if randomid == threadid:
        author = thread['Author']
        if author == userandtag:
          return render_template(
              "unlikethread.html",
              text="You cannot unlike your own thread!")
        else:
          title = thread['Title']
          body = thread['Body']
          votes = thread['Votes']
          voteslistwork = thread['Voteslist']
          voteslistwork.remove(username)
          votes = votes - 1
          document = [{
              "_id": threadid,
              "Title": title,
              "Body": body,
              "Author": author,
              "Votes": votes,
              "Voteslist": voteslistwork
          }]
          delete = {"_id": threadid}
          MYCOL.delete_one(delete)
          MYCOL.insert_many(document)
          authorname = list(author)
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          del authorname[-1]
          authorname2 = ""
          for i in authorname:
            authorname2 = authorname2 + i
          authorname = authorname2
          for doc in mycol.find({}, {
              "_id": 1,
              "Username": 1,
              "Password": 1,
              "Votes": 1,
              "Description": 1,
              "Admin": 1,
              "MOD": 1,
              "discordusername": 1,
              "statusdiscordusername": 1
          }):
            someusername = doc['Username']
            print(someusername)
            if authorname == someusername:
              print(authorname)
              authorid = doc["_id"]
              authorpass = doc['Password']
              authorvotes = doc['Votes']
              authordesc = doc['Description']
              authoradmin = doc['Admin']
              authorMOD = doc['MOD']
              authordiscordusername = doc['discordusername']
              userstatusdiscordusername = doc[
                  "statusdiscordusername"]
              authorvotes = authorvotes - 1
              authordelete = {"_id": authorid}
              mycol.delete_one(authordelete)
              document = [{
                  "Username":
                  authorname,
                  "Password":
                  authorpass,
                  "Votes":
                  authorvotes,
                  "Description":
                  authordesc,
                  "Admin":
                  authoradmin,
                  "MOD":
                  authorMOD,
                  "discordusername":
                  authordiscordusername,
                  "statusdiscordusername":
                  userstatusdiscordusername
              }]
              mycol.insert_many(document)
              print("Added the new user profile")
              url = "https://frank.vulcanwm.com/threads/" + str(
                  threadid)
              return redirect(url)
            else:
              pass


# @app.route("/adddiscordusername")
# def adddiscordusernamemain():
#   return render_template("adddiscordusername.html")


# @app.route("/adddiscordusername", methods=['POST', 'GET'])
# def adddiscordusername():
#   if request.method == "POST":
#     username = request.form['username']
#     password = request.form['password']
#     discordusername = request.form['discordusername']
#     db = mongoclient["AllUsers"]
#     mycol = db["userpass"]
#     allusers = []
#     for doc in mycol.find({}, {"_id": 0, "Username": 1}):
#       xx = doc['Username']
#       allusers.append(xx)
#     if username not in allusers:
#       return render_template(
#           "adddiscordusername.html", text="That is not a real username!")
#     for doc in mycol.find({}, {
#         "_id": 1,
#         "Username": 1,
#         "Password": 1,
#         "Votes": 1,
#         "Description": 1,
#         "Admin": 1,
#         "MOD": 1,
#         "discordusername": 1,
#         "statusdiscordusername": 1
#     }):
#       someusername = doc['Username']
#       if username == someusername:
#         passwordnew = doc['Password']
#         if password == passwordnew:
#           if doc['statusdiscordusername'] == "NODISCORDUSERNAME":
#             return render_template(
#                 "adddiscordusername.html",
#                 text=
#                 "You haven't done the first step of verification yet!"
#             )
#           else:
#             discordusernamereal = doc['discordusername']
#             if discordusername == discordusernamereal:
#               theusername = doc['Username']
#               thepassword = doc['Password']
#               thevotes = doc['Votes']
#               thevotes = thevotes + 10
#               thedesc = doc['Description']
#               theadmin = doc['Admin']
#               themod = doc['MOD']
#               theid = doc['_id']
#               delete = {"_id": theid}
#               mycol.delete_one(delete)
#               document = [{
#                   "Username":
#                   theusername,
#                   "Password":
#                   thepassword,
#                   "Votes":
#                   thevotes,
#                   "Description":
#                   thedesc,
#                   "Admin":
#                   theadmin,
#                   "MOD":
#                   themod,
#                   "discordusername":
#                   discordusername,
#                   "statusdiscordusername":
#                   "VERIFIEDDISCORDNAME"
#               }]
#               mycol.insert_many(document)
#               return render_template(
#                   "main.html",
#                   text="Your discord username has been verified! You also got 10 Wallers. Now go to #reaction-roles in the FRANK server, and react the Waller emoji to the verified account message, to get the verified account role"
#               )
#             else:
#               return render_template(
#                   "adddiscordusername.html",
#                   text=
#                   "Either somebody else did the first step of your verification, you are entering your discord username and tag instead of your discord user id or you are entering the wrong discord user id"
#               )
#               print('That is not the id your discord username')
#         else:
#           return render_template(
#               "adddiscordusername.html", text="Wrong password!")


@app.route("/addlink")
def addlinkmain():
  return render_template("addlink.html")


@app.route("/addlink", methods=['POST', 'GET'])
def addlink():
  if request.method == "POST":
    username = request.form['username']
    password = request.form['password']
    db = mongoclient["AllUsers"]
    mycol = db["userpass"]
    allusers = []
    for doc in mycol.find({}, {"_id": 0, "Username": 1}):
      xx = doc['Username']
      allusers.append(xx)
    if username not in allusers:
      return render_template(
          "addlink.html", text="That is not a real username!")
    for doc in mycol.find({}, {
        "_id": 0,
        "Username": 1,
        "Password": 1,
        "Votes": 1,
        "Description": 1,
        "Admin": 1,
        "MOD": 1,
        "discordusername": 1
    }):
      someusername = doc['Username']
      if username == someusername:
        passwordnew = doc['Password']
        if password == passwordnew:
          userandtag = checktag(username)
        else:
          return render_template(
              "addlink.html", text="Wrong password!")
    redirectlink = request.form['redirectlink']
    x = 0
    if "https://" in redirectlink:
      x = x + 1
    if "http://" in redirectlink:
      x = x + 1
    if x == 0:
      return render_template(
          "addlink.html",
          text=
          "Make sure to include https:// or http:// in your redirect link"
      )
    if "." not in redirectlink:
      return render_template(
          "addlink.html", text="Have you forgotten to add the .?")
    allcodes = []
    db = mongoclient.links
    mycol = db.SomeLinks
    for doc in mycol.find({}, {"_id": 0, "code": 1}):
      allcodes.append(doc['code'])
    link = request.form['link']
    if link in allcodes:
      return render_template(
          "addlink.html",
          text=
          "This Easy to Remember Link is already taken, enter another one"
      )
    if " " in link:
      return render_template(
          "addlink.html",
          text=
          "You cannot have space in the Easy to Remember link, use a - instead"
      )
    document = [{
        "LinkMaker": userandtag,
        "thelink": redirectlink,
        "code": link
    }]
    mycol.insert_many(document)
    reallink = "https://frank.vulcanwm.com/links/" + link
    return render_template(
        "main.html",
        text="The link has been made! Go to " + reallink +
        " to try out the Easy to Remember Link")


@app.route("/links/<link>")
def links(link):
  db = mongoclient.links
  mycol = db.SomeLinks
  for doc in mycol.find({}, {"_id": 0, "thelink": 1, "code": 1}):
    if doc['code'] == link:
      return redirect(doc['thelink'])
    else:
      pass
  return render_template("404.html")


@app.route('/favicon-ico')
def logo():
  return send_file('static/FRANKlogo.png')

@app.route("/style.css")
def stylecss():
  return send_file("static/style.css")

@app.route("/script.js")
def scriptjs():
  return send_file("static/script.js")