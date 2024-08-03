import pygame
import time

pygame.init()
print('init =', pygame.mixer.get_init())

onekick = pygame.mixer.Sound("onekick.wav")
synthbass = pygame.mixer.Sound("synthbass.wav")

s = onekick + synthbass
s.play()
time.sleep(2)

c2 = synthbass.play()
print (f"synthbass on {c2.id}")
c1 = onekick.play()
print (f"onekick on {c1.id}")

time.sleep(2)
