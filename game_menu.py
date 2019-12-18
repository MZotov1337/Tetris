from tkinter import *
import time
from PIL import ImageTk, Image
from pygame import mixer

root = Tk()
root.geometry('500x550')
canv = Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

def create_main_menu():
    global buttons
    if len(buttons) > 0:  #method bind doesn't work for music
        play_short_sound()
    canv.delete(all)  #deleting all, including buttons
    for b in buttons:
        b.destroy()
        
    img = ImageTk.PhotoImage(Image.open("Textures\menu.jpg"))   #the only way to create background in function
    win = canv.create_image(0, 0, anchor=NW, image=img)

    play_intro_music()

    img2 = ImageTk.PhotoImage(Image.open("Buttons/push_start.jpg"))
    button2 = Button(root, image=img2, command=create_settings_menu)   #start button
    button2.place(x=100, y=350)
    buttons.append(button2)
    
    img3 = ImageTk.PhotoImage(Image.open("Buttons/settings.jpg"))
    button3 = Button(root, image=img3, command=create_settings_menu)   #settings button
    button3.place(x=50, y=355)
    buttons.append(button3)
    
    win.pack()   #!doesn't work if being removed! Leave as the last string of the function!
    
def create_settings_menu():
    global buttons
    if len(buttons) > 0:  #method bind doesn't work for music
        play_short_sound()
    canv.delete(all)  #deleting all, including buttons
    for b in buttons:
        b.destroy()
        
    img = ImageTk.PhotoImage(Image.open("Textures\settings.jpg"))
    win = canv.create_image(0, 0, anchor=NW, image=img)

    img4 = ImageTk.PhotoImage(Image.open("buttons/back.jpg"))
    button4 = Button(root, image=img4, command=create_main_menu) #back to main menu button
    button4.place(x=20, y=505)
    buttons.append(button4)

    global sound_on_off
    sound_button = Checkbutton(text="Звук", command = change_sound_existance, variable = sound_on_off, onvalue=1, offvalue=0)
    sound_button.place(x=20, y=20)   #sound checkbutton
    buttons.append(sound_button)
    sound_button.deselect()
    sound_on_off = False
    
    win.pack()    #!doesn't work if being removed! Leave as the last string of the function!

def play_short_sound():
    global sound_on_off
    if not(sound_on_off):
        return
    mixer.music.load('Music/button_sound.mp3')
    mixer.music.play()

def play_intro_music():
    global sound_on_off
    if not(sound_on_off):
        return
    mixer.music.load('Music/title.mp3.mid')
    mixer.music.play(-1)

def change_sound_existance():
    global sound_on_off
    sound_on_off = not(sound_on_off)
    print('&', sound_on_off)

'''root = Tk()
root.geometry('500x550')

canv = Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)

img = ImageTk.PhotoImage(Image.open("Textures\menu.jpg"))
canv.create_image(0, 0, anchor=NW, image=img)'''

mixer.init()   #initialising mixer for playing music
buttons =[]
sound_on_off = False
create_main_menu()
