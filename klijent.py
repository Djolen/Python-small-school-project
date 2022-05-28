import select
import tkinter
from tkinter import *
import time
import socket
import threading


def sendSrv():
    if gorivo.get() == 0:
        tipGoriva = vrsteGoriva[0]
    else:
        tipGoriva = vrsteGoriva[1]
    str1 = ""
    str1 += model.get() + ":" + proizvodjac.get() + ":" + kw.get() + ":" + tipGoriva

    s = socket.socket()
    s.connect(("localhost", 12345))
    s.sendall(str1.encode())
    srecv = s.recv(1024).decode()
    ta.insert("0.0", srecv + "\n")
    s.close()


tk = Tk()
f = ("Arial", 13)
tk.geometry("400x700")
model = StringVar()
proizvodjac = StringVar()
kw = StringVar()
vrsteGoriva = ("Dizel","Benzin")
gorivo = IntVar(value=0)

Label(tk, text="IME PROIZVODJACA", bg="blue", fg="white", width=100, font=f).pack()
entProiz = Entry(tk, font=f, width=50, textvariable=proizvodjac).pack()

Label(tk, text="IME MODELA", bg="blue", fg="white", width=100, font=f).pack()
entModel = Entry(tk, font=f, width=50, textvariable=model).pack()

Label(tk, text="SNAGA MOTORA (Kw)", bg="blue", fg="white", width=100, font=f).pack()
entModel = Entry(tk, font=f, width=50, textvariable=kw).pack()

for i in range (len(vrsteGoriva)):
    R = Radiobutton(tk,text=vrsteGoriva[i],  value=i, variable=gorivo, font=f)
    R.pack( anchor = W )

button = Button(tk, text="Send", width=100, command=sendSrv).pack()

ta = Text(tk, width=40, font=f)
ta.pack()

tk.mainloop()
