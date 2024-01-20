import itertools
import math
import random
import pyaudio
import numpy as np
from enum import Enum, auto

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1


def note_pitch(n):
    """Return the frequency of the n-th note (piano numbering) in Hz"""
    return 440 * (2**(1/12)) ** (n - 49)

def get_note(n: str):
    """
    Return the frequency of the note in Hz
    
    This function accepts notes in the form of a string, e.g. 'A4', 'C#5' or 'Eb3'
    """
    if len(n) == 1:
        n += '4'
   
    mod = None
    if len(n) == 2:
        note, octave = n[0], int(n[1])
    elif len(n) == 3:
        note, octave, mod = n[0], int(n[1]), n[2]

    note_n = {
        'A': 0,
        'B': 2,
        'C': -9,
        'D': -7,
        'E': -5,
        'F': -4,
        'G': -2,
    }[note.upper()]
    
    if mod:
        if mod == '#':
            note_n += 1
        elif mod == 'b':
            note_n -= 1
        else:
            raise ValueError(f"Invalid note modifier: {mod}")
    

    note_n = note_n + octave * 12 + 1
    return note_pitch(note_n)


test_notes = ['A4', 'A4#', 'B4', 'C5', 'C5#', 'D5', 'D5#', 'E5', 'F5', 'F5#', 'G5', 'G5#']
    
blues_scale_1 = [
    'C5',
    'D5#',
    'F5',
    'F5#',
    'G5',
    'A5#',
    'C6',
]
blues_scale_2 = [
    'C6',
    'D6#',
    'F6',
    'F6#',
    'G6',
    'A6#',
    'C7',
]
blues_scale_3 = [
    'C7',
    'D7#',
    'F7',
    'F7#',
    'G7',
    'A7#',
    'C8',
]


def pure_tone(i, freq, amplitude, sample_rate=SAMPLE_RATE):
    return math.sin(i * 2 * math.pi / sample_rate * freq) * amplitude


def simple_render(notes: list[str], length=0.2):
    """
    Render a set of notes into a sequence of samples.
    length: length of the note in seconds
    """
    samples = []
    end = int(SAMPLE_RATE * length)
    for i in range(end):
        amplitude = 10_000

        tones = []
        for note in notes:
            tones.append(pure_tone(i, get_note(note), amplitude)) 
    
        v = 0 
        for tone in tones:
            v += tone
        v /= len(tones)

        samples.append(v * ((end - i)/end))

    return samples

stream = pyaudio.PyAudio().open(
    rate=SAMPLE_RATE,
    channels=1,
    format=pyaudio.paInt16,
    output=True,
    frames_per_buffer=BUFFER_SIZE,
)

def play(samples):
    stream.write(np.int16(samples).tobytes())


def simple_blues():
    while True:
        scale = random.choice([blues_scale_1, blues_scale_2, blues_scale_3])
        note_sel = random.randint(0, len(scale) - 1)
        for i in range(4):
            note_sel += random.choice([-1, 0, 1])
            note = scale[note_sel % len(scale)]
            play(simple_render([note, 'C3', 'C4'], length=0.2))
        for i in range(4):
            note_sel += random.choice([-1, 0, 1])
            note = scale[note_sel % len(scale)]
            play(simple_render([note, 'A3#', 'A4#'], length=0.2))
        for i in range(4):
            note_sel += random.choice([-1, 0, 1])
            note = scale[note_sel % len(scale)]
            play(simple_render([note, 'G3#', 'G4#'], length=0.2))
        for i in range(4):
            note_sel += random.choice([-1, 0, 1])
            note = scale[note_sel % len(scale)]
            play(simple_render([note, 'G3', 'G4'], length=0.2))


if __name__ == '__main__':
    simple_blues()