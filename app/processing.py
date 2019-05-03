from django.db.models import Max
from django.shortcuts import get_object_or_404
from pathlib import Path
import os
from PIL import Image

from .models import ImageUpload

from pydub import AudioSegment
from pydub.playback import play

import pyaudio
import numpy as np


def get_image(imageid):
    image_object = get_object_or_404(ImageUpload, pk=imageid)
    i = Image.open(os.path.abspath(os.path.join('media', image_object.image.name)))
    return i


class Processing:

    def __init__(self, imageid):
        self.imageToBeProcess = get_image(imageid)
        self.i = 0
        # Values obtained
        self.redPixel = []
        self.greenPixel = []
        self.bluePixel = []
        self.soundValue = []
        self.audioSegment = []

    def getRGB(self):
        image_file = self.imageToBeProcess
        image = image_file.load()
        [xs, ys] = image_file.size

        for x in range(0, xs):
            for y in range(0, ys):

                [r, g, b] = image[x, y]
                self.redPixel.append(r)
                self.greenPixel.append(g)
                self.bluePixel.append(b)

                if y == ys - 1:
                    avg_red = sum(self.redPixel) / ys
                    avg_green = sum(self.greenPixel) / ys
                    avg_blue = sum(self.bluePixel) / ys
                    # print(self.redPixel)
                    # print(self.greenPixel)
                    # print(self.bluePixel)
                    self.redPixel.clear()
                    self.greenPixel.clear()
                    self.bluePixel.clear()

                    sound_value = (avg_red + avg_green + avg_blue) / 3
                    self.soundValue.append(sound_value)

        print("getRGB is completed successfully!")
        print(len(self.soundValue))

    def getSound(self, sound_value):
        # p = pyaudio.PyAudio()

        # volume = 0.8  # range [0.0, 1.0]
        fs = 44100  # sampling rate, Hz, must be integer
        duration = 0.2  # in seconds, may be float
        f = (sound_value*440)/255  # sine frequency, Hz, may be float

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

        audiosegment = AudioSegment(
                samples.tobytes(),
                frame_rate=44100,
                sample_width=samples.dtype.itemsize,
                channels=1
            )

        self.audioSegment.append(audiosegment)


        # for paFloat32 sample values must be in range [-1.0, 1.0]
        # stream = p.open(format=pyaudio.paFloat32,
        #                 channels=1,
        #                 rate=fs,
        #                 output=True)

        # play. May repeat with different volume values (if done interactively)
        # stream.write(volume * samples)
        #
        # stream.stop_stream()
        # stream.close()
        #
        # p.terminate()

        # # Append each tone onto other with crossfade
        # multitone = tone1.append(tone2, crossfade=2500).append(tone3, crossfade=2500)
        #
        # # Play final tone
        # play(multitone)

    def makefile(self):
        multitone = 0
        for s in self.soundValue:
            Processing.getSound(self, s)
            # vector de sunet si vector de audio segmente

        for asegm in range(0, len(self.audioSegment)):
            multitone += self.audioSegment[asegm]

        multitone.export('media/sound.wav', format="wav")

        print("Media file created!")