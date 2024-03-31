from tkinter import *
from tkinter import font
from os import path, _exit
import random
import threading
from webbrowser import open as webopen
from time import sleep



current_dir = path.dirname(path.realpath(__file__))
root = Tk()
root.title("MHP Simulator")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
x = int((root.winfo_screenwidth() - width)/2)
y = int((root.winfo_screenheight() - height)/2) 
root.geometry(f"{width}x{height}+{x}+{y}")
root.iconbitmap(f"{current_dir}\\images\\mhp_logo.ico")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#Images
od_image = PhotoImage(file = f"{current_dir}\\images\\door_open.PNG")
cd_image = PhotoImage(file = f"{current_dir}\\images\\door_closed.PNG")
md_image = PhotoImage(file = f"{current_dir}\\images\\door_marked.PNG") 
wd_image = PhotoImage(file = f"{current_dir}\\images\\door_winner.PNG")
info_icon = PhotoImage(file=f"{current_dir}\\images\\info.png")
github_icon = PhotoImage(file=f"{current_dir}\\images\\github.png")


#Credits window
def credits():
    win = Toplevel(root)
    win.title("Credits")
    width = int(root.winfo_screenwidth()/4)
    height = int(root.winfo_screenheight()/3.5)
    x = int((root.winfo_screenwidth() - width)/2)
    y = int((root.winfo_screenheight() - height)/2) 
    win.geometry(f"{width}x{height}+{x}+{y}")
    win.resizable(False, False)
    win.iconbitmap(f"{current_dir}\\images\\mhp_logo.ico")
    win.rowconfigure((0,1,2,3,4,5), weight=1)
    win.columnconfigure(0, weight=1)
    it_font = font.Font(slant="italic")
    sum = Label(win, text=",,A program to simulate the Monty Hall problem''", font=it_font)
    sum.grid(row=0, column=0)
    bold_font = font.Font(weight="bold")
    creator = Label(win, text="Made by Gergo Magyar", font=bold_font)
    creator.grid(row=1, column=0, sticky="n")
    gitb = Button(win, image=github_icon, borderwidth=0, command=lambda: webopen("github.com/Magrgo"))
    gitb.grid(row=2, column=0, sticky="n")
    picc = Label(win, text="Images from Vecteezy.com", font=bold_font)
    picc.grid(row=4, column=0)
    backb = Button(win, text="Back", font=("Calibri", 10), command=lambda:win.destroy())
    backb.grid(row=5, column=0)
    win.mainloop()


#Door object
class Door: 
    def __init__(self, master, cnum):
        self.door = Button(master, image=cd_image, borderwidth=0, width=350, height=450, background="white", command=lambda: self.mark())
        self.door.grid(row=1, column=cnum)
        self.cnum = cnum
        self.isMarked = False
        self.isOpen = False
        self.isActive = False

    def open(self):
        self.isOpen = True
        self.door.config(image=od_image)

    def close(self):
        self.isOpen = False
        self.door.config(image=cd_image)

    def mark(self):
        if self.isActive:
            self.isMarked = True
            self.door.config(image=md_image)

    def show_win(self):
        self.isOpen = True 
        self.door.config(image=wd_image)



#Using threading because of tkinter so that simulation runs separately from GUI
def sthread():
    t = threading.Thread(target=simdecide)
    t.start()



#Reading statistics of winning (In txt, first line is all games played, second is number of wins by switching, and third line is number of wins by staying)
def readstat():
    f = open(f"{current_dir}\\stat.txt")
    all_withsw = int(f.readline())
    win_withsw = int(f.readline())
    all_withoutsw = int(f.readline())
    win_withoutsw = int(f.readline())
    f.close()
    if all_withsw == 0:
        win_withsw = 0
        perc_sw = 0.0
    else:
        perc_sw = round(win_withsw/all_withsw*100, 1)
    if all_withoutsw == 0:
        win_withoutsw = 0
        perc_nosw = 0.0
    else:
        perc_nosw = round(win_withoutsw/all_withoutsw*100, 1)
    return all_withsw, win_withsw, all_withoutsw, win_withoutsw , perc_sw, perc_nosw



#Edit statistics of winning
def addstat(win, bySwitch):
    f = open(f"{current_dir}\\stat.txt")
    all_withsw = int(f.readline())
    win_withsw = int(f.readline())
    all_withoutsw = int(f.readline())
    win_withoutsw = int(f.readline())
    f.close()
    if bySwitch:
        all_withsw += 1
        if win:
            win_withsw += 1
    else:
        all_withoutsw += 1
        if win:
            win_withoutsw += 1 
    string = f"{all_withsw}\n{win_withsw}\n{all_withoutsw}\n{win_withoutsw}"
    f = open(f"{current_dir}\\stat.txt", "w")
    f.write(string)
    f.close()



