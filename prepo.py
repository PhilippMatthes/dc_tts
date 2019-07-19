# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
By kyubyong park. kbpark.linguist@gmail.com.
https://www.github.com/kyubyong/dc_tts
'''

from __future__ import print_function

from utils import load_spectrograms
import os
from data_load import load_data
import numpy as np
import tqdm

import wave
import time
import os

import pygame

from os import listdir
from os.path import isfile, join

existing_samples = [f for f in listdir("LJSpeech-1.1/wavs") if isfile(join("LJSpeech-1.1/wavs", f))]
existing_identifiers = [sample.replace(".wav", "") for sample in existing_samples]
print("{} existing samples found. Preloading transcript...".format(len(existing_samples)))

with open("LJSpeech-1.1/metadata_all.csv", "r") as all_metadata_file:
    with open("LJSpeech-1.1/transcript.csv", "w") as transcript_file:
        for row in all_metadata_file.readlines():
            splitted_row = row.split("|")
            identifier = splitted_row[0]
            if identifier in existing_identifiers:
                transcript_file.write(row)

print("Done with preloading transcript.")

# Load data
fpaths, _, _ = load_data() # list

for fpath in tqdm.tqdm(fpaths):
    fname, mel, mag = load_spectrograms(fpath)
    if not os.path.exists("mels"): os.mkdir("mels")
    if not os.path.exists("mags"): os.mkdir("mags")

    np.save("mels/{}".format(fname.replace("wav", "npy")), mel)
    np.save("mags/{}".format(fname.replace("wav", "npy")), mag)
