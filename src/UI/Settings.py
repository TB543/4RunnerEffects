from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, StringVar


class Settings(CTkFrame):
    """
    a class for the settings menu of the program
    """

    def __init__(self, parent, audio, **kwargs):
        """
        creates the settings menu

        :param parent: the parent widget
        :param audio: the audio stream
        :param kwargs: any other keyword arguments
        """

        # initializes class and configures grid
        super().__init__(parent, **kwargs)
        self.audio = audio
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # title, close button, and error notification
        CTkLabel(self, text="Settings", font=("Comic Sans MS", 30, "bold")).grid(row=0, column=0, columnspan=3)
        CTkButton(self, text="X", font=("Comic Sans MS", 25, "bold"), border_width=3, border_color="black", width=50, height=50, command=self.place_forget).grid(row=0, column=1, sticky="ne", padx=20, pady=20)
        self.failed_label = CTkLabel(self, text="Selected Input and Output Devices are not Compatible", font=("Comic Sans MS", 15), text_color="red")
        self.validate_stream()

        # audio input selection
        CTkLabel(self, text="Audio In:", font=("Comic Sans MS", 20)).grid(row=1, column=0, sticky="s")
        self.inputs = CTkOptionMenu(self, variable=StringVar(self, self.audio.input_device), font=("Comic Sans MS", 15), command=self.set_audio_in)
        self.inputs.bind("<Enter>", lambda e: self.update_audio_devices())
        self.inputs.grid(row=2, column=0, sticky="n")

        # audio output selection
        CTkLabel(self, text="Audio Out:", font=("Comic Sans MS", 20)).grid(row=1, column=1, sticky="s")
        self.outputs = CTkOptionMenu(self, variable=StringVar(self, self.audio.output_device), font=("Comic Sans MS", 15), command=self.set_audio_out)
        self.outputs.bind("<Enter>", lambda e: self.update_audio_devices())
        self.outputs.grid(row=2, column=1, sticky="n")

    def update_audio_devices(self):
        """
        updates the lists of input and output devices
        """

        self.audio.refresh_devices()
        self.inputs.configure(values=self.audio.input_devices)
        self.outputs.configure(values=self.audio.output_devices)

    def set_audio_in(self, value):
        """
        sets the audio input device
        """

        self.audio.input_device = value
        self.validate_stream()

    def set_audio_out(self, value):
        """
        sets the audio output device
        """

        self.audio.output_device = value
        self.validate_stream()

    def validate_stream(self):
        """
        checks if the audio devices are compatible
        """

        if self.audio.compatible_stream:
            self.failed_label.grid_forget()
        else:
            self.failed_label.grid(row=2, column=0, columnspan=2)
