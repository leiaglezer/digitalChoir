import pygame
from pygame import mixer
from menu import MainMenu
from player import Player


class Game:
    def __init__(self):
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

        ######## MUSIC SETUP ##########
        # setup music player
        mixer.init()
        pygame.mixer.set_num_channels(50)
        self.wav_list = []

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
                self.display.blit(pygame.image.load('splash.png'), (0, 0))

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
                        # Single Selection Mode
                        if char.IS_SELECTED:
                            self.curr_status = 'Solo Mode'
                        # Multi Selection Mode
                        if char.ALL_SELECTED:
                            self.curr_status = 'Multi Mode'

                    # Stop current music, so that correct music starts playing for single/multimode.
                    for channel in range(0, 50):
                        pygame.mixer.Channel(channel).stop()

                # 3. ####### NEW MOUSEMOTION: CHORD OR NOTE SELECTION #######
                # clear old wav list, so correct wavs are loaded each loop
                self.reset_wav_list()

                if event.type == pygame.MOUSEMOTION:
                    for i, char in enumerate(self.char_list):
                        char.set_pitch(x, i)
                        char.set_volume(y)
                        char.set_frame()
                        char.set_wav()
                        self.wav_list.append(char.get_wav())

                # 4. ####### ANIMATION #######
                # draws chars to display
                for char in self.char_list:
                    char.draw(self.display)
                self.window.blit(self.display, (0, 0))
                pygame.display.update()

            # 5. ####### RESET START KEY #######
            self.reset_key()

            # 6. ####### PITCH, VOLUME CHANGES & MUSIC PLAYING #######
            if self.curr_status == 'Multi Mode':
                # if the mouse motion is within the x bound of the current chord
                if self.curr_chord == self.char_list[0].get_chord():
                    # check and potentially change the global volume variable
                    self.curr_volume = self.char_list[0].get_volume()
                    # set the volume for all channels
                    for channel in range(0, 50):
                        pygame.mixer.Channel(channel).set_volume(self.curr_volume)
                    # continue playing the current chord
                    continue

                # the mouse has moved to the x bound of a new chord
                else:
                    for i, x in enumerate(self.wav_list):
                        # play the new chord
                        pygame.mixer.Channel(i + 1).play(x, -1)
                        # update the global volume variable
                        self.curr_volume = self.char_list[0].get_volume()
                        # play the global current chord variable

                        for channel in range(0, 50):
                            pygame.mixer.Channel(channel).set_volume(self.curr_volume)
                        # update the global current chord variable
                        self.curr_chord = char.get_chord()

            if self.curr_status == 'Solo Mode':
                # go through char list
                for char in self.char_list:
                    # find the selected char
                    if char.IS_SELECTED:
                        if self.curr_pitch == char.get_pitch():
                            # set the char's volume in a single channel
                            pygame.mixer.Channel(1).set_volume(char.get_volume())
                            continue
                        else:
                            pygame.mixer.Channel(1).play(char.get_wav())
                            pygame.mixer.Channel(1).set_volume(char.get_volume())
                            self.curr_pitch = char.get_pitch()
    def reset_wav_list(self):
        self.wav_list = []
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