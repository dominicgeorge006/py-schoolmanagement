import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import filedialog
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from tkinter import messagebox

def log_out():
    global root, dashboard_window
    
    # Destroy the current dashboard window if it exists
    if dashboard_window:
        dashboard_window.destroy()
    
    # Recreate the root window
    root = tk.Tk()
    root.geometry('925x500+300+200')

    # Import the tcl file
    root.tk.call('source', 'forest-dark.tcl')

    # Set the theme with the theme_use method
    ttk.Style().theme_use('forest-dark')
    
    img = PhotoImage(file='login.PNG')
    img_label = tk.Label(root, image=img)
    img_label.place(x=50, y=50)

    frame = ttk.Frame(root, width=350, height=350)
    frame.place(x=625, y=60)

    # Header
    header2 = ttk.Label(frame, text="Sign In", anchor=tk.CENTER, font=("Open Sans", 19, "bold"))
    header2.pack(pady=10)

    lab1 = ttk.Label(frame, text="Username:", anchor=tk.CENTER, font=("Segoe UI", 13, "bold"))
    global username
    username = ttk.Entry(frame)
    lab1.pack(pady=10)
    username.pack(pady=2)

    lab2 = ttk.Label(frame, text="Password:", anchor=tk.CENTER, font=("Segoe UI", 13, "bold"))
    global pwd
    pwd = ttk.Entry(frame, show="*")
    lab2.pack(pady=10)
    pwd.pack(pady=2)

    button = ttk.Button(frame, text='Login', style='Accent.TButton', command=handle_login)
    button.pack(pady=10)
    root.mainloop()
    

def openFile():
        global file_name
        file_name=[]
        '''file_name =filedialog.askopenfilename().replace("\\" , "\\\\")'''
        temp=filedialog.askopenfilenames()
        for i in temp:
            file_name.append(i.replace("\\" , "\\\\"))
def handle_login():
    global username_text
    username_text = username.get()
    password_text = pwd.get()
    credentials = {
        'parent': 'parent',
        'teacher': 'teacher',
        'admin': 'admin'
    }
    
    if username_text in credentials and password_text == credentials[username_text]:
        role =username_text
        open_dashboard(role)

       
    else:
        messagebox.showerror("Login Error", "Invalid username or password")
def email_student():
    smt_port=587
    smtp_server='smtp.gmail.com'
    email_from = 'veerhk2007@gmail.com'
    email_list =['cstrs5069@choiceschool.com']
    pswd='wfxr yqdy iopp elpz'
    email_window = tk.Tk()
    email_window.geometry('400x400')
    email_window.title("Send Email")
    subj=f'New Announcement from {username_text}'
    email_window.tk.call('source', 'forest-dark.tcl')
    ttk.Style().theme_use('forest-dark')
    inpembody = ttk.Label(email_window, text="Body:", anchor=tk.CENTER, font=("Segoe UI", 13, "bold"))
    body = ttk.Entry(email_window)
    inpembody.pack(pady=20)
    body.pack(pady=20)
    attach= ttk.Button(email_window, text='Add Attachments', style='Accent.TButton', command=openFile)
    attach.pack()
    def send_emails():
        subj = f'New Announcement from {username_text}'
        for person in email_list:
            # Fetch the body text from the entry widget
            body_text = body.get()
            styl="""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,200..1000;1,200..1000&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Mulish:ital,wght@0,200..1000;1,200..1000&family=Roboto+Condensed:ital,wght@0,100..900;1,100..900&display=swap');
    body{
    display: grid;
    place-items: center;
    background: #1a191f;
}
h1 {
    margin: 0;
    font-family: "Mulish", sans-serif;
    font-weight: 1000;
    font-size: 32px;
    color: #deb460;
}
h2{
    font-family: "Roboto Condensed", sans-serif;
  font-optical-sizing: auto;
  font-weight: 300;
  font-style: normal;
  color: #deb460;
}

    </style>
</head>
<body>
    <h1>New Announcement from your Teacher</h1>""" + f'''
    <h2>{body_text}</h2>
</body>
</html>
'''
            # Create the MIME object
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = person
            msg['Subject'] = subj
            msg.attach(MIMEText(styl, 'html'))

            # Attach file if selected
            if file_name:
                for i in file_name:
                    file_base_name = os.path.basename(i)
                    with open(i, 'rb') as attachment:
                        p = MIMEBase('application', 'octet-stream') 
    
                        # To change the payload into encoded form 
                        p.set_payload((attachment).read()) 
    
                        # encode into base64 
                        encoders.encode_base64(p) 
    
                    p.add_header('Content-Disposition', f"attachment; filename={file_base_name}") 
    
                        # attach the instance 'p' to instance 'msg' 
                    msg.attach(p) 
            try:
                # Send the email
                with smtplib.SMTP(smtp_server, smt_port) as email_server:
                    email_server.starttls()
                    email_server.login(email_from, pswd)
                    email_server.sendmail(email_from, person, msg.as_string())
                    messagebox.showinfo("showinfo", "Email Successfully Sent !")
                    email_window.destroy()
            except Exception as e:
                messagebox.showinfo("showinfo", e)                                                                               
        


    send_button = ttk.Button(email_window, text='Send Email', style='Accent.TButton', command=send_emails)
    send_button.pack(pady=20)
        

