import tkinter as tk
from main import Player

root = tk.Tk()
root.geometry('800x532')
root.wm_title('Aditya Music Player')
root.resizable(False, False)

app = Player(master=root)
app.mainloop()