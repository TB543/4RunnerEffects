from customtkinter import CTk
from UI.PedalboardUI import PedalboardUI


root = CTk()
root.geometry("1024x600")
board = PedalboardUI(root)
board.pack(fill="both", expand=True)
root.mainloop()
