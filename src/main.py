from customtkinter import CTk
from UI.PedalBoard import PedalBoard


root = CTk()
root.geometry("1024x600")
PedalBoard(root).pack(fill="both", expand=True)
root.mainloop()
