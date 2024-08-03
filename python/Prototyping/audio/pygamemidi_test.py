import pygame
import time
import pygame.midi

pygame.midi.init()

output_id = pygame.midi.get_default_output_id()
print (f"midi: default output id: {output_id}")

if output_id is not None:
    info = pygame.midi.get_device_info(output_id)
    print (f"device info: {info}")

# player = pygame.midi.Output(1)
# player.set_instrument(48,1)

major=[0,4,7,12]

def go(note):
    player.note_on(note, 127,1)
    time.sleep(1)
    player.note_off(note,127,1)

def arpeggio(base,ints):
    for n in ints:
        go(base+n)

def chord(base, ints):
    player.note_on(base,127,1)
    player.note_on(base+ints[1],127,1)
    player.note_on(base+ints[2],127,1)
    player.note_on(base+ints[3],127,1)
    time.sleep(1)
    player.note_off(base,127,1)
    player.note_off(base+ints[1],127,1)
    player.note_off(base+ints[2],127,1)
    player.note_off(base+ints[3],127,1)

def end():
       pygame.quit()

# go(60)

# chord (60, major)

# arp(60, major)