import wave
import time
import os

import pygame

from os import listdir
from os.path import isfile, join

existing_samples = [f for f in listdir("LJSpeech-1.1/wavs") if isfile(join("LJSpeech-1.1/wavs", f))]
existing_identifiers = [sample.replace(".wav", "") for sample in existing_samples]
print("{} existing samples found.".format(len(existing_samples)))


with open("LJSpeech-1.1/metadata.csv", "r") as f:
    for row in f.readlines():
        splitted_row = row.split("|")
        sequence = splitted_row[2]
        identifier = splitted_row[0]
        for i, existing_identifier in enumerate(existing_identifiers):
            if identifier == existing_identifier:
                os.system('clear')
                print(sequence)
                print(identifier)
                path = os.path.join("LJSpeech-1.1/wavs", existing_samples[i])
                pygame.mixer.init()
                pygame.mixer.music.load(path)
                pygame.mixer.music.play()
                if input("Keep this sample? n to delete") == "n":
                    os.remove(path)
