import tkinter as tk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from threading import Thread
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
from tkmacosx import Button as MacButton

from Generate_Dataset import Generate_Data
from Model_train import Model_Training
from Recognizer import Recognition

window = tk.Tk()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)            

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

app = FullScreenApp(window)

class Example(tk.Frame):
    def __init__(self, master, *pargs):
        tk.Frame.__init__(self, master, *pargs)

        self.image = Image.open("landscape.png")
        self.img_copy = self.image.copy()

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

e = Example(window)
e.pack(fill=tk.BOTH, expand=tk.YES)

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April',
    '05': 'May', '06': 'June', '07': 'July', '08': 'August',
    '09': 'September', '10': 'October', '11': 'November', '12': 'December'
}

window.title("Smart Attendance System - Khosla")

# Configure TTK Style for modern Treeview & Progressbar
style = ttk.Style()
style.theme_use('clam')
style.configure('Treeview',
                background='#ffffff',
                foreground='#111827',
                rowheight=26,
                fieldbackground='#ffffff',
                font=('Helvetica', 12))
style.configure('Treeview.Heading',
                background='#8a2e7f',
                foreground='#ffffff',
                relief='flat',
                font=('Helvetica', 12, 'bold'))
style.map('Treeview.Heading', background=[('active', '#712367')])

# Top Header Banner
message3 = tk.Label(window, text="Smart Attendance System", fg="white", bg="#8a2e7f",
                    width=40, height=1, font=('Helvetica', 28, 'bold'))
message3.place(relx=0.5, rely=0.08, anchor=tk.CENTER)

# Date Banner
frame4 = tk.Frame(window, bg="#8a2e7f")
frame4.place(relx=0.5, rely=0.15, relwidth=0.22, relheight=0.045, anchor=tk.CENTER)

datef = tk.Label(frame4, text=day + "-" + mont[month] + "-" + year, fg="#ffffff", bg="#262523",
                 font=('Helvetica', 16, 'bold'))
datef.pack(fill='both', expand=1)

# Left Card: Already Registered
frame1 = tk.Frame(window, bg="#ffffff", highlightthickness=1, highlightbackground="#e5e7eb")
frame1.place(relx=0.06, rely=0.20, relwidth=0.38, relheight=0.75)

head1 = tk.Label(frame1, text="For Already Registered", fg="white", bg="#8a2e7f",
                 font=('Helvetica', 16, 'bold'), height=2)
head1.pack(fill=tk.X, side=tk.TOP)

# Right Card: New Enrollment
frame2 = tk.Frame(window, bg="#ffffff", highlightthickness=1, highlightbackground="#e5e7eb")
frame2.place(relx=0.56, rely=0.20, relwidth=0.38, relheight=0.75)

head2 = tk.Label(frame2, text="For New Enrollment", fg="white", bg="#8a2e7f",
                 font=('Helvetica', 16, 'bold'), height=2)
head2.pack(fill=tk.X, side=tk.TOP)

# ----------------- RIGHT CARD (Enrollment) -----------------
lbl = tk.Label(frame2, text="Enter Roll Number", width=22, height=1, fg="white", bg="#8a2e7f",
               font=('Helvetica', 12, 'bold'))
lbl.place(relx=0.25, rely=0.12)

txt = tk.Entry(frame2, width=22, fg="#111827", bg="#f9fafb", insertbackground="#111827",
               highlightbackground="#9ca3af", highlightcolor="#8a2e7f", highlightthickness=1,
               font=('Helvetica', 13))
txt.place(relx=0.25, rely=0.18)

lbl2 = tk.Label(frame2, text="Enter Student's Name", width=22, height=1, fg="white", bg="#8a2e7f",
                font=('Helvetica', 12, 'bold'))
lbl2.place(relx=0.25, rely=0.28)

txt2 = tk.Entry(frame2, width=22, fg="#111827", bg="#f9fafb", insertbackground="#111827",
                highlightbackground="#9ca3af", highlightcolor="#8a2e7f", highlightthickness=1,
                font=('Helvetica', 13))
txt2.place(relx=0.25, rely=0.34)

def get_data():
    Name = txt2.get().strip()
    Roll = txt.get().strip()
    if not Name or not Roll:
        mess.showwarning("Input Error", "Please enter both Roll Number and Name")
        return
    Generate_Data(Name, Roll)

takeImg = MacButton(frame2, text="Take Images", command=get_data,
                    fg="#ffffff", bg="#8a2e7f", activebackground="#712367", activeforeground="#ffffff",
                    width=230, height=38, borderless=1, font=('Helvetica', 13, 'bold'))
takeImg.place(relx=0.25, rely=0.44)

# Progress Bar & Training
def update_progress(val):
    progress['value'] = val

def progress_Measure():
    steps = [(2000, 20), (8000, 40), (14000, 50), (20000, 60), (25000, 100)]
    for delay, val in steps:
        window.after(delay, update_progress, val)