#Clear statistics
def clearstat():
    f = open(f"{current_dir}\\stat.txt", "w")
    f.write("0\n0\n0\n0")
    f.close()
    perc.config(text="Win by switching: 0\\0: 0.0%")
    perc2.config(text=f"Win by staying: 0\\0: 0.0%")


#Reset everything after done with game
def reset():
    simb.config(state=NORMAL)
    autocb.config(state=NORMAL)
    simb.config(text="Simulate")
    simb.config(command=sthread)
    title.config(text="MH problem simulator")
    door1.close()
    door2.close()
    door3.close()


#Main process apart from GUI, the simulation itself
def simulate():
    simb.config(state=DISABLED)
    title.config(text="Choose a door!")
    for door in [door1, door2, door3]:          #Activating doors for selection
        door.isActive = True
    dnums = [1,2,3]
    winner_door_num = random.randint(1,3)
    dnums.remove(winner_door_num)
    
    #Constantly checking if a door has been selected
    selected_door_num = 0
    shouldBreak = False
    while shouldBreak != True:
        for i, door in enumerate([door1,door2,door3], start=1):         
            if door.isMarked:
                selected_door_num = i
                door.isMarked = False         #Turning off marked variable because door selection will need to be checked again*
                shouldBreak = True
                break
        sleep(0.2)

    for door in [door1, door2, door3]:      #Deactivating doors for dialog
        door.isActive = False
    sleep(0.5)

    title.config(text="Okay!")
    sleep(1.5)
    title.config(text="Now I'll help you a little!")
    sleep(2)
    try:
        dnums.remove(selected_door_num)
    except ValueError:                      #Delete marked/selected door from remaining. If it was already deleted(cause it's the winner), then pass 
        pass
    
    #Select a random door from remaining and open it
    odoor_num = random.choice(dnums)
    if odoor_num == 1:
        door1.open()
    elif odoor_num == 2:
        door2.open()
    elif odoor_num == 3:
        door3.open()
    sleep(1.5)

    title.config(text="I opened a door for you!")
    sleep(2)
    title.config(text="Do you want to change?")
    sleep(1.5)
    title.config(text="Confirm your choice!")
    sleep(1)

    i = 1
    for door in [door1, door2, door3]:
        if i != odoor_num:                             #Activating the doors except the one that's opened
            door.isActive = True
        i += 1

    #Waiting for choice confirm*
    shouldBreak = False
    previous_door_num = selected_door_num
    while shouldBreak != True:
        for i, door in enumerate([door1,door2,door3], start=1):         
            if door.isMarked:
                selected_door_num = i
                door.isMarked = False
                shouldBreak = True
                break
        sleep(0.2)

    switched = False
    if previous_door_num == selected_door_num:
        title.config(text="You stayed!")
    else:
        ([door1,door2,door3][previous_door_num-1]).close()     #Deleting the mark from previous door
        title.config(text="You switched!")
        switched = True
    sleep(1.5)

    title.config(text="Let's see the prize!")
    sleep(2)
    ([door1,door2,door3][winner_door_num-1]).show_win()
    sleep(1.5)
    phrases = {1:"first", 2:"second", 3:"third"}
    title.config(text=f"Behind the {phrases[winner_door_num]} door!")
    sleep(1.5)

    win = (selected_door_num == winner_door_num)
    if win:
        title.config(text="You win!")
    else:                                          #Decide if we won, and save stats
        title.config(text="You lose!")
    addstat(win, switched)

    all_sw, win_sw, all_nosw, win_nosw, perc_sw, perc_nosw = readstat()
    perc.config(text=f"Win by switching: {win_sw}\{all_sw}: {perc_sw}%")
    perc2.config(text=f"Win by staying: {win_nosw}\{all_nosw}: {perc_nosw}%")
    sleep(2)
    reset()


#Stopping simulation(waits until the end and then stops it)
def stopsim():
    autosim.set(False)
    autocb.config(state=DISABLED)
    simb.config(state=DISABLED)


#Custom sleep function for auto simulation, time divided by speed (SleepWithSpeed)
def sleepws(time):
        currspeed = simspeed.get()     
        sleep(time/currspeed)


