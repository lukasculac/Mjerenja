from this import d
from tkinter import *
from  tkinter import ttk
import tkinter
from tkinter import font
import serial
import time
import threading
from time import sleep

port = "COM3"
data  = []
buffer = [20,1010,500,100.00]
table = [
    ["Proba", ""],
    ["Test", ""]
]
global count
count=0

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
    

def heating():
    if(float(buffer[0]) < 20):
        return "uključeno"
    else:
        return "isključeno"
def cooling():
    if(float(buffer[0]) > 29):
        return "uključeno"
    else:
        return "isključeno"
def lights():
    if(float(buffer[2]) > 800):
        return "upaljeno"
    else:
        return "ugašeno"
def pressure():
    if(float(buffer[1]) < 1010):
        return "loše"
    elif(float(buffer[1]) > 1019):
        return "dobro"
    elif(float(buffer[1]) > 1010 and float(buffer[1]) < 1019):
        return "neodređeno"
def humid():
    if(float(buffer[3]) < 40):
        return "uključeno"
    else:
        return "isključeno"
def dehumid():
    if(float(buffer[3]) > 60):
        return "uključeno"
    else:
        return "isključeno"
def tablica():
    
    grijanje = Label(tbl_frame,text=heating(), font=("Tahoma", 16), relief=SUNKEN)
    grijanje.grid(row=0, column=1)
    hladjenje = Label(tbl_frame, text=cooling(), font=("Tahoma", 16), relief=SUNKEN )
    hladjenje.grid(row=1, column=1)
    osvjetljenje = Label(tbl_frame, text=lights(), font=("Tahoma", 16), relief=SUNKEN )
    osvjetljenje.grid(row=2, column=1)
    ovlazivanje = Label(tbl_frame, text=humid(), font=("Tahoma", 16), relief=SUNKEN )
    ovlazivanje.grid(row=3, column=1)
    odvlazivanje = Label(tbl_frame, text=dehumid(), font=("Tahoma", 16), relief=SUNKEN )
    odvlazivanje.grid(row=4, column=1)
    vrijeme = Label(tbl_frame, text=pressure(), font=("Tahoma", 16), relief=SUNKEN )
    vrijeme.grid(row=5, column=1) 
    
    root.after(100, tablica)

root = Tk()
root.title('Pametni stan')
root.geometry('1200x700')
root['bg'] = '#C1DBE3'

var = StringVar(root)

#Naslov
l = Label(root, text = "Vrijednosti parametara")
l.config(font = ("Courier", 15))
l.pack(pady=10)

#Izmjereni podaci
glavni = ttk.Label(
    root,
    text='',
    font=("Arial", 18),
    textvariable=var)
glavni.pack(ipadx=10, ipady=10, pady=10)
sec = Entry(root, textvariable = var)


#tablica
tbl_frame = Frame(root)
tbl_frame.pack()

grijanje = Label(tbl_frame,text="GRIJANJE", font=("Tahoma", 17))
grijanje.grid(row=0, column=0)
hladjenje = Label(tbl_frame, text="HLAĐENJE", font=("Tahoma", 17))
hladjenje.grid(row=1, column=0)
osvjetljenje = Label(tbl_frame, text="RASVJETA", font=("Tahoma", 17))
osvjetljenje.grid(row=2, column=0)
ovlazivanje = Label(tbl_frame, text="OVLAŽIVANJE", font=("Tahoma", 17))
ovlazivanje.grid(row=3, column=0)
odvlazivanje = Label(tbl_frame, text="ODVLAŽIVANJE", font=("Tahoma", 17))
odvlazivanje.grid(row=4, column=0)
vrijeme = Label(tbl_frame, text="VRIJEME", font=("Tahoma", 17))
vrijeme.grid(row=5, column=0)

tablica()
values()

root.mainloop()

