from sounddevice import query_devices, default, Stream, PortAudioError
from Audio.Effects import Effects


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
        self._input_index = default.device[0]
        self._output_index = default.device[1]
        self._stream: Stream | None = None
        self._effects = Effects()
        self.refresh_devices()
        self._start_stream()

    def __enter__(self):
        """
        accesses the audio stream within a context manager
        """

        self._stream.stop()
        return self._effects

    def __exit__(self, *args):
        """
        exists the context manager
        """

        self._stream.start()

    def modify_effects(self):
        """
        function to call when entering the context manager to modify the audio effects
        while ensuring the audio stream is paused:

        with self.modify_effects() as effects:
            ...
        """

        return self

    def refresh_devices(self):
        """
        gets a list of all available audio devices

        :return: a list of all available audio devices
        """

        # resets devices
        self.input_devices = []
        self.output_devices = []
        for device in query_devices():
            print(device)
            name = f"{device['index']} {device['name']}"

            # adds input devices
            if device["max_input_channels"] > 0:
                self.input_devices.append(name)

            # adds output devices
            if device["max_output_channels"] > 0:
                self.output_devices.append(name)

    def set_input_device(self, name):
        """
        selects an input device to use within the audio stream

        :param name: the name of the input device found in self.input_devices
            in the format {device['index']} {device['name']}

        :return: true or false to determine if the stream successfully started with
            the new input device
        """

        self.destroy()
        self._input_index = int(name.split(" ")[0])
        return self._start_stream()

    def set_output_device(self, name):
        """
        selects an output device to use within the audio stream

        :param name: the name of the output device found in self.output_devices
            in the format {device['index']} {device['name']}

        :return: true or false to determine if the stream successfully started with
            the new output device
        """

        self.destroy()
        self._output_index = int(name.split(" ")[0])
        return self._start_stream()

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

        outdata[:] = indata

    def _start_stream(self):
        """
        creates a new audio stream and starts it

        :return: true or false to determine if the stream successfully started
        """

        # attempts to start the new audio stream
        try:
            self._stream = Stream(
                device=(self._input_index, self._output_index),
                callback=lambda indata, outdata, frames, time, status: self._stream_callback(indata, outdata),
                samplerate=44100,
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