#Automatic simulation
def auto_simulate():
    sc.config(state=NORMAL)
    while autosim.get():
        title.config(text="Choose a door!")
        simb.config(text="Stop")
        simb.config(command=stopsim)

        dnums = [1,2,3]
        winner_door_num = random.randint(1,3)
        dnums.remove(winner_door_num)
        sleepws(1.5)
        
        for door in [door1, door2, door3]:          #Activating doors for selection
            door.isActive = True

        selected_door_num = random.randint(1,3)
        ([door1,door2,door3][selected_door_num-1]).mark()
        ([door1,door2,door3][selected_door_num-1]).isMarked = False

        for door in [door1, door2, door3]:      #Deactivating doors for dialog
            door.isActive = False
        sleepws(1.5)

        title.config(text="Okay!")
        sleepws(1.5)
        title.config(text="Now I'll help you a little!")
        sleepws(2)
        try:
            dnums.remove(selected_door_num)
        except ValueError:                      #Delete marked/selected door from remaining. If it was already deleted(cause it's the winner), then pass 
            pass
        
        #Select a random door from remaining and open it
        odoor_num = random.choice(dnums)
        if odoor_num == 1:
            door1.open()
        elif odoor_num == 2:
            door2.open()
        elif odoor_num == 3:
            door3.open()
        sleepws(1.5)

        title.config(text="I opened a door for you!")
        sleepws(2)
        title.config(text="Do you want to change?")
        sleepws(1.5)
        title.config(text="Confirm your choice!")

        i = 1
        for door in [door1, door2, door3]:
            if i != odoor_num:                             #Activating the doors except the one that's opened
                door.isActive = True
            i += 1

        previous_door_num = selected_door_num
        selected_door_num = random.randint(1,3)
        while selected_door_num == odoor_num:
            selected_door_num = random.randint(1,3)
        ([door1,door2,door3][selected_door_num-1]).mark()
        ([door1,door2,door3][selected_door_num-1]).isMarked = False

        switched = False
        if previous_door_num == selected_door_num:
            title.config(text="You stayed!")
        else:
            ([door1,door2,door3][previous_door_num-1]).close()     #Deleting the mark from previous door
            title.config(text="You switched!")
            switched = True
        sleepws(1.5)

        title.config(text="Let's see the prize!")
        sleepws(2)
        ([door1,door2,door3][winner_door_num-1]).show_win()
        sleepws(1.5)
        phrases = {1:"first", 2:"second", 3:"third"}
        title.config(text=f"Behind the {phrases[winner_door_num]} door!")
        sleepws(1.5)

        win = (selected_door_num == winner_door_num)
        if win:
            title.config(text="You win!")
        else:                                          #Decide if we won, and save stats
            title.config(text="You lose!")
        addstat(win, switched)
        sleepws(1.5)

        all_sw, win_sw, all_nosw, win_nosw, perc_sw, perc_nosw = readstat()
        perc.config(text=f"Win by switching: {win_sw}\{all_sw}: {perc_sw}%")
        perc2.config(text=f"Win by staying: {win_nosw}\{all_nosw}: {perc_nosw}%")
        reset()
        sleepws(0.5)
    else:
        simspeed.set(1)
        sc.config(state=DISABLED)


#Function for deciding if the simulation is automatic or not
def simdecide():
    if autosim.get():
        auto_simulate()
    else:
        simulate()


#GUI Widgets:
mFrame = Frame(root, background="white")
mFrame.grid(row=0, column=0, sticky="nsew")
mFrame.rowconfigure((0,1,2,3,4), weight=1)
mFrame.columnconfigure((0,1,2,3,4), weight=1)

title = Label(mFrame, text="MH problem simulator", font=('Helvetica bold', 25), background="white")
title.grid(row=0, column=2)
title2 = Label(mFrame, text="")
title2.grid(row=0, column=1)
title3 = Label(mFrame, text="")
title3.grid(row=0, column=3)

door1 = Door(mFrame, 1)
door2 = Door(mFrame, 2)
door3 = Door(mFrame, 3)

simspeed = IntVar()
simspeed.set(1.0)
sc = Scale(mFrame, variable=simspeed, from_=1, to=10)
sc.grid(row=1, column=3, sticky="e")
sc.config(state=DISABLED)
sc_label = Label(mFrame, text="Speed")
sc_label.grid(row=1, column=3, sticky="en", pady=height/6.8)

simb = Button(mFrame, text="Simulate", font=('Calibri', 15), command=sthread)
simb.grid(row=2, column=2)

autosim = BooleanVar(root)
autocb = Checkbutton(mFrame, text="Auto-simulate", variable=autosim)
autocb.grid(row=2, column=2, sticky="s")

all_sw, win_sw, all_nosw, win_nosw, perc_sw, perc_nosw = readstat()
perc = Label(mFrame, text=f"Win by switching: {win_sw}\{all_sw}: {perc_sw}%", background="white", font=("Times New Roman", 18))
perc.grid(row=3, column=2)
perc2 = Label(mFrame, text=f"Win by staying: {win_nosw}\{all_sw}: {perc_nosw}%", background="white", font=("Times New Roman", 18))
perc2.grid(row=3, column=2, sticky="s")
clearb = Button(mFrame, text="Clear", background="#DCDCDC", borderwidth=0, command=clearstat)
clearb.grid(row=4, column=2, sticky="n", pady=15)
infob = Button(mFrame, image=info_icon, width=50, height=50, background="white", borderwidth=0, command=credits)
infob.grid(row=0, column=4, sticky="ne", padx=15)


root.mainloop()
_exit(1)