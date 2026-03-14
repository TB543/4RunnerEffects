# 4Runner Effects

4Runner Effects is a **digital guitar pedalboard written in Python** that allows real‑time audio processing through a chain of effects.  
It provides a visual interface for adding, configuring, and ordering guitar pedals similar to a physical pedalboard.

The project uses the **[Pedalboard](https://github.com/spotify/pedalboard)** audio effects library for high‑quality signal processing.

---

## Features

- 🎸 Real‑time guitar signal processing
- 🧩 Modular pedalboard effect chain
- 🎛 Adjustable pedal parameters
- 🖥 Simple graphical interface
- ⚡ Designed for low‑latency audio playback
- 🐍 Built entirely in Python

---

## Effects

4Runner Effects supports multiple audio effects including:

- Gain / Overdrive
- Chorus
- Phaser
- Reverb
- Delay
- Compressor
- Limiter
- Noise Gate
- Pitch Shift
- Bitcrush
- Resample
- High Shelf Filter
- Low Shelf Filter
- Peak Filter
- High Pass Filter
- Low Pass Filter
- Ladder Filter
- MP3 Compressor
- GSM Full Rate Compressor

Each effect exposes parameters relevant to its behavior, allowing users to fine‑tune their sound.

---

## How It Works

1. Audio input is captured from an instrument input device (configured in settings).  
2. The signal is passed through a **pedal chain**.  
3. Each pedal processes the audio using the Pedalboard library.  
4. The processed audio is streamed to the output device (configured in settings).

The pedal chain can be dynamically modified while the application is running.

---

## Installation

Clone the repository:
```
git clone https://github.com/TB543/4RunnerEffects.git  
cd 4RunnerEffects
```
Install dependencies:
```
pip install -r requirements.txt
```
---

## Running the Application

Run the main program:
```
python src/main.py
```
Make sure your system audio input and output devices are properly configured.


---

## Pedalboard Citation

Pedalboard is developed by **Spotify AB** and licensed under the **GNU General Public License v3 (GPLv3)**.

Additional license notes:

- Core audio processing code uses **JUCE 6** (dual-licensed, GPLv3 for this project)  
- VST3 SDK bundled with JUCE (GPLv3)  
- PitchShift and time_stretch use **Rubber Band Library** (GPLv2 or newer)  
- MP3Compressor uses **libmp3lame** (LGPLv2 upgraded to GPLv3)  
- GSMFullRateCompressor uses **libgsm** (ISC license, GPLv3 compatible)  
- WAV decoding uses **dr_wav** (public domain)  
- VST is a registered trademark of Steinberg Media Technologies GmbH  

---

## Project Goals

- Provide a customizable **digital guitar pedalboard**  
- Enable **real‑time effects processing in Python**  
- Create an extensible framework for building new pedals  
- Run efficiently on small devices such as Raspberry Pi  

---

## Future Improvements

- Preset saving and loading
- Audio recording
- Make UI more pretty

---
