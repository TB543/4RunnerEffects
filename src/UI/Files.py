from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkScrollableFrame, StringVar, CTkEntry
from json import load, dump
from UI.Widgets import VirtualKeyboard


class Files(CTkFrame):
    """
    a class for the files menu of the program
    """

    def __init__(self, parent, **kwargs):
        """
        creates the files menu

        :param parent: the parent widget
        :param audio: the audio stream
        """

        # initializes class and configures grid
        super().__init__(parent, **kwargs)
        self.pedalboard = parent
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # title, close button and body
        CTkLabel(self, text="Saved Pedalboards", font=("Comic Sans MS", 30, "bold")).grid(row=0, column=0, columnspan=2)
        CTkButton(self, text="X", font=("Comic Sans MS", 25, "bold"), border_width=3, border_color="black", width=50, height=50, command=self.place_forget).grid(row=0, column=0, sticky="ne", padx=20, pady=20)
        self.body = CTkScrollableFrame(self)
        self.body.columnconfigure(0, weight=1)
        self.body.grid(row=1, column=0, sticky="nsew", padx=(3, 10), pady=3)
        self.keyboard = None
        self.update_saved()

        # creates confirmation popup
        self.popup_command = lambda: None
        self.popup = CTkFrame(self, border_width=2, border_color="black")
        self.popup.rowconfigure(0, weight=1)
        self.popup.columnconfigure(0, weight=1)
        self.popup.columnconfigure(1, weight=1)
        self.message = StringVar(self, "testingtesting123")
        CTkLabel(self.popup, font=("Comic Sans MS", 25, "bold"), textvariable=self.message).grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        CTkButton(self.popup, font=("Comic Sans MS", 20, "bold"), border_width=2, border_color="black", text="confirm", command=lambda: [self.popup_command(), self.popup.place_forget()]).grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        CTkButton(self.popup, font=("Comic Sans MS", 20, "bold"), border_width=2, border_color="black", text="cancel", command=self.popup.place_forget).grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    def show_popup(self, message, command):
        """
        displays a popup message that the user can confirm or cancel

        :param message: the message to display
        :param command: the command to execute if the user hits confirm
        """

        self.popup_command = command
        self.message.set(message)
        self.popup.place(relx=.5, rely=.55, anchor="center", relwidth=.85, relheight=.8)

    def load(self, pedalboard: list[dict] = ()):
        """
        loads an existing pedalboard file

        :param pedalboard: the pedalboard config json. will be a list of pedals in the following format:
            {
                "name": "Gain",
                **kwargs
            }
            where the kwargs are the settings for the pedal. for example gain might have "gain_db": 15
        """

        # removes old pedals
        for pedal in self.pedalboard.pedals.copy():
            self.pedalboard.delete_pedal(pedal)

        # loads new pedalboard
        for pedal in pedalboard:
            self.pedalboard.add_pedal(pedal.pop("name"), **pedal)
        self.place_forget()

    def save(self, name, show_popup=False):
        """
        saves the current pedalboard configuration in the json format listed above in the load method

        :param name: the name of the pedalboard to save
        :param show_popup: determines if a popup should be shown if the given name will overwrite a save
        """

        # reads current save file to memory
        self.keyboard.place_forget()
        try:
            with open("AppData/pedalboards.json", "r") as f:
                pedalboards = load(f)
        except FileNotFoundError:
            pedalboards = {}

        # displays popup message if save already exists with the given name
        if show_popup and name in pedalboards:
            self.show_popup(f"Saved Pedalboard With Name:\n\"{name}\"\nAlready Exists. Overwrite Existing Save?", lambda: self.save(name))
            return

        # gets the config json for the current pedalboard
        pedalboard = []
        for pedal in self.pedalboard.pedals.copy():
            config = {"name": pedal.__class__.__qualname__[:-5]}
            config.update({name: getattr(pedal.effect, name) for name in dir(pedal.effect) if name in pedal.__class__.MIN_MAX_VALUES})
            pedalboard.append(config)

        # writes it to the save file
        pedalboards[name] = pedalboard
        with open("AppData/pedalboards.json", "w") as f:
            dump(pedalboards, f, indent=4)
        self.update_saved()

    def delete(self, name):
        """
        deletes a saved pedalboard
        """

        with open("AppData/pedalboards.json", "r") as f:
            pedalboards = load(f)
        pedalboards.pop(name)
        with open("AppData/pedalboards.json", "w") as f:
            dump(pedalboards, f, indent=4)
        self.update_saved()

    def update_saved(self):
        """
        updates the list of saved pedalboards
        """

        # removes old saves
        for widget in self.body.winfo_children():
            widget.destroy()

        # creates the load and save options at the top
        name = StringVar(self.body)
        CTkButton(self.body, text="Load Blank PedalBoard", font=("Comic Sans MS", 20), border_width=2, height=75, border_color="black", command=self.load).grid(row=0, column=0, columnspan=4, sticky="ew", padx=5)
        entry = CTkEntry(self.body, placeholder_text="Enter Pedalboard Name...", textvariable=name, font=("Comic Sans MS", 20), height=75)
        entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=(5, 0))
        if self.keyboard is not None: self.keyboard.destroy()
        self.keyboard = VirtualKeyboard(self.winfo_toplevel(), entry, lambda n=name: self.save(n.get()))
        CTkButton(self.body, text="💾", font=("Comic Sans MS", 20), border_width=2, width=75, height=75, border_color="black", command=lambda n=name: self.save(n.get(), True)).grid(row=1, column=3, padx=5, pady=(5, 0))

        # reads current save file to memory
        try:
            with open("AppData/pedalboards.json", "r") as f:
                pedalboards = load(f)
        except FileNotFoundError:
            pedalboards = {}

        # draws saved pedals to screen
        for i, (name, data) in enumerate(pedalboards.items()):
            CTkLabel(self.body, text=name, font=("Comic Sans MS", 20)).grid(row=i + 2, column=0, sticky="w", padx=(25, 0), pady=(5, 0))
            CTkButton(self.body, text="📥", font=("Comic Sans MS", 20), border_width=2, width=75, height=75, border_color="black", command=lambda d=data: self.load(d)).grid(row=i + 2, column=1, padx=5, pady=(5, 0))
            CTkButton(self.body, text="💾", font=("Comic Sans MS", 20), border_width=2, width=75, height=75, border_color="black", command=lambda n=name: self.show_popup(f"Overwrite\n\"{n}\"\nSave Data?", lambda: self.save(n))).grid(row=i + 2, column=2, padx=5, pady=(5, 0))
            CTkButton(self.body, text="🗑️", font=("Comic Sans MS", 20), border_width=2, width=75, height=75, border_color="black", command=lambda n=name: self.show_popup(f"Delete\n\"{n}\"\nSave Data?", lambda: self.delete(n))).grid(row=i + 2, column=3, padx=5, pady=(5, 0))

    def place_forget(self):
        """
        overrides the place forget method to also hide the keyboard
        """

        super().place_forget()
        self.focus_set()
        self.keyboard.place_forget()
