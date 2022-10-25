import pygame
from menu import MainMenu
from player import Player

# chordList: [[C,E,D], [D,F,A], [E,G,B], [F,A,C], [G,B,D], [A,C,E], [B,D,F]]
# chord encoding: A=0, B=1, C=2, D=3, E=4, F=5, G=6
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
pitchList = [0, 1, 2, 3, 4, 5, 6]


class Game:
    def __init__(self):
        pygame.init()
        # self.running will be true when game is on
        self.running = True
        # self.playing will be true when game is being played
        self.playing = False
        # Game is not being played when first starting up, start key therefore is false
        self.START_KEY = False

        #background image
        self.background = pygame.image.load('stage.png')
        # canvas size
        self.DISPLAY_W, self.DISPLAY_H = self.background.get_width(), self.background.get_height()
        # creates canvas
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        # window to show up on screen
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        # font for game
        self.font_name = 'Kemco Pixel Bold.ttf'



        self.BLACK, self.WHITE  = (24,22,23), (255, 255, 255)
        self.BLUE, self.PINK = (97, 113, 255), (207, 29, 207)
        self.GREEN = (48, 181, 4)
        self.curr_menu = MainMenu(self)
        self.blobList = [Player(), Player(), Player()]

        # set initial image/location
        for blob in self.blobList:
            blob.set_current_image(self.blobList.index(blob) * 3)
            blob.set_location(self.blobList.index(blob))

    def game_loop(self):
        # only plays when player is IN game
        while self.playing:
            # check inputs, checking if player wants to quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # stop game from running
                    self.running = False
                    # stop game loop
                    self.playing = False
                    # stop display of main menu
                    self.curr_menu.run_display = False

                # if any keyboard item has been pressed
                if event.type == pygame.KEYDOWN:
                    # if that key is the return key
                    if event.key == pygame.K_RETURN:
                        self.START_KEY = True
                        self.playing = False

                self.display.fill(self.WHITE)
                # tuple to get mouse position
                x, y = pygame.mouse.get_pos()

                # update each character's image based on mouse click / mouse motion
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for blob in self.blobList:
                        blob.set_selected(x, y)

                if event.type == pygame.MOUSEMOTION:
                    for blob in self.blobList:
                        # update the animation frame
                        blob.set_character_image(chordList, pitchList, x, y, self.blobList.index(blob))

                # draw all the characters to the screen
                for blob in self.blobList:
                    blob.draw(self.display)

                # draws the display to the window, shows to user
                self.window.blit(self.display, (0, 0))
                pygame.display.update()

            # resets key to false for next frame
            self.reset_key()

    def check_events(self):
        # goes thru list of everything player can do on computer
        # if player clicks x on window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stop game from running
                self.running = False
                # stop game loop
                self.playing = False
                # stop display of main menu
                self.curr_menu.run_display = False

            # if any keyboard item has been pressed
            if event.type == pygame.KEYDOWN:
                # if that key is the return key
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True

    def reset_key(self):
        self.START_KEY = False

    # self is a reference to the game object
    def draw_text(self, text, size, x, y, color):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
