from music21 import *
import time
import sounddevice as sd
from scipy.io import wavfile as wav
import numpy as np

# Đọc file nhạc sheet và chuyển đổi thành đối tượng Score của thư viện music21
score = converter.parse('myfile.mxl')

# Chọn một nhạc cụ (instrument) để chơi file nhạc và tạo một đối tượng midi để lưu trữ dữ liệu âm thanh của file nhạc sheet
piano = instrument.Piano()
midi = midi.realtime.StreamPlayer(score)
midi.channel = midi.channel

# Chơi file nhạc bằng thư viện music21 và lưu lại thành file âm thanh
fs = 44100
blocksize = 2048

with sd.OutputStream(channels=2, blocksize=blocksize, samplerate=fs) as out_stream:
    midi_out = midi.realtime.StreamPlayer(score)
    midi_out.channel = midi.channel
    midi_out.source.client = out_stream.play

    midi_out.play()
    while midi_out.isPlaying:
        time.sleep(0.1)
    sd.wait()

audio = np.array(midi_out.data * 32767, dtype=np.int16)
wav.write('file_piano_audio.wav', fs, audio)
