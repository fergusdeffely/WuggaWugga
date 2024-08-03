import time
import pygame
from gensound import WAV, test_wav
from gensound import Sine, Square, Sawtooth, Triangle, WhiteNoise
from gensound.effects import Vibrato, Stretch, Downsample
from gensound.transforms import ADSR, Reverse
from gensound.filters import SimpleLPF, SimpleHPF, SimpleHighShelf, SimpleLowShelf, SimpleBandStop
from gensound.io import IO
from gensound.curve import SineCurve
import pkg_resources

def synth(note, duration, detune=5):
    synth =  Square(note, duration=duration) + Square(f"{note}-{detune*2}", duration=duration) + Square(f"{note}-{detune}", duration=duration) 
    synth += Square(f"{note}+{detune}", duration=duration) + Square(f"{note}+{detune*2}", duration=duration)  
    return synth 

def synth2(note, duration, detune=5):
    synth = Sawtooth(note, duration=duration) + Sawtooth(f"{note}-{detune}", duration=duration) + Sawtooth(f"{note}+{detune}", duration=duration) 
    synth += Square(note, duration=duration) + Square(f"{note}-{detune+5}", duration=duration) + Square(f"{note}+{detune+5}", duration=duration)
    return synth

def synth3(frequency, duration):
    return 0.5*Sine(frequency, duration) + 0.3*Square(frequency*2, duration) + 0.02*WhiteNoise(duration)

IO.set_io("play", "pygame")

#s = Sine('D5 C# A F# B G# E# C# F#', duration=0.5e3)

syn1 = False 
syn2 = False
syn3 = False
syn4 = False
rev1 = False 

synthbass = WAV("synthbass.wav")
synthbass.play()
onekick = WAV("onekick.wav")
onekick.play()
time.sleep(2)

s = synthbass + onekick
s.play()
time.sleep(2)

if syn1:
    s = synth("D3", 0.5e3, 3) | synth("C#3", 0.5e3, 3) | synth("A2", 0.5e3, 3) 
    #s *= Downsample(factor=8) * Stretch(rate=0.5)
    #s *= SimpleBandStop(200, 8500)
    s.play()
    time.sleep(3)

if syn2:
    adsr = ADSR(attack=0.002e3, decay=0.03e3, sustain=0.8, release=0.2e3)
    s2 = synth("D3", 0.5e3)*adsr | synth("C#3", 0.5e3)*adsr | synth("A2", 0.5e3)*adsr
    s2.play()
    time.sleep(2)

if syn3:
    s = synth2("D3", 0.5e3, 3) | synth2("C#3", 0.5e3, 3) | synth2("A2", 0.5e3, 3) 
    s.play()
    time.sleep(2)

if syn4:
    s = synth3(288.3, 0.5e3) | synth3(272.1, 0.5e3) | synth3(108.0, 0.5e3) 
    s.play()
    time.sleep(2)

if rev1:
    r = s * Reverse()
    r.play()
    time.sleep(2)

#fm = SineCurve(frequency=10, depth=1.01, baseline=330, duration=10e3)
#Sine(fm, 10e3).play()
#time.sleep(5)

#pygame.mixer.pause()
#
#time.sleep(4)
#
#pygame.mixer.unpause()
#
#time.sleep(5)

