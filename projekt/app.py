from tkinter import *
from  tkinter import ttk
from tkinter import font
import tkinter as tk
import serial
import time
import threading
from time import sleep
import numpy as np
import random
from itertools import count
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

port = "COM3"
data  = []
buffer = [20,1010,500,100.00]
table = [
    ["Proba", ""],
    ["Test", ""]
]

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
    
def animate(i):
    yar.append(int(float(buffer[2])))
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)

def animate_temp(i):
    yar_temp.append(int(float(buffer[0])))
    xar_temp.append(i)
    line_temp.set_data(xar_temp, yar_temp)
    ax1_temp.set_xlim(0, i+1)

def animate_pre(i):
    yar_pre.append(int(float(buffer[1])))
    xar_pre.append(i)
    line_pre.set_data(xar_pre, yar_pre)
    ax1_pre.set_xlim(0, i+1)

def animate_hum(i):
    yar_hum.append(int(float(buffer[3])))
    xar_hum.append(i)
    line_hum.set_data(xar_hum, yar_hum)
    ax1_hum.set_xlim(0, i+1)

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
    if(float(buffer[2]) > 500):
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
root.geometry('400x700+50+50')
root['bg'] = '#C1DBE3'
xar = []
yar = []
xar_temp = []
yar_temp = []
xar_pre = []
yar_pre = []
xar_hum = []
yar_hum = []
var = StringVar(root)
newwindow = tk.Toplevel(root)
newwindow.geometry("1500x500+500+300")

style.use('ggplot')
#plot_svjetlost
fig = plt.figure(figsize=(14, 4.5), dpi=50)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 1000)
line, = ax1.plot(xar, yar, 'r', marker='o')
#plot_temp
fig_temp = plt.figure(figsize=(14, 4.5), dpi=50)
ax1_temp = fig_temp.add_subplot(1, 1, 1)
ax1_temp.set_ylim(0, 50)
line_temp, = ax1_temp.plot(xar_temp, yar_temp, 'r', marker='o')
#plot_pre
fig_pre = plt.figure(figsize=(14, 4.5), dpi=50)
ax1_pre = fig_pre.add_subplot(1, 1, 1)
ax1_pre.set_ylim(900, 1200)
line_pre, = ax1_pre.plot(xar_pre, yar_pre, 'r', marker='o')
#plot_hum
fig_hum = plt.figure(figsize=(14, 4.5), dpi=50)
ax1_hum = fig_hum.add_subplot(1, 1, 1)
ax1_hum.set_ylim(0, 100)
line_hum, = ax1_hum.plot(xar_hum, yar_hum, 'r', marker='o')


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

#svjetlost
plotcanvas = FigureCanvasTkAgg(fig, newwindow)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False)

#temp
plotcanvas_temp = FigureCanvasTkAgg(fig_temp, newwindow)
plotcanvas_temp.get_tk_widget().grid(column=1, row=2)
ani_temp = animation.FuncAnimation(fig_temp, animate_temp, interval=1000, blit=False)

#pressure
plotcanvas_pre = FigureCanvasTkAgg(fig_pre, newwindow)
plotcanvas_pre.get_tk_widget().grid(column=2, row=1)
ani_pre = animation.FuncAnimation(fig_pre, animate_pre, interval=1000, blit=False)

#humidity
plotcanvas_hum = FigureCanvasTkAgg(fig_hum, newwindow)
plotcanvas_hum.get_tk_widget().grid(column=2, row=2)
ani_hum = animation.FuncAnimation(fig_hum, animate_hum, interval=1000, blit=False)


root.mainloop()


