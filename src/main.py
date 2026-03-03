from customtkinter import CTk
from UI.PedalBoard import PedalBoard


root = CTk()
root.geometry("1024x600")
board = PedalBoard(root)
board._audio.input_device = board._audio.input_devices[-1]
board._audio.output_device = board._audio.output_devices[20]
board.pack(fill="both", expand=True)
root.mainloop()
