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
    def __init__(self, index):
        # load frames into array
        self.right_selected = None
        self.middle_selected = None
        self.left_selected = None
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

        self.current_note = None
        self.index = index
        self.volume = 0
        self.frame_volume = 0
        self.face = None



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

    # determines if one or all blobs are selected using gloves
    def set_selected_blob_glove(self, imu_data):
        x = imu_data['RAx']

        # one char selected
        if x >= self.index * 10 and x < (self.index + 1) * 10:
            self.IS_SELECTED = True
            self.ALL_SELECTED = False

        # all selected, picked random x value it has to be greater then, will be button later
        elif x >= 30:
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

    def give_note(self, note, sing_note):
        if self.current_note != note:
            self.current_note = note
            sing_note(note, self.index)

    def update_volume(self, sensor, sing_volume):
        if sensor > 5:
            self.volume = sensor / 31
            if sensor > 15:
                self.frame_volume = 2
            else:
                self.frame_volume = 1
        else:
            self.volume = 0
            self.frame_volume = 0
        sing_volume(self.volume, self.index)

    def update_face(self, value):
        self.face = value
        self.frame = self.frame_list[self.face]


    def load_frames(self):
        my_spritesheet = Spritesheet('images/image.png')

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