from tkinter import *
from  tkinter import ttk
import tkinter
from tkinter import font
import serial
import time
import threading
from time import sleep

port = "COM3"
i = 0
data  = []
buffer = [20.18,1010.93,38.45,100.00]


def conn():
    global data
    global buffer
    ser = serial.Serial(port=port, baudrate=115200, timeout=.1)
    time.sleep(1)
    b = ser.readline()        # read a byte string
    string_n = b.decode()  # decode byte string into Unicode  
    string = string_n.rstrip() # remove \n and \r
    data = string.split("x")          
    ser.close()
    x = len(data)
    if(x == 4): 
        buffer[0] = data[0]
        buffer[1] = data[1] 
        buffer[2] = data[2]
        buffer[3] = data[3]
    

def values():
    conn()
    print(buffer) 
    my_text.insert(END, "Temperatura: ") 
    my_text.insert(END, buffer[0]) 
    my_text.insert(tkinter.END, u" \N{DEGREE SIGN}C") 
    my_text.insert(tkinter.END, "\n")
    my_text.insert(tkinter.END, "Pritisak: ") 
    my_text.insert(tkinter.END, buffer[1]) 
    my_text.insert(tkinter.END, " hPa") 
    my_text.insert(tkinter.END, "\n")
    my_text.insert(tkinter.END, "Svjetlost: ") 
    my_text.insert(tkinter.END, buffer[2]) 
    my_text.insert(tkinter.END, " lux") 
    my_text.insert(tkinter.END, "\n")
    my_text.insert(tkinter.END, "Vlažnost: ") 
    my_text.insert(tkinter.END, buffer[3]) 
    my_text.insert(tkinter.END, " %") 
    my_text.insert(tkinter.END, "\n")
    root.after(2000, Values)


root = Tk()
root.title('Pametni stan')
root.geometry('1200x700')
root['bg'] = '#AC99F2'

var = StringVar(root)
var.set('hello')

l = Label(root, text = "Vrijednosti parametara")
l.config(font = ("Courier", 14))
l.pack()

glavni = ttk.Label(
    root,
    text='Ovo je tekst',
    font=("Arial", 18),
    textvariable=var)
glavni.pack(ipadx=10, ipady=10, pady=10)

sec = Entry(root, textvariable = var)
sec.pack()
#my_text = Text(root, width = 40, height= 6, font=("Arial", 19))
#my_text.pack(padx = 20)

Entry.insert(0, buffer[1])
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 14)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 15,'bold'))

my_tab = ttk.Treeview(root, style="mystyle.Treeview")

my_tab['columns'] = ('object', 'value')

my_tab.column("#0",width=0, stretch=NO)
my_tab.column("object",anchor=CENTER)
my_tab.column("value",anchor=CENTER)

my_tab.heading("object",text="OBJEKT",anchor=CENTER)
my_tab.heading("value",text="STANJE",anchor=CENTER)

my_tab.insert(parent='',index='end',iid=0,text='',
values=('Rolete','Otvoreno'))
my_tab.insert(parent='',index='end',iid=1,text='',
values=('Svijetlo','Jako'))

my_tab.pack(pady= 20)

root.mainloop()

