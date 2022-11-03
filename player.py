import pygame
from spritesheet import Spritesheet

#C Major scale
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
        self.note = 0
        self.chord = None

        # flag for one char selected
        self.IS_SELECTED = False
        # flag for all chars selected
        self.ALL_SELECTED = True

        # animation frame
        self.frame = self.frame_list[0]

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

    def set_note_and_chord(self, x, i):
        # if one char selected
        if self.ALL_SELECTED:
            # update chord based on x position
            if x < 100:
                self.note = chord_list[0][i]
                self.chord = "Cmaj"
            elif (x > 100) & (x < 200):
                self.note = chord_list[1][i]
                self.chord = "Dmin"
            elif (x > 200) & (x < 300):
                self.note = chord_list[2][i]
                self.chord = "Emin"
            elif (x > 300) & (x < 400):
                self.note = chord_list[3][i]
                self.chord = "Fmaj"
            elif (x > 400) & (x < 500):
                self.note = chord_list[4][i]
                self.chord = "Gmaj"
            elif (x > 500) & (x < 600):
                self.note = chord_list[5][i]
                self.chord = "Amin"
            elif (x > 600) & (x < 700):
                self.note = chord_list[6][i]
                self.chord = "Bdim"

        # if one char is selected
        elif self.IS_SELECTED:
            # pitch update
            if x < 100:
                self.note = pitch_list[0]
            elif (x > 100) & (x < 200):
                self.note = pitch_list[1]
            elif (x > 200) & (x < 300):
                self.note = pitch_list[2]
            elif (x > 300) & (x < 400):
                self.note = pitch_list[3]
            elif (x > 400) & (x < 500):
                self.note = pitch_list[4]
            elif (x > 500) & (x < 600):
                self.note = pitch_list[5]
            elif x > 600:
                self.note = pitch_list[6]
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
            self.frame = self.frame_list[3 * self.note]
        else:
            self.frame = self.frame_list[3 * self.note + self.volume]
    def set_location(self, frame):
        self.x = frame * 150 + 165
        self.y = 150

    def get_pitch(self):
        return self.note

    def get_chord(self):
        return self.chord

    def get_volume(self):
        return self.volume

    def draw(self, display):
        display.blit(self.frame, (self.x, self.y))

    def load_frames(self):
        my_spritesheet = Spritesheet('image.png')

        self.frame_list = [my_spritesheet.parse_sprite("image0.png"),
                           my_spritesheet.parse_sprite("image1.png"),
                           my_spritesheet.parse_sprite("image2.png"),
                           my_spritesheet.parse_sprite("image3.png"),
                           my_spritesheet.parse_sprite("image4.png"),
                           my_spritesheet.parse_sprite("image5.png"),
                           my_spritesheet.parse_sprite("image6.png"),
                           my_spritesheet.parse_sprite("image7.png"),
                           my_spritesheet.parse_sprite("image8.png"),
                           my_spritesheet.parse_sprite("image9.png"),
                           my_spritesheet.parse_sprite("image10.png"),
                           my_spritesheet.parse_sprite("image11.png"),
                           my_spritesheet.parse_sprite("image12.png"),
                           my_spritesheet.parse_sprite("image13.png"),
                           my_spritesheet.parse_sprite("image14.png"),
                           my_spritesheet.parse_sprite("image15.png"),
                           my_spritesheet.parse_sprite("image16.png"),
                           my_spritesheet.parse_sprite("image17.png"),
                           my_spritesheet.parse_sprite("image18.png"),
                           my_spritesheet.parse_sprite("image19.png"),
                           my_spritesheet.parse_sprite("image20.png")]

        return self.frame_list