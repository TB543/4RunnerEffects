from sounddevice import query_devices, default, Stream, PortAudioError
from pedalboard import Pedalboard


class AudioIO:
    """
    a class for managing audio input/output devices and passing the audio stream

    TODO make input and output devices properties and only give devices that are compatible
    """

    def __init__(self):
        """
        initializes the audio stream to use the default input and output devices
        """

        self.input_devices = []
        self.output_devices = []
        self._input_device = query_devices(default.device[0])
        self._output_device = query_devices(default.device[1])
        self._stream: Stream | None = None
        self._effects = Pedalboard()
        self._start_stream()

    def __enter__(self):
        """
        accesses the effects within a context manager where audio stream is paused
        """

        self._stream.stop()
        return self._effects

    def __exit__(self, *args):
        """
        exits the context manager and resumes the audio stream
        """

        self._stream.start()

    @property
    def input_device(self):
        """
        returns the currently selected input device
        """

        return f"{self._input_device['index']} {self._input_device['name']}"

    @property
    def output_device(self):
        """
        returns the currently selected output device
        """

        return f"{self._output_device['index']} {self._output_device['name']}"

    @input_device.setter
    def input_device(self, name):
        """
        selects an input device to use within the audio stream

        :param name: the name of the input device found in self.input_devices
            in the format {device['index']} {device['name']}
        """

        self.destroy()
        self._input_device = query_devices(int(name.split(" ")[0]))
        self._start_stream()

    @output_device.setter
    def output_device(self, name):
        """
        selects an output device to use within the audio stream

        :param name: the name of the output device found in self.output_devices
            in the format {device['index']} {device['name']}
        """

        self.destroy()
        self._output_device = query_devices(int(name.split(" ")[0]))
        self._start_stream()

    def modify_effects(self):
        """
        function to call when entering the context manager to modify the audio effects
        while ensuring the audio stream is paused:

        with self.modify_effects() as effects:
            ...

        note: accessing effects outside the context manager will produce unexpected behavior
        """

        return self

    def refresh_devices(self):
        """
        updates the lists of input and output devices
        """

        # resets devices
        self.input_devices = []
        self.output_devices = []
        for device in query_devices():
            name = f"{device['index']} {device['name']}"

            # adds input devices
            if device["max_input_channels"] > 0:
                self.input_devices.append(name)

            # adds output devices
            if device["max_output_channels"] > 0:
                self.output_devices.append(name)

    def destroy(self):
        """
        stops the audio stream and frees it
        note: some other class functionality will re-open the stream
        """

        self._stream.stop()
        self._stream.close()

    def _stream_callback(self, indata, outdata):
        """
        the callback function that is called each sample of the audio stream and
        applies effects to the audio stream

        see Stream docs for more details
        """

        outdata[:] = self._effects(indata, self._input_device["default_samplerate"])

    def _start_stream(self):
        """
        creates a new audio stream and starts it

        :return: true or false to determine if the stream successfully started
        """

        # attempts to start the new audio stream
        try:
            self._stream = Stream(
                device=(self._input_device["index"], self._output_device["index"]),
                callback=lambda indata, outdata, *args: self._stream_callback(indata, outdata),
                samplerate=self._input_device["default_samplerate"],
                blocksize=128,
                channels=1
            )
            self._stream.start()
            return True

        # returns false if I/O devices are incompatible
        except PortAudioError:
            return False

        except ValueError:
            return "test"
