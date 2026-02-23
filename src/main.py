from sounddevice import Stream, sleep
from pedalboard import Pedalboard, Reverb, Distortion, Chorus
from AppData import *

board = Pedalboard([
    Distortion(),
    Reverb(room_size=0.3),
    Chorus()
])

def callback(indata, outdata, frames, time, status):
    outdata[:] = board(indata, SAMPLE_RATE)

with Stream(device=(AUDIO_IN, AUDIO_OUT),
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=CHANNELS,
            callback=callback):
    sleep(60000)