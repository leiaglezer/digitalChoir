import time

import pygame
from pygame import mixer

# setup music player
mixer.init()
pygame.mixer.set_num_channels(50)

wavList = [pygame.mixer.Sound('C3.wav'), pygame.mixer.Sound('timbre1D.wav')]

# for i, x in enumerate(wavList):
#     pygame.mixer.Channel(i + 1).play(x) #full volume
#     time.sleep(5)
#     pygame.mixer.Channel(i + 1).set_volume(0) #0 volume
#     time.sleep(5)
#     pygame.mixer.Channel(i + 1).set_volume(1) #full volume
#     time.sleep(5)


pygame.mixer.Channel(1).play(pygame.mixer.Sound('C3.wav')) #full volume
pygame.mixer.Channel(2).play(pygame.mixer.Sound('timbre1D.wav')) #full volume
time.sleep(5)
pygame.mixer.Channel(1).set_volume(.5)
pygame.mixer.Channel(2).set_volume(.5)
time.sleep(5)
pygame.mixer.Channel(1).set_volume(1)
pygame.mixer.Channel(2).set_volume(1)
time.sleep(5)
