"""
Description: The front-end component of Secutors membership managment applet.
Author: Aleksa Zatezalo
Date: July 2021

Developer Contact: zabumaphu@gmail.com
Notes: Please put 'SECUTOR SUPPORT' in email Subject line. 
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from tkcalendar import Calendar
import controller as controller

# Setting up the the canvas
root = tk.Tk(className="Secutor Membership Managment")
root.winfo_toplevel().title("Secutor Membership Management")
root.geometry("525x625")

# Setting Up Tabs
tabControl = ttk.Notebook(root)
sign_in = ttk.Frame(tabControl)
editUser = ttk.Frame(tabControl)
new_user = ttk.Frame(tabControl)
exist_user = ttk.Frame(tabControl)
contact = ttk.Frame(tabControl)

tabControl.add(sign_in, text='Sign In')
tabControl.add(editUser, text='Edit User')
tabControl.add(new_user, text='New Member')
tabControl.add(exist_user, text='Add Existing Member')
tabControl.add(contact, text='Developer Contact')
tabControl.pack(expand=1, fill="both")


# Dialogs
def noneFound():
    """
    Creates a dialog to announce that user is not found.

    Returns:
    Bool -> True representing success.
    """

    mb.showinfo('User not found.', "USER NOT FOUND")

    return True

def signInDialog():
    """
    Creates a dialog to announce successfull user login. Presents all user information.

    Returns:
    Bool -> True representing success. 
    """
    
    # Finds user and signs in
    pin = pin_box_sign_in.get()
    phone = phone_box_sign_in.get()
    email = name_box_sign_in.get()

    if (controller.find(pin, phone, email)):
        user, count = controller.find(pin, phone, email)

        # Checks date against current date
        # Shows success if membership is not expired
        # Otherwise shows warning
        print ("USER: ")
        print(user)
        controller.signIn(pin)
        if user[2] == 'False':
            mb.showinfo('User Signed In', 'Name: %(name)s\nPin: %(pin)s\nPhone: %(phone)s\nEmail: %(email)s\nBirthday: %(birthday)s\nSessions This Week: %(trainings)s\nMembership Expiry: %(date)s\n'%{"name": user[0], "pin": user[1], "phone":user[4], "date": user[3],"email": user[6], 'birthday':user[5], "trainings": user[7]})
        else:
            controller.toggleMembership(pin_box_sign_in.get())
            user, count = controller.find(pin_box_sign_in.get(), phone_box_sign_in.get(), name_box_sign_in.get())
            mb.showinfo('User Signed In', 'Name: %(name)s\nPin: %(pin)s\nPhone: %(phone)s\nEmail: %(email)s\nBirthday: %(birthday)s\nSessions-In This Week: %(trainings)s\nMembership Expiry: %(date)s\n'%{"name": user[0], "pin": user[1], "phone":user[4], "date": user[3],"email": user[6], 'birthday':user[5], "trainings": user[7],})
    else:
        noneFound()

    pin_box_sign_in.delete(0, END)
    pin_box_sign_in.insert(0, "")
    name_box_sign_in.delete(0, END)
    name_box_sign_in.insert(0, "")
    phone_box_sign_in.delete(0, END)
    phone_box_sign_in.insert(0, "")

    return True
    
def updateDialog(pin): 
    """
    Creates a dialog to announce successfull user update. Presents all user information.

    Returns:
    Bool -> True representing success. 
    """

    # New User Success Dialog created  
    user = controller.find(pin)[0]
    if user[2] == 'False':
        mb.showinfo('User Updated', 'Name: %(name)s\nPin: %(pin)s\nPhone: %(phone)s\nEmail: %(email)s\nBirthday: %(birthday)s\nMembership Expiry: %(date)s\n'%{"name": user[0], "pin": user[1], "phone":user[4], "date": user[3], "email": user[6], "birthday": user[5] })
    else:
        mb.showinfo('User Updated', 'Name: %(name)s\nPin: %(pin)s\nPhone: %(phone)s\nEmail: %(email)s\nBirthday: %(birthday)s\nMembership Expiry: Paused\n'%{"name": user[0], "pin": user[1], "phone":user[4], "email": user[6], "birthday": user[5]})

    # Fields cleared after success
    pin_box_edit.delete(0, END)
    pin_box_edit.insert(0, "Must Enter")
    phone_box_edit.delete(0, END)
    phone_box_edit.insert(0, "")
    name_box_edit.delete(0, END)
    name_box_edit.insert(0, "")
    email_box_edit.delete(0, END)
    email_box_edit.insert(0, "")
    
    return True

def existUserDialog():
    """
    Creates a dialog to enter existing user. Presents all user information.

    Returns:
    Bool -> True representing success. 
    """

    user = controller.existUser(ex_name_box.get(), ex_pin_box.get(), ex_cal.selection_get(), ex_phone_box.get(), ex_birthday_box.selection_get(), ex_email_box.get())
    mb.showinfo('User Re-Added', 'Name: %(name)s\nPin: %(pin)s\nPhone: %(phone)s\nEmail: %(email)s\nBirthday: %(birthday)s\nMembership Expiry: %(date)s\n'%{"name": user[0], "pin": user[1], "phone":user[4], "date": user[3],"email": user[6], 'birthday':user[5]})
   
   # Fields cleared after success
    ex_name_box.delete(0, END)
    ex_name_box.insert(0, "")
    ex_pin_box.delete(0, END)
    ex_pin_box.insert(0, "")
    ex_phone_box.delete(0, END)
    ex_phone_box.insert(0, "")
    ex_email_box.delete(0, END)
    ex_email_box.insert(0, "")

    return True

def newUserDialog():
    """
    Creates a dialog to announce new user. Presents all user information.

    Returns:
    Bool -> True representing success. 
    """

    user = controller.setUser(name_box.get(), cal.selection_get(), phone_box.get(), birthday_box.selection_get(), email_box.get())
    mb.showinfo('User Created', 'Name: %(name)s\nPin: %(pin)s\nPhone: %(phone)s\nEmail: %(email)s\nBirthday: %(birthday)s\nMembership Expiry: %(date)s\n'%{"name": user[0], "pin": user[1], "phone":user[4], "date": user[3],"email": user[6], 'birthday':user[5]})
   
   # Fields cleared after success
    name_box.delete(0, END)
    name_box.insert(0, "")
    phone_box.delete(0, END)
    phone_box.insert(0, "")
    email_box.delete(0, END)
    email_box.insert(0, "")

    return True

# Sign In Tab
tk.Label(sign_in, 
         text="PIN").grid(row=3, column=35)
tk.Label(sign_in, 
         text="Phone Number").grid(row=5, column=35)
tk.Label(sign_in, 
         text="Email").grid(row=7, column=35)

pin_box_sign_in = tk.Entry(sign_in)
phone_box_sign_in = tk.Entry(sign_in)
name_box_sign_in = tk.Entry(sign_in)
pin_box_sign_in.grid(row=4, column=35, padx=100, pady=1)
phone_box_sign_in.grid(row=6, column=35,padx=100, pady=1)
name_box_sign_in.grid(row=8, column=35, padx=100, pady=1)

# Adding photo to root
photo = PhotoImage(file = './graphics/logo.png')
root.iconphoto(False, photo)
root.title("Secutor Membership Managment")

# Find User Button
# A user in the system with a non expired membership is 'Loged in'
findUser =  Button(sign_in, text="Sign In", command= signInDialog)
findUser.grid(row=11, column=35,padx=100, pady=1)

# Edit User Tab
# Pin is unique and can not be changed
# Membership end date, Name, and Phone number is all up for channge
tk.Label(editUser, 
         text="PIN").grid(row=1, column=35)
tk.Label(editUser, text = "To Change", font = ('Helvetica', 14, 'bold')).grid(row=3, column=35, padx=100, pady=10)
tk.Label(editUser, 
         text="New Phone - if needed").grid(row=5, column=35) # Blank fields will not be changed
tk.Label(editUser, 
         text="New Name - if needed").grid(row=7, column=35) # Blank fields will not be changed
tk.Label(editUser, 
         text="New Email - if needed").grid(row=10, column=35) # Blank fields will not be changed
         
pin_box_edit = tk.Entry(editUser)
pin_box_edit.insert(0, 'must enter')
phone_box_edit = tk.Entry(editUser)
name_box_edit = tk.Entry(editUser)
email_box_edit = tk.Entry(editUser)
pin_box_edit.grid(row=2, column=35, padx=100, pady=1)
phone_box_edit.grid(row=6, column=35,padx=100, pady=1)
name_box_edit.grid(row=8, column=35, padx=100, pady=1)
email_box_edit.grid(row=11, column=35, padx=100, pady=1)

pin_box_sign_in = tk.Entry(sign_in)
phone_box_sign_in = tk.Entry(sign_in)
name_box_sign_in = tk.Entry(sign_in)
pin_box_sign_in.grid(row=4, column=35, padx=100, pady=1)
phone_box_sign_in.grid(row=6, column=35,padx=100, pady=1)
name_box_sign_in.grid(row=8, column=35, padx=100, pady=1)

def updateUser():
    """
    Updates a user upon update user button press.

    Returns:
    Bool -> True representing success. 
    """

    # No need for new name or phone number
    if (controller.newNameNum(pin_box_edit.get(), name_box_edit.get(), phone_box_edit.get(), email_box_edit.get())):
        updateDialog(pin_box_edit.get())
    else:
        noneFound()

    return True
   
def pauseMembership():
    """
    Pauses users membership upon button press.

    Returns:
    Bool -> True representing success. 
    """

    # Date change to time remaining
    # Unpause upon sign in
    if(controller.toggleMembership(pin_box_edit.get())):
        updateDialog(pin_box_edit.get())
    else:
        noneFound()
    return True

def extendMembership():
    """
    Extends membership by a month upon button press.

    Returns:
    Bool -> True representing success. 
    """

    pin = pin_box_edit.get()
    if (controller.extendMembership(pin)):
        updateDialog(pin_box_edit.get())
    else:
        noneFound()
    return True

updateButton =  Button(editUser, text="Update User", command=updateUser)
updateButton.grid(row=12, column=35,padx=100, pady=3)

# Pause or Extend membership
# This partition is not about personal information
tk.Label(editUser, text = "", font = ('Helvetica', 10, 'bold')).grid(row=15, column=35, padx=100, pady=10)

pauseButton =  Button(editUser, text="Toggle Membership", command=pauseMembership)
pauseButton.grid(row=17, column=35,padx=100, pady=3)

pauseButton =  Button(editUser, text="Extend Membership By Month", command=extendMembership)
pauseButton.grid(row=19, column=35,padx=100, pady=3)


# New User Tab
    # Set New User
tk.Label(new_user, 
         text="Name").grid(row=3, column=25)
tk.Label(new_user, 
         text="Phone Number").grid(row=5, column=25)
tk.Label(new_user, 
         text="Email").grid(row=7, column=25)
tk.Label(new_user, 
         text="Birthday").grid(row=9, column=25)
tk.Label(new_user, 
         text="Membership Expiriy Date").grid(row=11, column=25) # Users choose length of membership

name_box = tk.Entry(new_user)
phone_box = tk.Entry(new_user)
email_box = tk.Entry(new_user)
birthday_box = Calendar(new_user, selectmode = 'day')

name_box.grid(row=4, column=25, padx=100, pady=1)
phone_box.grid(row=6, column=25,padx=100, pady=1)
email_box.grid(row=8, column=25,padx=100, pady=1)
birthday_box.grid(row=10, column=25,padx=100, pady=1)
cal = Calendar(new_user, selectmode = 'day')
cal.grid(row=12, column=25,padx=100, pady=1)
 
# Button to. create user
newUser =  Button(new_user, text="Add New User", command=newUserDialog)
newUser.grid(row=13, column=25,padx=100, pady=3)


# Existing User Tab
    # Set New User
tk.Label(exist_user, 
         text="Name").grid(row=3, column=25)
tk.Label(exist_user, 
         text="Pin").grid(row=5, column=25)
tk.Label(exist_user, 
         text="Phone Number").grid(row=7, column=25)
tk.Label(exist_user, 
         text="Email").grid(row=9, column=25)
tk.Label(exist_user, 
         text="Birthday").grid(row=11, column=25)
tk.Label(exist_user, 
         text="Membership Expiriy Date").grid(row=13, column=25) # Users choose length of membership

ex_name_box = tk.Entry(exist_user)
ex_pin_box = tk.Entry(exist_user)
ex_phone_box = tk.Entry(exist_user)
ex_email_box = tk.Entry(exist_user)
ex_birthday_box = Calendar(exist_user, selectmode = 'day')

ex_name_box.grid(row=4, column=25, padx=100, pady=1)
ex_pin_box.grid(row=6, column=25, padx=100, pady=1)
ex_phone_box.grid(row=8, column=25,padx=100, pady=1)
ex_email_box.grid(row=10, column=25,padx=100, pady=1)
ex_birthday_box.grid(row=12, column=25,padx=100, pady=1)
ex_cal = Calendar(exist_user, selectmode = 'day')
ex_cal.grid(row=14, column=25,padx=100, pady=1)
 
# Button to create user
existUser =  Button(exist_user, text="Add Existing User", command=existUserDialog)
existUser.grid(row=16, column=25,padx=100, pady=3)

# Support Tab
ttk.Label(contact, text="For Developer Support \nEmail: zabumaphu@gmail.com\nSubject: SECUTOR MEMBERSHIP APP\nLanguages: Srpski or English").grid(column=0, row=0, padx=30, pady=30)
ttk.Label(contact, text="Software By Aleksa Zatezalo").grid(column=0, row=3, padx=30, pady=30)

root.mainloop()