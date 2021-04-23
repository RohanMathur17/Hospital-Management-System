from tkinter import *
#ttk is a module (which contains combobox) inside ttk module
#modules inside a module do not get imported unless explicitly imported
#classes and functions are imported with *

from tkinter import ttk
import sqlite3

def add_student():
    r = e_roll.get()
    n = e_name.get()
    e = e_email.get()
    m = e_mobile.get()
    g = c_gender.get()
    d = e_dob.get()
    a = t_address.get("1.0",END)
    #here '1' is line number 'one' and '0' means first character of line number 'one'
    #it reads zeroth character of 1st line till end

    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute('INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?)' , (r, n, e, m, g, d, a))#'?' is known as place holder
    #c.execute("INSERT INTO student VALUES  ('"+r+"','"+n+"','"+e+"','"+m+"','"+g+"','"+d+"','"+a+"')")
    # Above technique is also correct
    conn.commit()
    conn.close()

    show_all()

    clear_all()

def show_all():
    e_search.delete(0, END)
    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM student')
    student_table.delete(*student_table.get_children())#it will delete/erase all rows of the table
    for r in c:
        student_table.insert("", "end", values=r)#end appends new row #value=r assigns entire row
    conn.commit()
    conn.close()

def clear_all():
    e_roll.delete(0, END)
    e_name.delete(0, END)
    e_email.delete(0, END)
    e_mobile.delete(0, END)
    e_dob.delete(0, END)
    t_address.delete(1.0, END)
    c_gender.current(0)

def get_data(event):
    current = student_table.item(student_table.focus())#focus(selected/highlighted) and item together fetch the info of the highlighted row and store it in current
    #item returns dictionary
    row = current["values"] #focussed row stored in current as a dictionary
    #current is a dictionary which returns current of values (stored in form of row(row is list))

    clear_all()

    e_roll.insert(0, row[0])
    e_name.insert(0, row[1])
    e_email.insert(0, row[2])
    e_mobile.insert(0, row[3])
    e_dob.insert(0, row[5])
    t_address.insert(1.0, row[6])#here '1' is line number 'one' and '0' means first character of line number 'one'
    c_gender.current(["female","male","other"].index(row[4]))#list same as combobox it will search the input index in the list and assign the value to c_gender.current
    
def update_student():
    e = e_email.get()
    m = e_mobile.get()
    a = t_address.get("1.0",END)
    r = e_roll.get()
    
    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute('UPDATE student SET email = ? , mobile = ? , address = ? WHERE roll = ?' , (e,m,a,r) )
    conn.commit()
    conn.close()
    show_all()
    clear_all()

def delete_student():
    r = e_roll.get()
    
    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute('DELETE FROM student WHERE roll = ?' , (r,) )#(r,) its a bug if we do this the code will always work otherwise it won't (we talkin about comma after r)
    conn.commit()
    conn.close()
    show_all()
    clear_all()

