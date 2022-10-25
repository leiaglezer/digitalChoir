import pygame
from spritesheet import Spritesheet


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

        #one char selected
        self.IS_SELECTED = False
        #all chars selected
        self.ALL_SELECTED = True
        self.current_image = self.note_frames[0]

        #will use state to create animations later
        self.state = 'idle'

    def set_current_image(self, frame):
        self.current_image = self.note_frames[frame]

    def set_location(self, frame):
        self.x = frame * 200 + 60
        self.y = 280

    def set_selected(self, mouseX, mouseY):
        # if blob drawing is under mouse click, that blob is selected
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

    def set_character_image(self, chordList, pitchList, x, y, i):
        #if all chars selected
        if self.ALL_SELECTED:
            #chord update
            if x < 100:
                self.pitch = chordList[0][i]
            elif (x > 100) & (x < 200):
                self.pitch = chordList[1][i]
            elif (x > 200) & (x < 300):
                self.pitch = chordList[2][i]
            elif (x > 300) & (x < 400):
                self.pitch = chordList[3][i]
            elif (x > 400) & (x < 500):
                self.pitch = chordList[4][i]
            elif (x > 500) & (x < 600):
                self.pitch = chordList[5][i]
            elif x > 600:
                self.pitch = chordList[6][i]

            #volume update
            if y > 350:
                self.volume = 0
            elif (y < 350) & (y > 200):
                self.volume = 1
            elif y < 200:
                self.volume = 2

            #update curr image based on pitch + volume
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
