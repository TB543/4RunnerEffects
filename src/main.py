from Controller import INTERACTABLES
from UI.PedalboardUI import PedalboardUI


root = INTERACTABLES.root
root.geometry("1024x600")
root.attributes("-fullscreen", True)
root.configure(cursor="none")
board = PedalboardUI(root)
board.pack(fill="both", expand=True)
root.mainloop()
