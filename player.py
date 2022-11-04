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

        # flag for one char selected
        self.IS_SELECTED = False
        # flag for all chars selected
        self.ALL_SELECTED = True


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

    def set_location(self, index):
        self.x = index * 150 + 165
        self.y = 150

    def draw(self, display, frame):
        display.blit(frame, (self.x, self.y))

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