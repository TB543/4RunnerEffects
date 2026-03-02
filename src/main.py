from customtkinter import CTk
from UI.PedalBoard import PedalBoard


root = CTk()
root.geometry("1024x600")
board = PedalBoard(root)
board._pedals.input_device = board._pedals.input_devices[-1]
board._pedals.output_device = board._pedals.output_devices[20]
board.pack(fill="both", expand=True)
root.mainloop()