def bar(): 
    progress['value'] = 0
    Thread(target=Model_Training, daemon=True).start()
    progress_Measure()

trainImg = MacButton(frame2, text="Train The Model", fg="#ffffff", bg="#507d2a",
                     activebackground="#3b5d1f", activeforeground="#ffffff",
                     command=bar, width=300, height=42, borderless=1,
                     font=('Helvetica', 14, 'bold'))
trainImg.place(relx=0.18, rely=0.62)

progress = ttk.Progressbar(frame2, length=260, orient=tk.HORIZONTAL, mode='determinate')
progress.place(relx=0.22, rely=0.74)

# Watermark label in bottom right corner
watermark_lbl = tk.Label(frame2, text="Designed & Developed by Khosla", fg="#9ca3af", bg="#ffffff",
                         font=('Helvetica', 10, 'italic'))
watermark_lbl.place(relx=0.32, rely=0.92)

# ----------------- LEFT CARD (Attendance) -----------------
lbl3 = tk.Label(frame1, text="Select Class", width=20, fg="white", bg="#8a2e7f",
                height=1, font=('Helvetica', 12, 'bold'))
lbl3.place(relx=0.28, rely=0.10)

v = tk.IntVar()
v.set(1)
selection = 1

def ShowChoice():
    global selection
    selection = v.get()

first = tk.Radiobutton(frame1, text="Hindi", variable=v, command=ShowChoice, value=1,
                       bg="#ffffff", fg="#111827", activebackground="#ffffff", activeforeground="#8a2e7f",
                       selectcolor="#ffffff", font=('Helvetica', 13, 'bold'))
first.place(relx=0.28, rely=0.17)

second = tk.Radiobutton(frame1, text="English", variable=v, command=ShowChoice, value=2,
                        bg="#ffffff", fg="#111827", activebackground="#ffffff", activeforeground="#8a2e7f",
                        selectcolor="#ffffff", font=('Helvetica', 13, 'bold'))
second.place(relx=0.55, rely=0.17)

def Recognizer():
    Recognition(selection)

trackImg = MacButton(frame1, text="Take Attendance", fg="#ffffff", bg="#507d2a",
                     activebackground="#3b5d1f", activeforeground="#ffffff",
                     command=Recognizer, width=300, height=40, borderless=1,
                     font=('Helvetica', 14, 'bold'))
trackImg.place(relx=0.18, rely=0.25)

# Treeview & Scrollbar
tree_container = tk.Frame(frame1, bg="#ffffff")
tree_container.place(relx=0.06, rely=0.41, relwidth=0.88, relheight=0.38)

tv = ttk.Treeview(tree_container, columns=('roll_no', 'name', 'attendance'),
                  selectmode='browse', show=["headings"])
tv.column('roll_no', width=110, anchor=tk.CENTER)
tv.column('name', width=150, anchor=tk.CENTER)
tv.column('attendance', width=110, anchor=tk.CENTER)

tv.heading('roll_no', text='Roll Number')
tv.heading('name', text='Name')
tv.heading('attendance', text='Attendance')

scroll = ttk.Scrollbar(tree_container, orient='vertical', command=tv.yview)
tv.configure(yscrollcommand=scroll.set)

tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

def clear_tree():
    x = tv.get_children()
    for child in x:
        tv.delete(child)

def Show_attendance():
    clear_tree()
    if selection == 1:
        subject = "Hindi_attendance/Hindi_Attendance.csv"
    else:
        subject = "English_attendance/English_Attendance.csv"

    if not os.path.exists(subject):
        mess.showinfo("No Records", "No attendance records found for this class.")
        return

    with open(subject, newline="") as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            roll = row.get('Roll Number', '')
            Name = row.get('Name', '')
            attendance = row.get('Attendance', '0')
            tv.insert("", 0, values=(roll, Name, attendance))

Show_button = MacButton(frame1, text="Show Attendance", fg="#ffffff", bg="#15803d",
                        activebackground="#166534", activeforeground="#ffffff",
                        command=Show_attendance, width=140, height=34, borderless=1,
                        font=('Helvetica', 12, 'bold'))
Show_button.place(relx=0.12, rely=0.33)

Show_button1 = MacButton(frame1, text="Clear", fg="#ffffff", bg="#b91c1c",
                         activebackground="#991b1b", activeforeground="#ffffff",
                         command=clear_tree, width=110, height=34, borderless=1,
                         font=('Helvetica', 12, 'bold'))
Show_button1.place(relx=0.60, rely=0.33)

def destroy():
    window.destroy()

quitWindow = MacButton(frame1, text="Quit Application", fg="#ffffff", bg="#b91c1c",
                       activebackground="#991b1b", activeforeground="#ffffff",
                       command=destroy, width=300, height=38, borderless=1,
                       font=('Helvetica', 13, 'bold'))
quitWindow.place(relx=0.18, rely=0.84)

window.mainloop()
