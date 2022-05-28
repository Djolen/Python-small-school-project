import json
import tkinter
from tkinter import *
import time
import socket
import threading
import functools
import pymysql

class auto:

    def __init__(self, proizvodjac,model,tipGoriva,hp=0):
        self.proizvodjac = proizvodjac
        self.model = model
        self.hp = hp
        self.tipGoriva = tipGoriva

    def to_json(self):
        return json.dumps(self.__dict__)

    def getHp(self):
        return self.hp

    def __str__(self):
        return "Auto: %s , proizvodjac: %s, snaga motora(hp): %s" % (self.model,self.proizvodjac,self.hp)


#konekcija na bazu
db = pymysql.connect (host="localhost",port=3306,user="root", passwd= "",db="test")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS AUTOMOBILI")
sql = """CREATE TABLE AUTOMOBILI (
         MODEL CHAR(20) NOT NULL,
         PROIZVODJAC CHAR(20),
         SNAGA FLOAT,
         GORIVO CHAR(6)) """
cursor.execute(sql)




def mapiranje(auto):
    return auto.model

automobili = []
snage = []

kw2hp = lambda x: x * 1.34

def bezbedniAutomobili(x):
  if x.getHp() < 109:
    return True
  else:
    return False


def srvThread():
    s=socket.socket()
    s.bind(("localhost", 12345))
    s.listen()
    while True:
        conn, add=s.accept()
        str=conn.recv(1024).decode()
        poruke = str.split(":")
        snagaKw = float(poruke[2])

        ta.insert("0.0", str+'\n')
        ta.insert("0.0", "SERVER: waiting...\n")
        #print(poruke)
        snaga = kw2hp(snagaKw)
        snage.append(snaga)

        automobil = auto(poruke[1],poruke[0],poruke[3],snaga)
        automobili.append(automobil)

        dictAuto = auto(poruke[1],poruke[0],poruke[3],snaga).to_json()
        automobiliFajl = open("automobili.txt", "a")
        json.dump(dictAuto, automobiliFajl)
        automobiliFajl.write("\n")
        automobiliFajl.close()

        automobiliZaPocetnike = filter(bezbedniAutomobili,automobili)
        print("Od unetih automobila pocetnici smeju da voze: ")
        for x in automobiliZaPocetnike:
            print(x)

        print("A od svih unetih automobila najveca snaga : ", end="")
        print(functools.reduce(lambda a, b: a if a > b else b, snage))

        print("Svi modeli koji su uneti")
        sviModeli = list(map(mapiranje, automobili))
        print(list(sviModeli))

        sql = "INSERT INTO AUTOMOBILI(MODEL, \
               PROIZVODJAC, SNAGA, GORIVO) \
               VALUES ('%s', '%s', '%d', '%s')" % \
                (poruke[1], poruke[0], snaga, poruke[3])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

        sret="Vreme primanja poruke je "
        sret+=time.ctime()
        sret+="\n"
        ta.insert("0.0", sret)

        conn.sendall(sret.encode())
        conn.close()


tk = Tk()

tk.geometry("500x500")

ta=Text(tk, width=100, height=30, font=("Arial", 13))
ta.pack()
ta.insert("0.0", "SERVER: waiting...\n")
t1=threading.Thread(target=srvThread)
t1.start()

mainloop()
db.close()
