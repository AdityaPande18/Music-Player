import os
import time
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import tkinter.ttk as ttk
import vlc

class Player(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()

		if os.path.exists('songs.pickle'):
			with open('songs.pickle', 'rb') as f:
				self.playlist = pickle.load(f)
		else:
			self.playlist=[]

		self.dark = "#424040"  
		self.light = "#494747" 
		self.lighter = "#4f4f4f"

		# Images
		self.nextImage = PhotoImage(file = 'images/next.gif')
		self.prevImage = PhotoImage(file='images/previous.gif')
		self.playImage = PhotoImage(file='images/play.gif')
		self.pauseImage = PhotoImage(file='images/pause.gif')

		# Variables
		self.count = 0
		self.current = 0
		self.paused = True
		self.played = False
		self.song = vlc.MediaPlayer() 

		# Methods
		self.create_frames()
		self.track_widgets()
		self.control_widgets()
		self.tracklist_widgets()

	# UI Components
	def create_frames(self):
		# Song Track Section (UI)
		self.track = tk.LabelFrame(self, text='Song Track', 
					font=("times new roman",15,"bold"),
					bg=self.lighter,fg="white",bd=3,relief=tk.GROOVE)
		self.track.grid(row=0, column=0)

		# PlayList Section (UI)
		self.tracklist = tk.LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',
							font=("times new roman",15,"bold"),
							bg=self.light,fg="white",bd=3, relief=tk.GROOVE)
		self.tracklist.config(width=300,height=525)
		self.tracklist.grid(row=0, column=1, rowspan=3)

		# Bottom Controls Section (UI)
		self.controls = tk.LabelFrame(self,
							font=("times new roman",15,"bold"),
							bg=self.lighter,fg="white",bd=3,relief=tk.GROOVE)
		self.controls.grid(row=1, column=0)

	# Track all the songs in a folder
	def track_widgets(self):

		self.canvas = tk.LabelFrame(self.track, text=f'Folders',
							font=("times new roman",15,"bold"),
							bg=self.light,fg="white",bd=3, relief=tk.GROOVE)
		self.canvas.config(width=550,height=330, highlightbackground = "red", highlightcolor= "red")
		self.canvas.grid(row=0, column=0)

		self.listfolder = tk.Listbox(self.canvas, background=self.lighter, fg='white', selectmode=tk.SINGLE,
					 		selectbackground='sky blue')

		self.listfolder.config(height=15, width=68)
		self.listfolder.grid(row=0, column=0, rowspan=5)
		self.listfolder.insert(0, "All the songs list goes here...")
		self.listfolder.insert(1, "Under development right now!!")


		self.songtrack = tk.Label(self.track, font=("Batang",13,"bold"),
						bg=self.lighter,fg="white")
		self.songtrack['text'] = 'Aditya MP3 Player'
		self.songtrack.config(width=50, height=1)
		self.songtrack.grid(row=1,column=0)

		self.songSlider = ttk.Scale(self.track, from_ = 0, to = 100, orient = tk.HORIZONTAL, length=500)
		self.songSlider.set(0)
		self.songSlider.grid(row=2, column=0, padx=19, pady=19)

		self.songLength = tk.Label(self.track, font=("Batang",12,"normal"),
						bg=self.lighter,fg="white")
		self.songLength.config(width=50, height=1)
		self.songLength.grid(row=3,column=0)


	# Control Section Bottom (UI)
	def control_widgets(self):
		# Load song button
		self.loadSongs = tk.Button(self.controls, bg=self.lighter, fg='white', font=10)
		self.loadSongs['text'] = 'Load Songs'
		self.loadSongs['command'] = self.retrieve_songs
		self.loadSongs.config(padx=30)
		self.loadSongs.grid(row=0, column=0)

		# Previous button
		self.prev = tk.Button(self.controls, image=self.prevImage)
		self.prev['command'] = self.prev_song
		self.prev.grid(row=0, column=1, padx=19, pady=19)

		# Pause button
		self.pause = tk.Button(self.controls, image=self.pauseImage)
		self.pause['command'] = self.pause_song
		self.pause.grid(row=0, column=2, padx=19, pady=19)

		# Next button
		self.next = tk.Button(self.controls, image=self.nextImage)
		self.next['command'] = self.next_song
		self.next.grid(row=0, column=3, padx=19, pady=19)

		# Volume scroll
		self.volume = tk.DoubleVar(self)
		self.slider = tk.Scale(self.controls, from_ = 0, to = 100, bg=self.lighter, fg='white',activebackground=self.lighter, orient = tk.HORIZONTAL)
		self.slider['variable'] = self.volume
		self.slider.set(80)
		self.slider['command'] = self.change_volume
		self.slider.grid(row=0, column=4, padx=19, pady=19)

	# Tacklist of all the songs in list right now (Side panel)
	def tracklist_widgets(self):
		self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL, background=self.light, activebackground=self.dark, highlightbackground=self.lighter)
		self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

		self.list = tk.Listbox(self.tracklist, background=self.lighter, fg='white', selectmode=tk.SINGLE,
					 yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
		self.enumerate_songs()
		self.list.config(height=28, width=27)
		self.list.bind('<Double-1>', self.play_song) 
		self.list.bind('<Button-1>', self.change_bg) 

		self.scrollbar.config(command=self.list.yview)
		self.list.grid(row=0, column=0, rowspan=5)

	# Change the text & bg color of playlist element
	# Default is normal blue it chnages it to white
	def change_bg(self, event=None):
		if event is not None:
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, selectbackground='white', selectforeground=self.lighter)

	# Play song
	def play_song(self, event=None):
		self.song.stop()
		if event is not None:
			self.current = self.list.curselection()[0]
			for i in range(len(self.playlist)):
				self.list.itemconfigure(i, selectbackground='white', selectforeground=self.lighter)

		self.song = vlc.MediaPlayer(self.playlist[self.current])
		self.songtrack['anchor'] = 'c' 
		self.songtrack['text'] = os.path.basename(self.playlist[self.current])

		self.songLength['anchor'] = 'c' 

		self.pause['image'] = self.playImage
		self.paused = False
		self.played = True
		self.list.activate(self.current) 

		self.song.play()
		self.show_song_length()
		i = 0
		while self.song.get_length() == 0:
			i += 1
		self.songSlider['to'] = self.song.get_length() / 1000
		self.songSlider.set(0)

	# Pause song
	def pause_song(self):
		if not self.paused:
			self.paused = True
			self.song.pause()
			self.pause['image'] = self.pauseImage
		else:
			if self.played == False:
				self.play_song()
			self.paused = False

			self.song.play()
			self.pause['image'] = self.playImage

	# Previous song
	def prev_song(self):
		if self.current > 0:
			self.current -= 1
			self.list.itemconfigure(self.current + 1, bg=self.lighter)
		else:
			self.current = len(self.playlist) - 1
			self.list.itemconfigure(self.current, bg=self.lighter)
		self.play_song()

	# Next song
	def next_song(self):
		if self.current < len(self.playlist) - 1:
			self.current += 1
			self.list.itemconfigure(len(self.playlist) - 1, bg=self.lighter)
		else:
			self.current = 0
			self.list.itemconfigure(self.current, bg=self.lighter)
		self.play_song()

	# Retrieve all songs from the folder (Load song button)
	# Only retrieve's MP3 files
	def retrieve_songs(self):
		self.songlist = []
		directory = filedialog.askdirectory()
		for root_, dirs, files in os.walk(directory):
				for file in files:
					if os.path.splitext(file)[1] == '.mp3':
						path = (root_ + '/' + file).replace('\\','/')
						self.songlist.append(path)

		# Saves song in pickel file
		with open('songs.pickle', 'wb') as f:
			pickle.dump(self.songlist, f)
		self.playlist = self.songlist
		self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
		self.list.delete(0, tk.END)
		self.enumerate_songs()

	# Insert songs in playlist section
	def enumerate_songs(self):
		for index, song in enumerate(self.playlist):
			self.list.insert(index, os.path.basename(song))

	# Change volume
	def change_volume(self, event=None):
		self.v = self.volume.get()
		self.song.audio_set_volume(int(self.v))

	# show current time of the song
	def show_song_length(self):
		curr_time_millis = self.song.get_time()
		curr_time_secs = curr_time_millis / 1000
		
		converted_curr_time_secs = time.strftime('%M:%S', time.gmtime(curr_time_secs))

		total_time_millis = self.song.get_length()
		total_time_secs = total_time_millis / 1000
		converted_total_time_secs = time.strftime('%M:%S', time.gmtime(total_time_secs))

		self.songLength.config(text=f"Time Elapsed: {converted_curr_time_secs} of {converted_total_time_secs}")

		self.songSlider.set(curr_time_secs)

		self.songLength.after(1000, self.show_song_length)
