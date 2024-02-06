import os
from tkinter import *
import tkinter.messagebox
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time
import tkfontchooser
import threading
from tkinter import messagebox


root = tk.ThemedTk()
style = ttk.Style()
root.get_themes()
root.set_theme("equilux")
root.resizable(0, 0)
root.configure(bg='#0b273c')

# create a menu bar
helv36 = tkfontchooser.Font(family="Verdana", size=8)
statusbar = Label(root, text="AudioCharm", anchor=W, font=helv36, fg="white")
statusbar.configure(bg="#0b273c")
statusbar.pack(side=BOTTOM, fill=X)

menubar = Menu(root)
root.config(menu=menubar)

# Create the submenu

subMenu = Menu(menubar, tearoff=0)

playlist = []
# playlist - contains the full path + filename
# playlistbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music function


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilenames()
    for song in filename_path:
        add_to_playlist(song)


def add_to_playlist(filename):
    if filename[-4:] == ".mp3":
        index = 0
        playlistbox.insert(index, os.path.basename(filename))
        playlist.insert(index, filename)
        index += 1
    else:
        messagebox.showerror("Error", "This file is not supported, please only add mp3 files.")


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


mixer.init()  # initializing the mixer


root.title("AudioCharm")
root.iconbitmap(r'images/icon.ico')  # Icon

changepause = False

leftframe = Frame(root)
leftframe.configure(bg="#0b273c")
leftframe.pack(side=LEFT, padx=50)

playlistbox = Listbox(leftframe, selectbackground="#0b273c")
playlistbox.pack(pady=20)

ttk.Style().configure("TButton", relief="flat", background="#0b273c")
btn1 = ttk.Button(leftframe, text="+ Add", command=browse_file, style="new_style.TButton")
btn1.pack(side=LEFT, pady=5)


def del_song():
    stop_music()
    selected_song_delete = playlistbox.curselection()
    selected_song_delete = int(selected_song_delete[0])
    playlistbox.delete(selected_song_delete)
    playlist.pop(selected_song_delete)


btn2 = ttk.Button(leftframe, text="- Delete", command=del_song)
btn2.pack(side=LEFT)

rightframe = Frame(root)
rightframe.configure(bg="#0b273c")
rightframe.pack()

filelabel = Label(rightframe, font=helv36)
filelabel.configure(bg="#0b273c", fg="white")
filelabel.pack(pady=(10, 0))

topframe = Frame(rightframe)
topframe.configure(bg="#0b273c")
topframe.pack()


pauseder = False


