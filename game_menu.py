from tkinter import *
import time
from PIL import ImageTk, Image
from pygame import mixer

root = Tk()
root.geometry('500x550')
canv = Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

def create_main_menu():
    canv.delete(all)
    img = ImageTk.PhotoImage(Image.open("Textures\menu.jpg"))   #the only way to create background in function
    win = canv.create_image(0, 0, anchor=NW, image=img)

    mixer.init()       #playing intro music
    #play_intro_music()

    global buttons
    img2 = ImageTk.PhotoImage(Image.open("Buttons/push_start.jpg"))
    button2 = Button(root, image=img2, command=create_settings_menu)   #start button
    button2.place(x=100, y=350)
    buttons.append(button2)
    
    img3 = ImageTk.PhotoImage(Image.open("Buttons/settings.jpg"))
    button3 = Button(root, image=img3, command=create_settings_menu)   #settings button
    button3.place(x=50, y=355)
    buttons.append(button3)
    
    win.pack()   #!doesn't work if being removed! Leave it the last string in this function!
    
def create_settings_menu():
    global buttons
    if len(buttons) > 0:  #method bind doesn't work for music
        play_short_sound()
    canv.delete(all)  #deleting all, including buttons
    for b in buttons:
        b.destroy()
        
    img = ImageTk.PhotoImage(Image.open("Textures\settings.jpg"))
    win = canv.create_image(0, 0, anchor=NW, image=img)
    win.pack()    #!doesn't work if being removed! Leave it the last string in this function!

def play_short_sound():
    mixer.music.load('Music/button_sound.mp3')
    print('&')
    mixer.music.play()

def play_intro_music():
    mixer.music.load('Music/title.mp3.mid')
    mixer.music.play(-1)

'''root = Tk()
root.geometry('500x550')

canv = Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

img = ImageTk.PhotoImage(Image.open("Textures\menu.jpg"))
canv.create_image(0, 0, anchor=NW, image=img)'''

buttons =[]
create_main_menu()
