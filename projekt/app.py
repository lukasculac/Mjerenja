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
buffer = [20,1010,500,100.00]

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
    #print(data)
    if(x == 4): 
        buffer[0] = data[0]
        buffer[1] = data[1] 
        buffer[2] = data[2]
        buffer[3] = data[3]
    

def values():
    conn()
    #print(buffer) 
    sec.delete(0, 'end')
    sec.insert(END, "Temperatura: ") 
    sec.insert(END, buffer[0]) 
    sec.insert(END, u" \N{DEGREE SIGN}C") 
    sec.insert(END, "\n")
    sec.insert(END, "Tlak: ") 
    sec.insert(END, buffer[1]) 
    sec.insert(END, " hPa") 
    sec.insert(END, "\n")
    sec.insert(END, "Svjetlost: ") 
    sec.insert(END, buffer[2]) 
    sec.insert(END, " lux") 
    sec.insert(END, "\n")
    sec.insert(END, "Vlažnost: ") 
    sec.insert(END, buffer[3]) 
    sec.insert(END, " %") 
    sec.insert(END, "\n")
    root.after(100, values)

root = Tk()
root.title('Pametni stan')
root.geometry('1200x700')
root['bg'] = '#C1DBE3'

var = StringVar(root)

l = Label(root, text = "Vrijednosti parametara")
l.config(font = ("Courier", 15))
l.pack(pady=10)

glavni = ttk.Label(
    root,
    text='',
    font=("Arial", 18),
    textvariable=var)
glavni.pack(ipadx=10, ipady=10, pady=10)

sec = Entry(root, textvariable = var)


values()

root.mainloop()