def search_student():
    s = c_search.get()
    key = e_search.get()

    conn = sqlite3.connect('student_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM student WHERE "+s+"= ?", (key,))
    student_table.delete(*student_table.get_children())
    for r in c:
            student_table.insert("", "end", values=r)
    conn.commit()
    conn.close()
    
    
master = Tk()
master.title('Student Management System')
master.geometry('1300x800')

title = Label(master, text="Student Management System", font=("Calibri",40,"bold"), bg="red", fg="white", bd=7, relief=GROOVE) #relief = type of border
title.pack(side=TOP, fill=X) #pack is known as geometry manager
                             #fill=X occupies entire x axis 

left_frame = Frame(master, bg="red", bd=4, relief=RIDGE)
left_frame.place(x=20, y=90, width=550, height=700)

left_frame_title = Label(left_frame, text="Manage Students", font=("Calibri",30,"bold"), bg="white", fg="red", bd=4, relief=GROOVE)
left_frame_title.pack(side=TOP, fill=X)

l_roll = Label(left_frame, text="Roll No.", font=("Calibri",25,"bold"), fg="white", bg="red") #why bg
l_roll.place(x=20, y=80)
e_roll = Entry(left_frame, font=("Calibri",18))
e_roll.place(x=150, y=80)

l_name = Label(left_frame, text="Name", font=("Calibri",25,"bold"), fg="white", bg="red")
l_name.place(x=20, y=140)
e_name = Entry(left_frame, font=("Calibri",18))
e_name.place(x=150, y=140)

l_email = Label(left_frame, text="Email", font=("Calibri",25,"bold"), fg="white", bg="red")
l_email.place(x=20, y=200)
e_email = Entry(left_frame, font=("Calibri",18))
e_email.place(x=150, y=200)

l_mobile = Label(left_frame, text="Mobile", font=("Calibri",25,"bold"), fg="white", bg="red")
l_mobile.place(x=20, y=260)
e_mobile = Entry(left_frame, font=("Calibri",18))
e_mobile.place(x=150, y=260)

l_gender = Label(left_frame, text="Gender", font=("Calibri",25,"bold"), fg="white", bg="red")
l_gender.place(x=20, y=320)
c_gender = ttk.Combobox(left_frame, font=("Calibri",18), width=7, state='readonly') #why readonly
c_gender["values"] = ("female","male","other")
c_gender.current(0)
c_gender.place(x=150, y=320)

l_dob1 = Label(left_frame, text="DOB", font=("Calibri",25,"bold"), fg="white", bg="red")
l_dob1.place(x=20, y=380)
l_dob2 = Label(left_frame, text="(dd/mm/yyyy)", font=("Calibri",20), fg="white", bg="red")
l_dob2.place(x=20, y=410)
e_dob = Entry(left_frame, font=("Calibri",18))
e_dob.place(x=150, y=380)

l_address = Label(left_frame, text="Address", font=("Calibri",25,"bold"), fg="white", bg="red")
l_address.place(x=20, y=460)
t_address = Text(left_frame, font=("Calibri",18), width=20, height=4)
t_address.place(x=150, y=460)

b_add = Button(left_frame, text='Add', width=8, height=2, command=add_student)
b_add.place(x=130, y=600)

b_update = Button(left_frame, text='Update', width=8, height=2, command=update_student)
b_update.place(x=230, y=600)

b_delete = Button(left_frame, text='Delete', width=8, height=2, command=delete_student)
b_delete.place(x=330, y=600)

right_frame = Frame(master, bg="red", bd=4, relief=RIDGE)
right_frame.place(x=590, y=90, width=690, height=700)

l_search = Label(right_frame, text="Search by", font=("Calibri",25,"bold"), fg="white", bg="red")
l_search.place(x=20, y=18)
c_search = ttk.Combobox(right_frame, width=10, font=("Calibri",15), state='readonly')
c_search["values"] = ("roll","name","mobile")
c_search.current(0)
c_search.place(x=150, y=18)
e_search = Entry(right_frame, font=("Calibri",18), width=10)
e_search.place(x=280, y=15)
b_search = Button(right_frame, text="Search", font=("Calibri",20), width=7, command=search_student)
b_search.place(x=420, y=16)
b_showall = Button(right_frame, text="Show All", font=("Calibri",20), width=7, command=show_all)
b_showall.place(x=520, y=16)

table_frame = Frame(right_frame, bg="red", bd=4, relief=RIDGE)
table_frame.place(x=20, y=70, width=650, height=600)

hs = Scrollbar(table_frame, orient=HORIZONTAL)
hs.pack(side=BOTTOM, fill=X)
vs = Scrollbar(table_frame, orient=VERTICAL)
vs.pack(side=RIGHT, fill=Y)
student_table = ttk.Treeview(table_frame, columns=("r", "n", "e", "m", "g", "d", "a"), xscrollcommand=hs.set, yscrollcommand=vs.set)
#xscrollcommand=hs.set, yscrollcommand=vs.set (sets relationship between scrollbars and table)
hs.config(command=student_table.xview)
vs.config(command=student_table.yview)
student_table.heading("r", text="Roll No.")
student_table.heading("n", text="Name")
student_table.heading("e", text="Email ID")
student_table.heading("m", text="Mobile")
student_table.heading("g", text="Gender")
student_table.heading("d", text="DOB")
student_table.heading("a", text="Address")
student_table.pack(fill=Y, expand=1)
#student_table.pack(fill=BOTH, expand=1)
student_table.column("r", width=60)
student_table.column("n", width=150)
student_table.column("e", width=150)
student_table.column("m", width=100)
student_table.column("g", width=75)
student_table.column("d", width=90)
student_table.column("a", width=300)
student_table["show"] = "headings"
#show only those columns which I have assigned headings and hence removes indexed column 
#student_table["show"] = "headings" shows only those columns in which headings are present, does not show the default index column.

student_table.bind("<ButtonRelease-1>", get_data)
#.bind handels any event that is taking place on student table here we have specified event type i.e <ButtonRelease-1> which will fetch/get data for us from the table


try:
    conn = sqlite3.connect('student_database.db')#conn means connection it creates a database or connects with existing database
    c = conn.cursor()#creates a cursor which is used to execute a query
    c.execute('CREATE TABLE student (roll CHAR(3), name VARCHAR(20), email VARCHAR(20), mobile CHAR(10), gender VARCHAR(6), dob CHAR(10), address VARCHAR(30))')
    #c.execute function is used to execute a query whatever is the query
    conn.commit()#after every query execution commit is called to reflect the changes in database if not called it means changes not execuyed in database
    conn.close()
except sqlite3.OperationalError:#exception handling introduced because the file has already been created previously so no need 
    pass

master.mainloop()


