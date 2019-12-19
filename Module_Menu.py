from tkinter import *
import time
from PIL import ImageTk, Image
from pygame import mixer
from SuperCode import *

def create_main_menu():
    global buttons, win_menu, images
    if len(buttons) > 0:  #method bind doesn't work for music
        play_short_sound()
    canv.delete(all)  #deleting all, including buttons
    for b in buttons:
        b.destroy()
    for b in images:
        canv.delete(b)

    img = ImageTk.PhotoImage(Image.open("Textures\menu.jpg"))   #the only way to create background in function
    images.append(img)
    win_menu = Label(text = '', image = img)
    win_menu.place(x=0, y=0)

    play_intro_music()

    img2 = ImageTk.PhotoImage(Image.open("Buttons/push_start.jpg"))
    button2 = Button(root, image=img2, command=start_of_starting_game)   #start button
    button2.place(x=100, y=350)
    buttons.append(button2)
    images.append(img2)
    
    img3 = ImageTk.PhotoImage(Image.open("Buttons/settings.jpg"))
    button3 = Button(root, image=img3, command=create_settings_menu)   #settings button
    button3.place(x=55, y=350)
    buttons.append(button3)
    images.append(img3)

    img4 = ImageTk.PhotoImage(Image.open("Buttons/exit.jpg"))
    button4 = Button(root, image=img4, command=create_exit_menu)   #settings button
    button4.place(x=54, y=390)
    buttons.append(button4)
    images.append(img4)
    
def create_settings_menu():
    global buttons, win_menu, images
    if len(buttons) > 0:  #method bind doesn't work for music
        play_short_sound()
    canv.delete(all)  #deleting all, including buttons
    for b in buttons:
        b.destroy()
        
    img = ImageTk.PhotoImage(Image.open("Textures\settings.jpg"))
    images.append(img)
    win_menu = Label(text = '', image = img)
    win_menu.place(x=0, y=0)

    img5 = ImageTk.PhotoImage(Image.open("buttons/back.jpg"))
    button5 = Button(root, image=img5, command=create_main_menu) #back to main menu button
    button5.place(x=20, y=505)
    buttons.append(button5)
    images.append(img5)

    global sound_on_off
    sound_button = Checkbutton(text="Звук", command = change_sound_existance, variable = sound_on_off, onvalue=1, offvalue=0)
    sound_button.place(x=20, y=20)   #sound checkbutton
    buttons.append(sound_button)
    sound_button.deselect()
    sound_on_off = False

def stop_game():
    exit()

def create_exit_menu():
    global buttons
    yes = Radiobutton(text = 'Выход', font = 'Times 30', command = stop_game)
    no = Radiobutton(text = 'Отмена', font = 'Times 30', command = create_main_menu)
    buttons.append(yes)
    buttons.append(no)
    yes.place(x=90, y=260)
    no.place(x=250, y=260)

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

def open_game():
    global root
    root = Tk()
    root.geometry('500x550')
    global canv
    canv = Canvas(root,bg='white')
    canv.pack(fill=BOTH,expand=1)
    global images
    images = []
    mixer.init()   #initialising mixer for playing music
    global buttons
    buttons =[]
    global sound_on_off
    sound_on_off = False
    create_main_menu()

open_game()