def open_dashboard(role):
    """
    Opens a new window with widgets and functionalities specific to the user role.
    """
    root.destroy()  # Close the login window
    global dashboard_window
    dashboard_window = tk.Tk()
    dashboard_window.geometry('400x400')
    dashboard_window.title(f"{role.capitalize()} Dashboard")
    # Import the tcl file
    dashboard_window.tk.call('source', 'forest-dark.tcl')

    # Set the theme with the theme_use method
    ttk.Style().theme_use('forest-dark')
    
    # Common header
    header = ttk.Label(dashboard_window, text=f"Welcome, {role.capitalize()}!", font=("Segoe UI", 20, "bold"))
    header.pack(pady=10)
    
    if role == 'parent':
        # Widgets specific to Parent role
        ttk.Label(dashboard_window, text="Parent Dashboard", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Button(dashboard_window, text="View Child's Progress", command=lambda: print("View Child's Progress")).pack(pady=10)
        ttk.Button(dashboard_window, text="Update Contact Information", command=lambda: print("Update Contact Info")).pack(pady=10)
        ttk.Button(dashboard_window, text="Logout", command=log_out ,style='Accent.TButton').pack(pady=10)
        
    elif role == 'teacher':
        ttk.Label(dashboard_window, text="Teacher Dashboard", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Button(dashboard_window, text="Email Students", command=email_student).pack(pady=10)
        ttk.Button(dashboard_window, text="Mark Attendance", command=lambda:print("Hello")).pack(pady=10)
        ttk.Button(dashboard_window, text="View Attendance Graph", command=lambda:print("Hello")).pack(pady=10)
        ttk.Button(dashboard_window, text="Logout", command=log_out ,style='Accent.TButton').pack(pady=10)
        
    elif role == 'admin':
        ttk.Label(dashboard_window, text="Admin Dashboard", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Button(dashboard_window, text="Manage Users", command=lambda: print("Manage Users")).pack(pady=10)
        ttk.Button(dashboard_window, text="View System Logs", command=lambda: print("View System Logs")).pack(pady=10)
        ttk.Button(dashboard_window, text="Logout", command=log_out ,style='Accent.TButton').pack(pady=10)



root = tk.Tk()
root.geometry('925x500+300+200')

# Import the tcl file
root.tk.call('source', 'forest-dark.tcl')

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-dark')
img = PhotoImage(file='login.PNG')
img_label = tk.Label(root, image=img,)
img_label.place(x=50,y=50)

frame=ttk.Frame(root,width=350,height=350)
frame.place(x=625,y=60)


# Header
header2 = ttk.Label(frame, text="Sign In", anchor=tk.CENTER, font=("Open Sans", 19, "bold"))
header2.pack(pady=10)

lab1 = ttk.Label(frame, text="Username:", anchor=tk.CENTER, font=("Segoe UI", 13, "bold"))
username = ttk.Entry(frame)
lab1.pack(pady=10)
username.pack(pady=2)

lab2 = ttk.Label(frame, text="Password:", anchor=tk.CENTER, font=("Segoe UI", 13, "bold"))
pwd = ttk.Entry(frame, show="*")
lab2.pack(pady=10)
pwd.pack(pady=2)

button = ttk.Button(frame, text='Login', style='Accent.TButton', command=handle_login)
button.pack(pady=10)

root.mainloop()