def show_details(play_song):

    global total_length
    filelabel['text'] = "Playing" + ' - ' + os.path.basename(play_song)
    file_data = os.path.splitext(play_song)
    if file_data[1] == ".mp3":
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        messagebox.showerror("Error", "AudioCharm could not find this file or the file is not supported. Please try again.")

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    slider_position = int(total_length)
    timeslider.config(to=slider_position, value=int(timeslider.get()))
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global pauseder
    global current_time
    # mixer.music.get_busy() - stops when music is paused
    current_time = int(timeslider.get())
    if int(current_time) == int(t):
        stop_music()

    while current_time <= t and mixer.music.get_busy():
        if int(current_time) == int(t):
            stop_music()
        if pauseder:
            if int(current_time) == int(t):
                stop_music()
            continue
        else:
            if int(current_time) == int(t):
                stop_music()
            current_time = int(timeslider.get()) + 1
            next_time = int(timeslider.get()) + 1
            mins, secs = divmod(next_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = timeformat
            timeslider.config(value=next_time)
            time.sleep(1)

        if int(current_time) == int(t):
            stop_music()
    if int(current_time) == int(t):
        stop_music()


def play_music():
    global total_length
    global changepause
    global paused
    global pauseder
    global selected_song
    global x
    global play_this

    try:
        paused  # Check if the paused variable has be initialized or not.
    except NameError:
        x = playlistbox.curselection()
        x = int(x[0])
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])

        try:
            # play_this = playlist[selected_song]
            if changepause:
                paused = True
                mixer.music.pause()
                statusbar['text'] = "Music Paused"
                playbtn.configure(image=play)
                pauseder = True

            else:
                stop_music()
                time.sleep(1)
                selected_song = playlistbox.curselection()
                selected_song = int(selected_song[0])
                play_this = playlist[selected_song]
                mixer.music.load(play_this)
                mixer.music.play()
                statusbar['text'] = "Playing Music - " + os.path.basename(play_this)
                show_details(play_this)
                playbtn.configure(image=pause)
                changepause = True

        except:
            tkinter.messagebox.showerror("File not found", "AudioCharm could not find this file or the file is not supported. Please try again.")
    else:  # If initialized then it runs this code
        x = playlistbox.curselection()
        x = int(x[0])
        play_it = playlist[x]
        if play_it == play_this:
            mixer.music.unpause()
            playbtn.configure(image=pause)
            statusbar['text'] = "Playing Music - " + os.path.basename(play_it)
            del paused
            pauseder = False
            if int(timeslider.get()) == int(total_length):
                mins, secs = divmod(timeslider.get(), 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                currenttimelabel.config(text=timeformat)
            elif int(timeslider.get() == int(current_time)):
                slider_position = int(total_length)
                timeslider.config(to=slider_position, value=int(timeslider.get()))
            else:
                mins, secs = divmod(timeslider.get(), 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                currenttimelabel['text'] = timeformat
                next_time = int(timeslider.get()) + 1
                timeslider.config(value=next_time)
        else:
            stop_music()
            time.sleep(1)
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music - " + os.path.basename(play_it)
            filelabel['text'] = "Playing - " + os.path.basename(play_it)
            file_data = os.path.splitext(play_it)
            if file_data[1] == ".mp3":
                audio = MP3(play_it)
                total_length = audio.info.length
            else:
                messagebox.showerror("Error", "AudioCharm could not find this file or the file is not supported. Please try again.")
            mins, secs = divmod(total_length, 60)
            mins = round(mins)
            secs = round(secs)
            del play_it
            play_this = playlist[selected_song]
            del paused
            playbtn.configure(image=pause)
            changepause = True
            pauseder = False
            # timeformat = '{:02d}:{:02d}'.format(mins, secs)
            # lengthlabel['text'] = "Total Length" + ' - ' + timeformat
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            # slider_position = int(total_length)
            # timeslider.config(to=slider_position, value=0)
            if int(timeslider.get()) == int(current_time):
                slider_position = int(total_length)
                timeslider.config(to=slider_position, value=int(current_time))
            else:
                mins, secs = divmod(timeslider.get(), 60)
                mins = round(mins)
                secs = round(secs)
                # timeformat = '{:02d}:{:02d}'.format(mins, secs)
                # currenttimelabel['text'] = timeformat
                slider_position = int(total_length)
                timeslider.config(to=slider_position, value=int(timeslider.get()))
            t1 = threading.Thread(target=start_count, args=(total_length,))
            t1.start()


def stop_music():
    global changepause
    mixer.music.stop()
    playbtn.configure(image=play)
    timeslider.config(value=0)
    currenttimelabel['text'] = "00:00"
    filelabel['text'] = ""
    statusbar['text'] = "Music Stopped"
    changepause = False


def set_vol(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)  # Sets volume of mixer, takes value of 0 to 1 only so must be divided by 100


muted = FALSE


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(50)
        volumebtn.configure(image=notmute)
        scale.set(50)
        muted = FALSE
    else:  # unmute music
        mixer.music.set_volume(0)
        volumebtn.configure(image=mute)
        scale.set(0)
        muted = TRUE


def time_slide(x):
    song = playlistbox.get(ACTIVE)
    mixer.music.load(play_this)
    mixer.music.play(loops=0, start=int(timeslider.get()))


middleframe = Frame(rightframe)
middleframe.configure(bg="#0b273c")
middleframe.pack(padx=10, pady=10)

bottomframe = Frame(rightframe)
bottomframe.configure(bg="#0b273c")
bottomframe.pack(padx=10, pady=10)
play = PhotoImage(file="images/play.png")
playbtn = Button(middleframe, image=play, command=play_music, borderwidth=0, relief=SUNKEN, activebackground='#0b273c')  # button that plays music
playbtn.configure(bg="#0b273c")
playbtn.grid(row=0, column=0, padx=10)

pause = PhotoImage(file="images/pause.png")

stop = PhotoImage(file="images/stop.png")
stopbtn = Button(middleframe, image=stop, command=stop_music, borderwidth=0, relief=SUNKEN, activebackground='#0b273c')  # button that stops music
stopbtn.configure(bg="#0b273c")
stopbtn.grid(row=0, column=1, padx=10)

mute = PhotoImage(file="images/mute.png")
notmute = PhotoImage(file="images/notmute.png")
volumebtn = Button(bottomframe, image=notmute, command=mute_music, borderwidth=0, relief=SUNKEN, activebackground='#0b273c')  # button that mutes music
volumebtn.configure(bg="#0b273c")
volumebtn.grid(row=0, column=0, pady=(16, 0), padx=(200, 0))

style2 = ttk.Style()
style2.map("TScale", background=[('!disabled', '#0b273c')])
style2.configure('TScale', focuscolor=root.cget("background"))

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, style="TScale", command=set_vol, takefocus=False)  # Change volume
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row=0, column=1, pady=(17, 0))

timeslider = ttk.Scale(bottomframe, from_=0, to=100, value=0, orient=HORIZONTAL, command=time_slide)  # showvalue='no'
timeslider.grid(row=13, column=0, columnspan=10, sticky='wse', pady=(35, 0))

currenttimelabel = Label(root, text='', font=helv36)
currenttimelabel.configure(bg="#0b273c", fg="white")
currenttimelabel.pack(padx=(0, 280))



def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()  # Make the window constantly run
