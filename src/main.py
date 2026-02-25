from Audio.AudioIO import AudioIO

audio = AudioIO()
audio.set_input_device("45 Input (iRig USB)")
audio.set_output_device("34 Headphones (HD Audio Headphone)")
input("Press Enter to continue...")
audio.destroy()
input("Press Enter to continue...")
audio.set_output_device("34 Headphones (HD Audio Headphone)")
input("Press Enter to continue...")

with audio.modify_effects() as e:
    print(type(e))
    input()
input("Press Enter to continue...")
