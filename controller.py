"""
Description: The controller component of Secutors membership managment applet. Will operate on model. 
Author: Aleksa Zatezalo
Date: July 2021

Developer Contact: zabumaphu@gmail.com
Notes: Please put 'SECUTOR SUPPORT' in email Subject line. 
"""

import csv
from datetime import datetime
from datetime import date
import operator

def sortDb():
    """
    Sorts CSV file entry by pin entry.
    """

    reader = csv.reader(open("./memberInfo/membershipInfo.csv"), delimiter=",")
    sortedlist = sorted(reader, key=operator.itemgetter(1), reverse=False)
    print(sortedlist)
    with open("./memberInfo/membershipInfo.csv", 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(sortedlist)
    
# Database Management Calls
def generateNewPin():
    """
    Returns unique pin for a new user that is just being registered.
    Pins do not repreat themselvfs and cannot change. These purley serve as
    pointers for users in the database.

    Return
    Pin ->Int, a unique user identifer
    """

    # Parses through user DB
    # DB of users sorted by pin
    # Adds unique pin by adding 1 to highest pin 
    new_pin = 0
    with open('./memberInfo/membershipInfo.csv', 'r') as csv_file:
        # Iterate over each row in the csv using reader object 
        for row in csv_file:
                text = row.split(",")
                new_pin =  text[1]
    if (str(new_pin)[0:2] == "n-"):
        new_pin = "n-" + str(int(new_pin[2:]) + 1)
    else: 
        new_pin = int(new_pin) + 1
        new_pin = "n-" + str(new_pin)
    return new_pin
        
# Functions About User Instance
def setUser(name, membership, phone, birthday, email):
    """
    Takes name, membership expirey date, phone, birthday, and email. Puts it into array and saves to
    membershipInfo csv which acts as a DB. For new users.

    Arguments
    name ->  A String reprenting the users name.
    membership -> A String representing date of membership expiery. Formatted as YYYY-MM-DD.
    phone -> An Int representing users phone.
    membership -> A String representing date of membership expiery. Formatted as YYYY-MM-DD.
    birthday -> A String representing the users birthday. Formatted as YYYY-MM-DD.
    email -> A String representing the users email.

    Return
    user -> An array containing all arguments.

    """

    # Creates new user for CSV
    pin = generateNewPin()
    pause = False
    user = [name, pin, pause, membership, phone, birthday, email, 0]

    # Wrightes user to user db
    with open('./memberInfo/membershipInfo.csv', 'a') as f_object:
        writer_object = csv.writer(f_object, delimiter=',')
        writer_object.writerow(user)
        f_object.close()
    return user

def existUser(name, pin, membership, phone, birthday, email):
    """
    Takes name, membership expirey date, phone, birthday, and email. Puts it into array and saves to
    membershipInfo csv which acts as a DB. For users migrating to new DB.

    Arguments
    name ->  A String reprenting the users name.
    membership -> A String representing date of membership expiery. Formatted as YYYY-MM-DD.
    phone -> An Int representing users phone.
    membership -> A String representing date of membership expiery. Formatted as YYYY-MM-DD.
    birthday -> A String representing the users birthday. Formatted as YYYY-MM-DD.
    email -> A String representing the users email.

    Return
    user -> An array containing all arguments.

    """

    user = [name, pin, 'False', membership, phone, birthday, email, 0]
    # Wrightes user to user db
    with open('./memberInfo/membershipInfo.csv', 'a') as f_object:
        writer_object = csv.writer(f_object, delimiter=',')
        writer_object.writerow(user)
        f_object.close()
    
    # Sorts DB for Furute Pin
    sortDb()
    return user

# Functions regarding CSV database
def find(pin="", phone="", email=""):
    """
    Parses through membershipInfo.csv to find a user with matching pin, phone, or email.

    Arguments:
    pin -> Int, representing user pin.
    phone -> Int, representing user phone.
    email -> A String representing user email.

    Returns:
    text -> An Array of Strings representing the user.
    count -> Int, the CSV line where the user was found. 
    """

    count = 0
    print("Pin: " + pin)
    print("Phone: " + phone)
    print("Email: " + email)

    with open('./memberInfo/membershipInfo.csv', 'r') as csv_file:
        # Iterate over each row in the csv using reader object 
        for row in csv_file:
                text = row.split(",")
                print("Row - Pin: " + text[1] + " Phone: " + text[4] + " Email: " + text[6])
                if text[1] == pin:
                    return text, count  
                elif text[4] == phone:
                    return text, count
                elif text[6] == email:
                    return text, count
                count += 1
        return False, False

def signIn(pin):
    """
    Takes the users pin and finds the CSV row where the user is stored in the DB. Increments
    column 7, which represents the number of logins, by one. 

    Arguments:
    pin -> Int, represents the users pin.

    Return:
    Bool -> True representing signed in User.
    """

    user, count = find(pin)
    if user == False:
        return False

    user[7] = str(int(user[7]) + 1)
    print(user)

    wrightToDB(user, count)
    return True

def toggleMembership(user_pin=""):
    """
    Takes the users pin and finds the CSV row where the user is stored in the DB. 
    This toggles the boolean in column 2 representing wheather or not the membership
    is paused. Converts the date on column 3 to date when membership expires for False
    bool and to days remaining for True bool. False represents a not paused membership,
    while true represents a paused membership.

    Arguments:
    pin -> Int, represents the users pin.

    Return:
    Bool -> Returns True for toggled membership.
    """

    user, count = find(user_pin) 
    if user == "False":
        return False
    
    date_now = datetime.now()
    date_now = int(date_now.strftime("%Y%m%d"))
    user_expirey = int(user[3].replace('-', ''))

    if user[2] == 'False':
        user_expirey = user_expirey - date_now
        user[2] = 'True'
        user[3] = user_expirey
    else: 
        user[2] = 'False'
        user_expirey = user_expirey + date_now
        user[3] = str(user_expirey)
        user[3] = datetime(year=int(user[3][0:4]), month=int(user[3][4:6]), day=int(user[3][6:8])).strftime("%Y-%m-%d")

    wrightToDB(user, count)

    return True

def newNameNum(pin, name="", phone="", email=""):
    """
    Takes pin, name, phone, and email. If name, phone, or email are
    not passed as null, the correspdoning rows for user with pin PIN will
    be changed with the corresponding argument.

    Return:
    Bool -> Returns True for updated User.
    """
    # Ammend User
    user, count = find(pin)
    if user == "False":
        return False

    if name != "":
        user[0] = name
    if phone != "":
        user[4] = phone
    if email != "":
        user[6] = email
    
    wrightToDB(user, count)
    
    return True

def extendMembership(pin):
    """
    Finds user identified by the argument pin, and extends there membership by a month.

    Argument:
    Pin -> Int, representing users unique pin.

    Return:
    Bool -> True representing an updated user.
    """

    user, count = find(pin)
    if user == "False":
        return False

    user[3] = user[3].replace('-', '')

    # Toggle Membership if paused
    if user[2] == 'True':
        toggleMembership(pin)

    # Extend membership
    user_expirey = int(user[3])
    if int(user[3][4:6]) == 12:
        user_expirey = str(user_expirey)
        user_expirey = str(int(user_expirey[:4]) + 1) + '01' + user_expirey[6:]
    else: 
        user_expirey += 100

    user[3] = str(user_expirey)
    print(user[3])
    user[3] = datetime(year=int(user[3][0:4]), month=int(user[3][4:6]), day=int(user[3][6:8])).strftime("%Y-%m-%d")
    
    wrightToDB(user, count)

    return True

def wrightToDB(user, count):
    """
    Takes an array, user, representing a user to be overwritten in the membershipInfo CSV,
    and an int, count, representing the line to be overwrittern. Returns True upon success.

    Arguments:
    user -> Array, representing user.
    count -> Int, representing line to be overwritten. 
    """

    # Fixes bug with trailing whitespace in last column
    length = len(user) - 1
    user[length] = user[length].strip()

    # Rewright User
    userList = []

    # Read all data from the csv file.
    with open('./memberInfo/membershipInfo.csv', 'r') as b:
        users = csv.reader(b)
        userList.extend(users)

    # data to override in the format {line_num_to_override:data_to_write}. 
    line_to_override = {count:user}

    # Write data to the csv file and replace the lines in the line_to_override dict.
    with open('./memberInfo/membershipInfo.csv', 'w') as b:
        writer = csv.writer(b, delimiter=',')
        for line, row in enumerate(userList):
            data = line_to_override.get(line, row)
            writer.writerow(data)

    return True

def scheduleRest():
    """
    Parses through CSV and resets weekly logins.
    """

    if date.today().weekday() == 5: # Five is Saturday
        with open('./memberInfo/membershipInfo.csv', 'r') as b:
            users = list(csv.reader(b))
            for i in range(len(users)):
               users[i][7] = 0
            
        # Write data to the csv file and replace the lines in the line_to_override dict.
        with open("./memberInfo/membershipInfo.csv", 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(users)

    return True