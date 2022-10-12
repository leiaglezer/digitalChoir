import pygame

class Menu():
    #include variables all reference classes need
    #include reference to game object
    def __init__(self, game):
        #saves reference to game object
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        #tells menu to keep running
        self.run_display = True

    def blit_screen(self):
        # add Surface to window
        self.game.window.blit(self.game.display, (0, 0))
        # moves image onto computer screen
        pygame.display.update()
        self.game.reset_key()

#inherit values of Menu class
class MainMenu(Menu):
    def __init__(self, game):
        #using constructor of Menu class, gets game instance
        Menu.__init__(self, game)

        self.state = "Start"
        self.startx = self.mid_w
        self.starty = self.mid_h + 30

    def display_menu(self):
        self.run_display = True
        #similar to thanks for playing loop
        while self.run_display:
            #check if anything is clicked
            self.game.check_events()
            #if start key is pressed, no longer display this menu
            self.check_input()

            #set Surface to black to reset it
            self.game.display.fill(self.game.BLACK)

            #add text to Surface
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Start Musical Composer', 20, self.startx, self.starty)

            #adds Surface to Window and Window to Screen
            self.blit_screen()

    def check_input(self):
        #if return key is pressed
        if self.game.START_KEY:
            #stop displaying display menu
            #start displaying game!
            self.game.playing = True
            self.run_display = False