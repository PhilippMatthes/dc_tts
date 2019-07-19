import pyaudio
import wave
import time
import os

from os import listdir
from os.path import isfile, join

existing_samples = [f for f in listdir("LJSpeech-1.1/wavs") if isfile(join("LJSpeech-1.1/wavs", f))]
existing_identifiers = [sample.replace(".wav", "") for sample in existing_samples]
print("{} existing samples found.".format(len(existing_samples)))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


def record(sequence, identifier):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    while True:
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except KeyboardInterrupt:
            break

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    try:
        if input("Save this sample? ctrl+c to retry"):
            pass
    except KeyboardInterrupt:
        record(sequence, identifier)

    wf = wave.open("LJSpeech-1.1/wavs/{}.wav".format(identifier), 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    os.system('clear')


with open("LJSpeech-1.1/metadata.csv", "r") as f:
    for row in f.readlines():
        splitted_row = row.split("|")
        sequence = splitted_row[2]
        identifier = splitted_row[0]
        if identifier in existing_identifiers:
            continue

        print(sequence)
        try:
            input("Record? ctrl+c to exit")
        except KeyboardInterrupt:
            break

        record(sequence, identifier)
