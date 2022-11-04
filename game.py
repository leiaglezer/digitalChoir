import pygame
from pygame import mixer
from menu import MainMenu
from player import Player

class Game:
    def __init__(self, glove):
        self.glove = glove
        ######## APPLICATION SETUP ATTRIBUTES ##########
        #turn game on
        pygame.init()
        # background image
        self.background = pygame.image.load('splash.png')
        # canvas size
        self.DISPLAY_W, self.DISPLAY_H = self.background.get_width(), self.background.get_height()
        # creates canvas
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))

        # window to show up on screen
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.BLACK, self.WHITE = (13, 11, 11), (255, 255, 255)

        ######## MENU SETUP ATTRIBUTES ##########
        # menu to start on
        self.curr_menu = MainMenu(self)
        # self.running will be true when game is on
        self.running = True
        # self.playing will be true when game is being played
        self.playing = False
        # flag to switch between splash & game screen
        self.start = False

        ######## MUSIC PLAYING ATTRIBUTES ##########
        self.curr_pitch = None
        self.curr_status = 'Multi Mode'
        self.curr_volume = None
        self.curr_chord = None
        self.timbre = "timbre1"
        self.curr_note = None
        self.x = None
        self.y = None
        self.start_music = False

        ######## MUSIC SETUP ##########
        # setup music player
        mixer.init()
        pygame.mixer.set_num_channels(50)

        self.notes = {
            0: {"timbre1": "timbre1A.wav"},
            1: {"timbre1": "timbre1B.wav"},
            2: {"timbre1": "timbre1C.wav"},
            3: {"timbre1": "timbre1D.wav"},
            4: {"timbre1": "timbre1E.wav"},
            5: {"timbre1": "timbre1F.wav"},
            6: {"timbre1": "timbre1G.wav"},
        }

        self.chords = {
            "Cmaj": [2, 4, 6],
            "Dmin": [3, 5, 0],
            "Emin": [4, 6, 1],
            "Fmaj": [5, 0, 2],
            "Gmaj": [6, 1, 3],
            "Amin": [0, 2, 4],
            "Bdim": [1, 3, 5]
        }

        ######## INITIAL CHARACTER SETUP ##########
        # instantiate three chars
        self.char_list = [Player(), Player(), Player()]
        self.curr_char = None
        self.curr_frame_volume = None

        # set initial image/location
        for i, char in enumerate(self.char_list):
            char.frame = char.frame_list[i]
            char.set_location(i)

        ######## SPRITESHEET REFERENCES ##########
        # get x,y of frame bounding box
        self.x_frame = self.char_list[0].frame_list[0].get_rect().x
        self.y_frame = self.char_list[0].frame_list[0].get_rect().y

        # width/height each frame (all the same size, so can grab any image)
        self.width = self.char_list[0].frame_list[0].get_width()
        self.height = self.char_list[0].frame_list[0].get_height()
    def game_loop(self):
        # only plays when player is IN game
        while self.playing:
            for event in pygame.event.get():
                # 1. ####### GAME SETUP #######
                # reset background so you get a white screen
                self.display.blit(pygame.image.load('main.png'), (0, 0))

                #get fresh mouse coordinates
                self.x, self.y = pygame.mouse.get_pos()

                # checks if player wants to quit game
                if event.type == pygame.QUIT:
                    self.quit_game()

                #checks if we need to switch between splash and game screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_screens()

                # 2. ####### NEW MOUSECLICK: PLAY MODE SELECTION #######
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #changes between single and multi mode
                    self.update_mode()

                    # Stop current music, so that correct music starts playing for single/multimode.
                    for channel in range(0, 50):
                        pygame.mixer.Channel(channel).stop()

                # 3. ####### CHORD OR NOTE SELECTION #######
                if event.type == pygame.MOUSEMOTION:
                    self.update_sprite_frame()

                # 4. ####### ANIMATION #######
                self.draw_sprite()

                # 5. ####### MUSIC PLAYING #######
                self.update_chord_or_note()
                self.update_volume()

                # 6. ####### RESET START KEY #######
                self.reset_key()


    def update_mode(self):
        # checks if user selects individual char or entire choir
        for char in self.char_list:
            char.set_selected_blob(self.x, self.y)
            if char.IS_SELECTED:
                self.curr_status = 'Single Mode'
                self.curr_char = char
            if char.ALL_SELECTED:
                self.curr_status = 'Multi Mode'

    def play_chord(self, chord):
        #plays all notes in chord list
        if chord == self.curr_chord or chord is None:
            return
        for i, note in enumerate(self.chords[chord]):
            self.play_note(note, i)

    def play_note(self, note, channel=1):
        #plays all notes in note list, continues playing if still within x boundary.
        if note == self.curr_note:
            return
        file = self.notes[note][self.timbre]
        print(file)
        sound = pygame.mixer.Sound(file)
        #pygame.mixer.music.fadeout(10)
        pygame.mixer.Channel(channel).play(sound)

    def update_sprite_frame(self):
        #updates sprite's current frame based on multi or single mode
        if self.curr_status == 'Multi Mode':
            for i, char in enumerate(self.char_list):
                frame = 3 * self.chords[self.curr_chord][i] + self.curr_frame_volume
                char.frame = char.frame_list[frame]
        else:
            frame = 3 * self.curr_note + self.curr_frame_volume
            self.curr_char.frame = self.curr_char.frame_list[frame]

    def draw_sprite(self):
        #draw all chars in char list
        if self.curr_status == 'Multi Mode':
            for char in self.char_list:
                char.draw(self.display, char.frame)
        # same logic but for individual char
        # displays "closed mouth" for chars that aren't currently playing
        else:
            for char in self.char_list:
                if char == self.curr_char:
                    self.curr_char.draw(self.display, self.curr_char.frame)
                else:
                    char.draw(self.display, char.frame_list[0])

        self.window.blit(self.display, (0, 0))
        pygame.display.update()

    def update_chord_or_note(self):
        if self.x is not None:
            if self.curr_status == 'Multi Mode':
                # update chord based on x position
                if (self.x > 0) & (self.x < 100):
                    self.play_chord("Cmaj")
                    self.curr_chord = "Cmaj"
                elif (self.x > 100) & (self.x < 200):
                    self.play_chord("Dmin")
                    self.curr_chord = "Dmin"
                elif (self.x > 200) & (self.x < 300):
                    self.play_chord("Emin")
                    self.curr_chord = "Emin"
                elif (self.x > 300) & (self.x < 400):
                    self.play_chord("Fmaj")
                    self.curr_chord = "Fmaj"
                elif (self.x > 400) & (self.x < 500):
                    self.play_chord("Gmaj")
                    self.curr_chord = "Gmaj"
                elif (self.x > 500) & (self.x < 600):
                    self.play_chord("Amin")
                    self.curr_chord = "Amin"
                elif (self.x > 600) & (self.x < 700):
                    self.play_chord("Bdim")
                    self.curr_chord = "Bdim"

            # single mode
            else:
                # update note based on x position
                if self.x < 100:
                    self.play_note(0)
                    self.curr_note = 0
                elif (self.x > 100) & (self.x < 200):
                    self.play_note(1)
                    self.curr_note = 1
                elif (self.x > 200) & (self.x < 300):
                    self.play_note(2)
                    self.curr_note = 2
                elif (self.x > 300) & (self.x < 400):
                    self.play_note(3)
                    self.curr_note = 3
                elif (self.x > 400) & (self.x < 500):
                    self.play_note(4)
                    self.curr_note = 4
                elif (self.x > 500) & (self.x < 600):
                    self.play_note(5)
                    self.curr_note = 5
                elif (self.x > 600) & (self.x < 700):
                    self.play_note(6)
                    self.curr_note = 6
                else:
                    return
    def update_volume(self):
        if self.y is not None:
            # volume update based on y position
            if self.y > 350:
                self.curr_volume = 0
                self.curr_frame_volume = 0
            elif (self.y < 350) & (self.y > 200):
                self.curr_volume = 0.5
                self.curr_frame_volume = 1
            elif self.y < 200:
                self.curr_volume = 1.0
                self.curr_frame_volume = 2
            else:
                self.curr_volume = 0.0
                self.curr_frame_volume = 0

            for channel in range(0, 50):
                pygame.mixer.Channel(channel).set_volume(self.curr_volume)
    def check_events(self):
        #checks for which menu to display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start = True
    def reset_canvas(self):
        # redraw fresh canvas
        self.display.fill(self.WHITE)
    def reset_key(self):
        self.start = False
    def quit_game(self):
        self.running = False
        self.playing = False
    def change_screens(self):
        self.start = True
        self.playing = False