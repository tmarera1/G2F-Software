#Import the library
from tkinter import *
import time
import queue
import sys
import os
from functools import partial

Var1 = 0
Var2 = 0
Var3 = 0

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


class CapSense:

    def __init__(self, q):
        # initialize the plot
        global Var1
        global Var2
        global Var3

        self.root= Tk()
        self.root.title("Capacitive Touch Sensing GUI")
        self.root.geometry("2000x800")
        self.my_canvas= Canvas(self.root, width=1800, height=700, bg="white")
        self.my_canvas.pack(pady=20)

        self.my_canvas.create_rectangle(20,20,600,680,outline="black",fill="white")
        self.my_canvas.create_text(230,50,fill = "dark blue",font=("Arial", 26),text="Capacitive Touch Sensing")
        self.my_canvas.create_rectangle(640,20,1220,680,outline="black",fill="white")
        self.my_canvas.create_text(765,50,fill = "dark blue",font=("Arial", 26),text="Force Sensing")
        self.my_canvas.create_text(1150,200,fill = "purple",font=("Helvetica", 16),text="Qorvo 1")
        self.my_canvas.create_text(730,350,fill = "purple",font=("Helvetica", 16),text="Qorvo 2")
        self.my_canvas.create_text(1150,480,fill = "purple",font=("Helvetica", 16),text="Qorvo 3")


        self.img= PhotoImage(file= "C:/Users/tmarera/Downloads/nus_central/Graphic.png")
        self.my_image= self.my_canvas.create_image(350,350, anchor=CENTER, image=self.img)

        self.sensor_1=self.my_canvas.create_arc(800,180,1120,500, start = 0,extent = 120, outline = "black", fill = "white")
        self.sensor_2=self.my_canvas.create_arc(800,180,1120,500, start = 120,extent = 120, outline = "black", fill = "white")
        self.sensor_3=self.my_canvas.create_arc(800,180,1120,500, start = 240,extent = 120, outline = "black", fill = "white")
        self.label_1=Label(self.root, bg="white", text=str(Var1),font=("Helvetica",14))
        self.label_1.place(x=1150,y=235)
        self.label_2=Label(self.root, bg="white", text=str(Var2),font=("Helvetica",14))
        self.label_2.place(x=730,y=385)
        self.label_3=Label(self.root, bg="white", text=str(Var3),font=("Helvetica",14))
        self.label_3.place(x=1150,y=515)


        #Create Pins 1-6: Cap Sense IC 1
        self.pin1=self.my_canvas.create_oval(428,222,411,239,fill="white")
        self.pin2=self.my_canvas.create_oval(400,241,383,258,fill="white")
        self.pin3=self.my_canvas.create_oval(422,279,405,296,fill="white")
        self.pin4=self.my_canvas.create_oval(459,300,442,317,fill="white")
        self.pin5=self.my_canvas.create_oval(478,359.5,497,340.5,fill="white")
        self.pin6=self.my_canvas.create_oval(459,383,442,400,fill="white")

        #Create Pins 7-12: Cap Sense IC 2
        self.pin7=self.my_canvas.create_oval(422,404,405,421,fill="white")
        self.pin8=self.my_canvas.create_oval(400,442,383,459,fill="white")
        self.pin9=self.my_canvas.create_oval(428,478,411,461,fill="white")
        self.pin10=self.my_canvas.create_oval(272,478,289,461,fill="white")
        self.pin11=self.my_canvas.create_oval(300,442,317,459,fill="white")
        self.pin12=self.my_canvas.create_oval(278,404,295,421,fill="white")

        #Create Pins 13-18: Cap Sense IC 3
        self.pin13=self.my_canvas.create_oval(258,383,241,400,fill="white")
        self.pin14=self.my_canvas.create_oval(222,359.5,203,340.5,fill="white")
        self.pin15=self.my_canvas.create_oval(258,300,241,317,fill="white")
        self.pin16=self.my_canvas.create_oval(278,279,295,296,fill="white")
        self.pin17=self.my_canvas.create_oval(300,241,317,258,fill="white")
        self.pin18=self.my_canvas.create_oval(272,222,289,239,fill="white")

        self.btn = Button(self.root, height = 2, width = 20, bg='light blue',  fg = 'black', text="START", command=partial(self.update, q))  # Set a "Start button". The "start_indicators" function is a call-back.
        self.btn.place(x=300, y=600)
        self.btn2=Button(self.root, height = 2, width = 20, bg='light blue',  fg = 'black', text="STOP", command=restart_program)
        self.btn2.place(x=900, y=600)


        #self.root.mainloop()

    def update(self, q):

        if(q.empty != 1):

            item = q.get()
            #print("item is {}".format(item))
            if (item[3] & (1<<0)):
              self.my_canvas.itemconfig(self.pin1, fill="yellow")
            if (item[3] & (1<<1)):
              self.my_canvas.itemconfig(self.pin2, fill="yellow")
            if (item[3] & (1<<2)):
              self.my_canvas.itemconfig(self.pin3, fill="yellow")
            if (item[3] & (1<<3)):
              self.my_canvas.itemconfig(self.pin4, fill="yellow")
            if (item[3] & (1<<4)):
              self.my_canvas.itemconfig(self.pin5, fill="yellow")
            if (item[3] & (1<<5)):
              self.my_canvas.itemconfig(self.pin6, fill="yellow")
            if (item[4] & (1<<0)):
              self.my_canvas.itemconfig(self.pin7, fill="yellow")
            if (item[4] & (1<<1)):
              self.my_canvas.itemconfig(self.pin8, fill="yellow")
            if (item[4] & (1<<2)):
              self.my_canvas.itemconfig(self.pin9, fill="yellow")
            if (item[4] & (1<<3)):
              self.my_canvas.itemconfig(self.pin10, fill="yellow")
            if (item[4] & (1<<4)):
              self.my_canvas.itemconfig(self.pin11, fill="yellow")
            if (item[4] & (1<<5)):
              self.my_canvas.itemconfig(self.pin12, fill="yellow")
            if (item[5] & (1<<0)):
              self.my_canvas.itemconfig(self.pin13, fill="yellow")
            if (item[5] & (1<<1)):
              self.my_canvas.itemconfig(self.pin14, fill="yellow")
            if (item[5] & (1<<2)):
              self.my_canvas.itemconfig(self.pin15, fill="yellow")
            if (item[5] & (1<<3)):
              self.my_canvas.itemconfig(self.pin16, fill="yellow")
            if (item[5] & (1<<4)):
              self.my_canvas.itemconfig(self.pin17, fill="yellow")
            if (item[5] & (1<<5)):
              self.my_canvas.itemconfig(self.pin18, fill="yellow")
            if item[0]<4:
              self.my_canvas.itemconfig(self.sensor_1, fill="light yellow")
            else:
              self.my_canvas.itemconfig(self.sensor_1, fill="yellow")
            if item[1]<4:
              self.my_canvas.itemconfig(self.sensor_2, fill="light yellow")
            else:
              self.my_canvas.itemconfig(self.sensor_2, fill="yellow")
            if item[2]<4:
              self.my_canvas.itemconfig(self.sensor_3, fill="light yellow")
            else:
              self.my_canvas.itemconfig(self.sensor_3, fill="yellow")

             
            self.root.update()  # Update the complete GUI.
            time.sleep(0.02) # Sleep two secs
            self.my_canvas.itemconfig(self.pin1, fill="white")
            self.my_canvas.itemconfig(self.pin2, fill="white")
            self.my_canvas.itemconfig(self.pin3, fill="white")
            self.my_canvas.itemconfig(self.pin4, fill="white")
            self.my_canvas.itemconfig(self.pin5, fill="white")
            self.my_canvas.itemconfig(self.pin6, fill="white")
            self.my_canvas.itemconfig(self.pin7, fill="white")
            self.my_canvas.itemconfig(self.pin8, fill="white")
            self.my_canvas.itemconfig(self.pin9, fill="white")
            self.my_canvas.itemconfig(self.pin10, fill="white")
            self.my_canvas.itemconfig(self.pin11, fill="white")
            self.my_canvas.itemconfig(self.pin12, fill="white")
            self.my_canvas.itemconfig(self.pin13, fill="white")
            self.my_canvas.itemconfig(self.pin14, fill="white")
            self.my_canvas.itemconfig(self.pin15, fill="white")
            self.my_canvas.itemconfig(self.pin16, fill="white")
            self.my_canvas.itemconfig(self.pin17, fill="white")
            self.my_canvas.itemconfig(self.pin18, fill="white")
            self.my_canvas.itemconfig(self.sensor_1, fill="white")
            self.my_canvas.itemconfig(self.sensor_2, fill="white")
            self.my_canvas.itemconfig(self.sensor_3, fill="white")
            Var1=item[0]
            Var2=item[1]
            Var3=item[2]
            self.label_1.config(text=str(Var1))
            self.label_2.config(text=str(Var2))
            self.label_3.config(text=str(Var3))

def CapSense_plot(q):
    viz = CapSense(q)
    while True:
        viz.update(q)



