import pygame
from pygame import mixer
from menu import MainMenu
from player import Player

class Game:
    def __init__(self):
        ######## APPLICATION SETUP ATTRIBUTES ##########
        #turn game on
        self.curr_char = None
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
        # set initial image/location
        for char in self.char_list:
            char.set_frame()
            char.set_location(self.char_list.index(char))
    def game_loop(self):
        # only plays when player is IN game
        while self.playing:
            for event in pygame.event.get():

                # 1. ####### GAME SETUP #######
                # reset background so you get a white screen
                self.display.blit(pygame.image.load('main.png'), (0, 0))

                #get fresh mouse coordinates
                x, y = pygame.mouse.get_pos()

                # checks if player wants to quit game
                if event.type == pygame.QUIT:
                    self.quit_game()

                #checks if we need to switch between splash and game screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_screens()

                # 2. ####### NEW MOUSECLICK: PLAY MODE SELECTION #######
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # checks if user selects individual char or entire choir
                    for char in self.char_list:
                        char.set_selected_blob(x, y)
                        if char.IS_SELECTED:
                            self.curr_status = 'Solo Mode'
                            self.curr_char = char
                        if char.ALL_SELECTED:
                            self.curr_status = 'Multi Mode'

                    # Stop current music, so that correct music starts playing for single/multimode.
                    for channel in range(0, 50):
                        pygame.mixer.Channel(channel).stop()

                # 3. ####### NEW MOUSEMOTION: CHORD OR NOTE SELECTION #######
                if event.type == pygame.MOUSEMOTION:
                    for i, char in enumerate(self.char_list):
                        #frame stuff
                        char.set_note_and_chord(x, i)
                        char.set_volume(y)
                        char.set_frame()




                # 4. ####### ANIMATION #######
                # draws chars to display
                for char in self.char_list:
                    char.draw(self.display)
                self.window.blit(self.display, (0, 0))
                pygame.display.update()

            # 5. ####### RESET START KEY #######
            self.reset_key()

            # 6. ####### MUSIC PLAYING #######
            if self.curr_status == 'Multi Mode':
                # If the mouse motion is within the x bound of the current chord, don't restart the audio, just keep playing.
                if self.curr_chord == self.char_list[0].get_chord():
                    self.curr_volume = self.char_list[0].get_volume()
                    self.set_volume()
                    continue

                # the mouse has moved to the x bound of a new chord, play new chord.
                else:
                    self.play_chord(self.curr_chord)
                    self.curr_volume = self.char_list[0].get_volume()
                    self.curr_chord = self.char_list[0].get_chord()
                    self.set_volume()

            # same logic as above, but for notes in "Single Mode"
            else:
                if self.curr_pitch == self.curr_char.get_pitch():
                    self.set_volume()
                    continue
                else:
                    self.play_note(self.curr_char.get_pitch())
                    self.curr_pitch = self.curr_char.get_pitch()
                    self.set_volume()


    def set_volume(self):
        if self.curr_status == 'Multi Mode':
            for channel in range(0, 50):
                pygame.mixer.Channel(channel).set_volume(self.curr_volume/2.0)
        else:
            pygame.mixer.Channel(1).set_volume(self.curr_volume/2.0)

    def play_chord(self, chord):
        if chord is not None:
            for i, note in enumerate(self.chords[chord]):
                self.play_note(note, i)

    def play_note(self, note, channel=1):
        file = self.notes[note][self.timbre]
        print(file)
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Channel(channel).play(sound)

    def check_events(self):
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