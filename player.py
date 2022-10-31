import pygame
from spritesheet import Spritesheet
from pygame import mixer

# chordList: [[C,E,D], [D,F,A], [E,G,B], [F,A,C], [G,B,D], [A,C,E], [B,D,F]]
# pitch/note encoding: A=0, B=1, C=2, D=3, E=4, F=5, G=6
# chord progression we'll use:
# C major: C – E – G
# D minor: D – F – A
# E minor: E – G – B
# F major: F – A – C
# G major: G – B – D
# A minor: A – C – E
# B diminished: B – D – F

#we'll use one scale, C Major for now, but eventually this will be in its own class w a switch statement based on a button/slider input.
chordList = [[2, 4, 3], [3, 5, 0], [4, 6, 1], [5, 0, 2], [6, 1, 3], [0, 2, 4], [1, 3, 5]]

#chordList = {"a":[2, 4, 3], "b":[3, 5, 0], "c":[4, 6, 1], [5, 0, 2], [6, 1, 3], [0, 2, 4], [1, 3, 5]}

pitchList = [0, 1, 2, 3, 4, 5, 6]
class Player:
    def __init__(self):
        self.note_frames = self.load_frames()
        self.rect = self.note_frames[0].get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        # all the same width/height, so can grab any image
        self.width = self.note_frames[0].get_width()
        self.height = self.note_frames[0].get_height()
        self.volume = 0
        self.pitch = 0
        self.chord = "A"
        self.wav = None
        #flag for one blob selected
        self.IS_SELECTED = False
        #flag for all blobs selected
        self.ALL_SELECTED = True
        self.current_image = self.note_frames[0]

        #will use state to create animations later
        self.state = 'idle'

    def set_current_image(self, frame):
        self.current_image = self.note_frames[frame]

    def set_location(self, frame):
        self.x = frame * 200 + 50
        self.y = 100

    def set_wav(self):
        if self.pitch == 0:
            self.wav = pygame.mixer.Sound('A3.wav')
        elif self.pitch == 1:
            self.wav = pygame.mixer.Sound('B3.wav')
        elif self.pitch == 2:
            self.wav = pygame.mixer.Sound('C3.wav')
        elif self.pitch == 3:
            self.wav = pygame.mixer.Sound('D3.wav')
        elif self.pitch == 4:
            self.wav = pygame.mixer.Sound('E3.wav')
        elif self.pitch == 5:
            self.wav = pygame.mixer.Sound('F3.wav')
        elif self.pitch == 6:
            self.wav = pygame.mixer.Sound('G3.wav')
        else:
            self.wav = None

    def get_wav(self):
        return self.wav
    def get_volume(self):
        return self.volume

    #determines if one or all blobs are selected
    def set_selected_blob(self, mouseX, mouseY):
        #one blob selected
        if (mouseX > self.x) & (mouseX < self.x + self.width) & (mouseY > self.y) & (mouseY < self.y + self.height):
            self.IS_SELECTED = True
            self.ALL_SELECTED = False
        # all selected, picked random x value it has to be greater then, will be button later
        elif mouseX > 700:
            self.ALL_SELECTED = True
            self.IS_SELECTED = False
        else:
            self.IS_SELECTED = False
            self.ALL_SELECTED = False
            return None

    def set_character_iage(self, x, y, i):
        #if all blobs selected
        if self.ALL_SELECTED:
            #update chord based on x position
            if x < 100:
                self.pitch = chordList[0][i]
                self.chord = "A"
            elif (x > 100) & (x < 200):
                self.pitch = chordList[1][i]
                self.chord = "B"
            elif (x > 200) & (x < 300):
                self.pitch = chordList[2][i]
                self.chord = "C"
            elif (x > 300) & (x < 400):
                self.pitch = chordList[3][i]
                self.chord = "D"
            elif (x > 400) & (x < 500):
                self.pitch = chordList[4][i]
                self.chord = "E"
            elif (x > 500) & (x < 600):
                self.pitch = chordList[5][i]
                self.chord = "F"
            elif x > 600:
                self.pitch = chordList[6][i]
                self.chord = "G"

            # volume update
            if y > 350:
                self.volume = 0
            elif (y < 350) & (y > 200):
                self.volume = 1
            elif y < 200:
                self.volume = 2

            # image update
            self.set_current_image(3 * self.pitch + self.volume)

        #if one char is selected
        elif self.IS_SELECTED:
            # pitch update
            if x < 100:
                self.pitch = pitchList[0]
            elif (x > 100) & (x < 200):
                self.pitch = pitchList[1]
            elif (x > 200) & (x < 300):
                self.pitch = pitchList[2]
            elif (x > 300) & (x < 400):
                self.pitch = pitchList[3]
            elif (x > 400) & (x < 500):
                self.pitch = pitchList[4]
            elif (x > 500) & (x < 600):
                self.pitch = pitchList[5]
            elif x > 600:
                self.pitch = pitchList[6]

            # volume update
            if y > 350:
                self.volume = 0
            elif (y < 350) & (y > 200):
                self.volume = 1
            elif y < 200:
                self.volume = 2

            # image update
            frame = 3 * self.pitch + self.volume
            self.set_current_image(frame)

        #rest of blobs need vol 0 and "closed mouth" image aka their first image, so no vol input
        else:
            self.set_current_image(3 * self.pitch)
            self.volume = 0

    def draw(self, display):
        display.blit(self.current_image, (self.x, self.y))

    def load_frames(self):
        my_spritesheet = Spritesheet('choir.png')

        self.note_frames = [my_spritesheet.parse_sprite("A0.png"),
                            my_spritesheet.parse_sprite("A1.png"),
                            my_spritesheet.parse_sprite("A2.png"),
                            my_spritesheet.parse_sprite("B0.png"),
                            my_spritesheet.parse_sprite("B1.png"),
                            my_spritesheet.parse_sprite("B2.png"),
                            my_spritesheet.parse_sprite("C0.png"),
                            my_spritesheet.parse_sprite("C1.png"),
                            my_spritesheet.parse_sprite("C2.png"),
                            my_spritesheet.parse_sprite("D0.png"),
                            my_spritesheet.parse_sprite("D1.png"),
                            my_spritesheet.parse_sprite("D2.png"),
                            my_spritesheet.parse_sprite("E0.png"),
                            my_spritesheet.parse_sprite("E1.png"),
                            my_spritesheet.parse_sprite("E2.png"),
                            my_spritesheet.parse_sprite("F0.png"),
                            my_spritesheet.parse_sprite("F1.png"),
                            my_spritesheet.parse_sprite("F2.png"),
                            my_spritesheet.parse_sprite("G0.png"),
                            my_spritesheet.parse_sprite("G1.png"),
                            my_spritesheet.parse_sprite("G2.png")]

        return self.note_frames
