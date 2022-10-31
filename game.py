import time

import pygame
from pygame import mixer
from menu import MainMenu
from player import Player


class Game:
    def __init__(self):
        self.curr_pitch = None
        self.status = 'all'
        self.event = None
        self.curr_volume = None

        pygame.init()
        # self.running will be true when game is on
        self.RUNNING = True
        # self.playing will be true when game is being played
        self.PLAYING = False
        # flag to switch between splash & game screen
        self.START_KEY = False
        # background image
        self.background = pygame.image.load('splash.png')
        # canvas size
        self.DISPLAY_W, self.DISPLAY_H = self.background.get_width(), self.background.get_height()
        # creates canvas
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        # window to show up on screen
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE)
        self.BLACK, self.WHITE = (13, 11, 11), (117, 73, 34)
        self.BLUE, self.PINK = (97, 113, 255), (207, 29, 207)
        self.GREEN, self.DARK_RED = (48, 181, 4), (84, 0, 0)
        # menu to start on
        self.curr_menu = MainMenu(self)
        # instantiate three blobs
        self.blobList = [Player(), Player(), Player()]
        self.curr_chord = None

        # setup music player
        mixer.init()
        pygame.mixer.set_num_channels(50)
        self.wavList = []

        # set initial image/location
        for blob in self.blobList:
            blob.set_current_image(self.blobList.index(blob) * 3)
            blob.set_location(self.blobList.index(blob))

    def game_loop(self):
        # only plays when player is IN game
        while self.PLAYING:
            for event in pygame.event.get():
                # 1. ####### GAME SETUP #######
                self.reset_canvas()
                x, y = pygame.mouse.get_pos()

                # checks if player wants to quit game
                if event.type == pygame.QUIT:
                    self.quit_game()

                # switches between splash and game screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_screens()

                # 2. ####### PLAY MODE SELECTION #######
                # checks if user selects individual blob or entire choir
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for blob in self.blobList:
                        blob.set_selected_blob(x, y)
                        # Single Selection Mode
                        if blob.IS_SELECTED:
                            self.status = 'single'
                            for channel in range(0, 50):
                                pygame.mixer.Channel(channel).stop()
                        # Multi Selection Mode
                        if blob.ALL_SELECTED:
                            self.status = 'all'
                            for channel in range(0, 50):
                                pygame.mixer.Channel(channel).stop()

                # updates each blob's pitch, wav file based on mouse position
                if event.type == pygame.MOUSEMOTION:
                    for i, blob in enumerate(self.blobList):
                        self.wavList = []
                        blob.set_character_iage(x, y, i)
                        blob.set_wav()
                        self.wavList.append(blob.get_wav())


                # 3. ####### ANIMATION #######
                # draws blobs to display
                for blob in self.blobList:
                    blob.draw(self.display)

                # draws the display to the window, shows to user
                self.window.blit(self.display, (0, 0))
                pygame.display.update()

            # resets START_KEY to false (you're on game screen) for next frame
            self.reset_key()

            # 4. ####### PITCH CHANGES AND MUSIC PLAYING #######
            if self.status == 'all':
                if self.curr_chord == self.blobList[0].chord:
                    self.curr_volume = self.blobList[0].volume

                    for channel in range(0, 50):
                        pygame.mixer.Channel(channel).set_volume(self.curr_volume)
                    continue
                else:
                    if self.wavList:
                        for i, x in enumerate(self.wavList):
                            pygame.mixer.Channel(i + 1).play(x, -1)
                            self.curr_volume = self.blobList[0].volume

                            for channel in range(0, 50):
                                pygame.mixer.Channel(channel).set_volume(self.curr_volume)
                            self.curr_chord = blob.chord

            elif self.status == 'single':

                for blob in self.blobList:
                    if blob.IS_SELECTED:
                        if self.curr_pitch == blob.pitch:
                            pygame.mixer.Channel(1).set_volume(blob.volume)
                            continue
                        else:
                            for channel in range(0, 50):
                                pygame.mixer.Channel(channel).stop()
                            blob.set_wav()
                            pygame.mixer.Channel(1).play(blob.wav)
                            pygame.mixer.Channel(1).set_volume(blob.volume)
                            self.curr_pitch = blob.pitch

                        # if self.curr_volume == blob.volume:
                        #     continue
                        # else:
                        #     # change the volume of only the selected blob
                        #     self.curr_volume = blob.volume




            # 5. ####### VOLUME CHANGES #######
            # if(mode == all):
                # change volume to current y value for all channels
            #
            #else:
                # find the current selected blob
                # find the channel of current selected blob
                # change volume for  value for that channel

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUNNING = False
                self.PLAYING = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
    def reset_canvas(self):
        # redraw fresh canvas
        self.display.fill(self.WHITE)

    def reset_key(self):
        self.START_KEY = False

    def quit_game(self):
        self.RUNNING = False
        self.PLAYING = False

    def change_screens(self):
        self.START_KEY = True
        self.PLAYING = False