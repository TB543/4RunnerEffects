from customtkinter import CTk
from UI.PedalBoard import PedalBoard


root = CTk()
root.geometry("1024x600")
board = PedalBoard(root)
board.pack(fill="both", expand=True)
root.mainloop()
