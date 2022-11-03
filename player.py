import pygame
from spritesheet import Spritesheet

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

# we'll use one scale, C Major for now, but eventually this will be in its own class w a switch statement based on a button/slider input.
chord_list = [[2, 4, 3], [3, 5, 0], [4, 6, 1], [5, 0, 2], [6, 1, 3], [0, 2, 4], [1, 3, 5]]
pitch_list = [0, 1, 2, 3, 4, 5, 6]

class Player:
    def __init__(self):

        # load frames into array
        self.frame_list = self.load_frames()

        # get x,y of frame bounding box
        self.x = self.frame_list[0].get_rect().x
        self.y = self.frame_list[0].get_rect().y

        # width/height each frame (all the same size, so can grab any image)
        self.width = self.frame_list[0].get_width()
        self.height = self.frame_list[0].get_height()

        # sets initial
        self.volume = 0
        self.pitch = 0
        self.chord = "Cmaj"
        self.wav = None

        # flag for one char selected
        self.IS_SELECTED = False
        # flag for all chars selected
        self.ALL_SELECTED = True

        # animation frame
        self.frame = self.frame_list[0]

        # will use state to create animations later
        self.state = 'idle'

    def set_location(self, frame):
        self.x = frame * 200 + 50
        self.y = 100

    def set_wav(self):
        if self.pitch == 0:
            self.wav = pygame.mixer.Sound('timbre1A.wav')
        elif self.pitch == 1:
            self.wav = pygame.mixer.Sound('timbre1B.wav')
        elif self.pitch == 2:
            self.wav = pygame.mixer.Sound('C3.wav')
        elif self.pitch == 3:
            self.wav = pygame.mixer.Sound('timbre1D.wav')
        elif self.pitch == 4:
            self.wav = pygame.mixer.Sound('timbre1E.wav')
        elif self.pitch == 5:
            self.wav = pygame.mixer.Sound('timbre1F.wav')
        elif self.pitch == 6:
            self.wav = pygame.mixer.Sound('timbre1G.wav')
        else:
            self.wav = None

    def get_wav(self):
        return self.wav

    def get_pitch(self):
        return self.pitch

    def get_chord(self):
        return self.chord

    def get_volume(self):
        return self.volume

    # determines if one or all blobs are selected
    def set_selected_blob(self, mouseX, mouseY):
        # one char selected
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

    def set_pitch(self, x, i):
        # if one char selected
        if self.ALL_SELECTED:
            # update chord based on x position
            if x < 100:
                self.pitch = chord_list[0][i]
                self.chord = "Cmaj"
            elif (x > 100) & (x < 200):
                self.pitch = chord_list[1][i]
                self.chord = "Dmin"
            elif (x > 200) & (x < 300):
                self.pitch = chord_list[2][i]
                self.chord = "Emin"
            elif (x > 300) & (x < 400):
                self.pitch = chord_list[3][i]
                self.chord = "Fmaj"
            elif (x > 400) & (x < 500):
                self.pitch = chord_list[4][i]
                self.chord = "Gmaj"
            elif (x > 500) & (x < 600):
                self.pitch = chord_list[5][i]
                self.chord = "Amin"
            elif x > 600:
                self.pitch = chord_list[6][i]
                self.chord = "Bdim"

        # if one char is selected
        elif self.IS_SELECTED:
            # pitch update
            if x < 100:
                self.pitch = pitch_list[0]
            elif (x > 100) & (x < 200):
                self.pitch = pitch_list[1]
            elif (x > 200) & (x < 300):
                self.pitch = pitch_list[2]
            elif (x > 300) & (x < 400):
                self.pitch = pitch_list[3]
            elif (x > 400) & (x < 500):
                self.pitch = pitch_list[4]
            elif (x > 500) & (x < 600):
                self.pitch = pitch_list[5]
            elif x > 600:
                self.pitch = pitch_list[6]

    def set_volume(self, y):
        if self.ALL_SELECTED or self.IS_SELECTED:
            # volume update
            if y > 350:
                self.volume = 0
            elif (y < 350) & (y > 200):
                self.volume = 1
            elif y < 200:
                self.volume = 2
        else:
            self.volume = 0

    def set_frame(self):
        # keeps closed mouth animation
        if self.volume == 0:
            self.frame = self.frame_list[3 * self.pitch]
        else:
            self.frame = self.frame_list[3 * self.pitch + self.volume]

    def draw(self, display):
        display.blit(self.frame, (self.x, self.y))

    def load_frames(self):
        my_spritesheet = Spritesheet('choir.png')

        self.frame_list = [my_spritesheet.parse_sprite("A0.png"),
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

        return self.frame_list
