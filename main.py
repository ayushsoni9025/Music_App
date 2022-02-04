from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import shutil
import pygame
from tkinter import ttk
from PIL import Image, ImageTk
import os

#data
paused = False

class MusicApp:
    def __init__(self, Music_App):
        self.get_song()
        self.Music_App = Music_App
        # interface
        Music_App.title("Music App")
        Music_App.iconbitmap("App_icon.ico")
        device_height = Music_App.winfo_screenheight()
        device_width = Music_App.winfo_screenwidth()
        Music_App.geometry(str(device_width)+"x"+str(device_height)+"+0+0")

        # frame
        global mode_frame
        mode_frame = Frame(Music_App,  bg="black",
                           highlightbackground="green", highlightthickness=2)
        mode_frame.place(x=device_width/4, y=0, width=3 * device_width /
                         4, height=device_height/8)

        global option_frame
        option_frame = Frame(Music_App, bd=3, bg="black",
                             highlightbackground="red", highlightthickness=2)
        option_frame.place(x=0, y=0, width=device_width /
                           4, height=device_height)

        global song_frame
        song_frame = Frame(Music_App, bd=3, bg="black",
                           highlightbackground="blue", highlightthickness=2)
        song_frame.place(x=device_width/4, y=device_height/8, width=3 *
                         device_width/4, height=5*device_height/8)

        global play_song_frame
        play_song_frame = Frame(
            Music_App, bd=3, bg="black", highlightbackground="yellow", highlightthickness=2)
        play_song_frame.place(x=device_width/4, y=3*device_height/4,
                              width=3*device_width/4, height=device_height/4)

        # lable
        image = Image.open("logo1.png").resize((75, 75), Image.ANTIALIAS)
        logo_image = ImageTk.PhotoImage(image)
        logo_label = Label(option_frame, image=logo_image, bg="black")
        logo_label.image = logo_image
        logo_label.grid(row=0, column=0, rowspan=2, pady=10)

        title_lable_1 = Label(option_frame, text="WORLD", font=(
            "times new roman", 30, "bold"), fg="red", bg="black")
        title_lable_1.grid(row=0, column=1)

        title_lable_2 = Label(option_frame, text="OF MUSIC", font=(
            "times new roman", 20, "bold"), fg="white", bg="black")
        title_lable_2.grid(row=1, column=1)

        # self.play_sound_lable(songs[0])

        search_bar = Entry(option_frame, font=("times new roman", 14), relief="sunken", width=int(
            device_width/20-35))
        search_bar.grid(row=2, column=0, columnspan=2, padx=10)

        # button
        search_button = Button(option_frame, text="Search", width=15, font=(
            "times new roman", 12, "bold"), fg="red", command = lambda: self.song_searched(search_bar))
        search_button.grid(row=3, column=1, pady=10)

        about_app = Button(option_frame, text="About World of Music", fg="red", font=(
            "times new roman", 11), relief="raised", width=int(device_width/20-40), command=self.about_app)
        about_app.grid(row=4, column=0, columnspan=2, pady=10)

        exit_app = Button(option_frame, text="Exit App", fg="red", font=("times new roman", 11),
                          relief="raised", width=int(device_width/20-40), command=Music_App.quit)
        exit_app.grid(row=5, column=0, columnspan=2)

        add_song = Button(mode_frame, text="Add Song", fg="green",
                          font=("times new roman", 11), width=30, command=self.add_song_pressed)
        add_song.grid(row=0, column=0, padx=25, pady=25)

        remove_song = Button(mode_frame, text="Remove Song",
                             fg="green", font=("times new roman", 11), width=30, command = lambda: self.remove_song_pressed(row[0]))
        remove_song.grid(row=0, column=1, padx=25, pady=25)




        # Table Frame
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("Treeview", background="black",
                        fieldbackground="black", foreground="white")

        global song_list
        song_list = ttk.Treeview(song_frame)

        song_list["columns"] = ("song")

        song_list.column("#0", width=50, anchor=CENTER)
        song_list.column("song", width=900, anchor=W)
        # song_list.column("location", width=75, anchor=W)
        # song_list.column("artist", width=270, anchor=CENTER)

        song_list.heading("#0", text="S.NO.")
        song_list.heading("song", text="Song")
        # song_list.heading("location", text="Location")
        # song_list.heading("artist", text="Artist")

        scroll_y = Scrollbar(song_frame, orient=VERTICAL, command=song_list.yview).pack(
            side=RIGHT, fill=Y, expand=1)
        
        self.fatch_data(song_list)
        song_list.bind("<ButtonRelease-1>",self.play_table_song)
        song_list.pack(padx=10, pady=10, fill=Y, expand=1)

    def get_song(self):
        global songs
        songs=os.listdir("Songs/")

    def fatch_data(self, song_list):
        song_list.delete(*song_list.get_children())
        counter = 1
        for song in songs:
            # song = song.replace(" ", "")
            song_list.insert(parent='', index='end', iid=counter,
                            text=counter, values=(song,))
            counter+=1

    def play_table_song(self, event):
        cursour = song_list.focus()
        content = song_list.item(cursour)

        global row
        row = content["values"]
        self.play()

    def play(self):
        if pygame.mixer.get_busy() is True:
            pygame.mixer.stop()
        global paused
        paused = False
        self.forget_pack()
        self.play_sound_lable(row[0])
        
        path = 'Songs\\'+row[0]
        pygame.mixer.init()
        sounda = pygame.mixer.Sound(path)
        sounda.play()
  
    def forget_pack(self):
        try:
            current_playing.place_forget()
        except:
            pass

    def play_sound_lable(self, song):
        global current_playing          
        current_playing = Label(
            play_song_frame, text=str(song), bg="black", fg="white")
        current_playing.place(x = 45, y = 25)
        global paused
        if paused == True:
            play_button = Button(play_song_frame, text="▶️", height=1, width=3, relief=FLAT, font=(
                "times new roman", 20, "bold"), fg="yellow", bg="black", command= self.play_pause_music).place(x=110, y = 60)
        else:    
            play_button = Button(play_song_frame, text="⏸", height=1, width=3, relief=FLAT, font=(
                "times new roman", 20, "bold"), fg="yellow", bg="black", command= self.play_pause_music).place(x=110, y = 60)

        prev_button = Button(play_song_frame, text="⮜", height=1, width=3, relief=FLAT, font=(
            "times new roman", 20, "bold"), fg="yellow", bg="black", command = lambda: self.next_button_pressed(row[0], "prev")).place(x = 45, y= 60)
        next_button = Button(play_song_frame, text="➤", height=1, width=3, relief=FLAT, font=(
            "times new roman", 20, "bold"), fg="yellow", bg="black", command =lambda: self.next_button_pressed(row[0], "next")).place(x=175, y=60)
        # repeat_button = Button(play_song_frame, text="🔁", height=1, width=3, relief=FLAT, font=(
        #     "times new roman", 20, "bold"), fg="yellow", bg="black").place(x = 240, y = 60)
    
    def play_pause_music(self):
        global paused
        if paused == True:
            pygame.mixer.unpause()
            paused = False
        else:
            pygame.mixer.pause()
            paused = True

        self.play_sound_lable(row[0])

    def next_button_pressed(self,current_playing, command):
        global row
        try:
            count = 0
            for song in songs:
                if current_playing == song:
                    if command == "next":
                        row[0] = songs[count+1]
                    elif command == "prev":
                        row[0] = songs[count-1]

                    break
                count+=1
        except:
            if command == "next":
                row[0] = songs[0]
            elif command == "pre":
                row[0] = songs[len(songs)-1]
        self.play()

    def remove_song_pressed(self, current_playing):       
        os.remove("Songs\\"+current_playing)
        songs.remove(current_playing)
        global song_list
        self.fatch_data(song_list)
        self.forget_pack()
        pygame.mixer.stop()
    
    def add_song_pressed(self):
        added_song = filedialog.askopenfilename(initialdir="Songs", title="Add Song", filetypes=(("MP3 files", "*.mp3"),("all files","*.*")))
        shutil.copy(added_song, "Songs\\")
        self.get_song()
        self.fatch_data(song_list)
    
    def song_searched(self, search_bar):
        text = search_bar.get()
        search_bar.delete(0,"end")
        text = text.lower()
        self.get_song()
        for song in songs:
            if text in song.lower():
                pass
            else:
                songs.remove(song)
        self.fatch_data(song_list)

    @staticmethod
    def about_app():
        actual_message = "Music App is Python Application\nBuild by Indore Institute of Science and Technology, Rau \nDeveloper are:\nAyush Soni, Electronic and Communication Engineering Student"
        messagebox.showinfo("About App", actual_message)
root = Tk()
MusicApp(root)
root.mainloop()