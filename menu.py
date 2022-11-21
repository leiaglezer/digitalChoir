import pygame

class Menu():
    def __init__(self, game):
        #saves reference to game object
        self.game = game
        self.initial_buttons = True
        self.glove_selected = False
        self.mouse_selected = False
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        #tells menu to keep running
        self.run_display = True
    def blit_screen(self):
        # add Surface to window
        self.game.window.blit(self.game.display, (0, 0))
        # moves image onto computer screen
        pygame.display.update()
        self.game.reset_key()
    
    def draw_buttons(self):
        if self.initial_buttons:
            self.game.display.blit(pygame.image.load('images/mouse-button.png'), (170, 320))
            self.game.display.blit(pygame.image.load('images/glove-button.png'), (405, 320))
        if self.mouse_selected:
            self.game.display.blit(pygame.image.load('images/mouse-selected-button.png'), (170, 320))
            self.game.display.blit(pygame.image.load('images/glove-button.png'), (405, 320))
            self.game.display.blit(pygame.image.load('images/enter-message.png'), (158, 405))

        if self.glove_selected:
            self.game.display.blit(pygame.image.load('images/mouse-button.png'), (170, 320))
            self.game.display.blit(pygame.image.load('images/glove-selected-button.png'), (405, 320))
            self.game.display.blit(pygame.image.load('images/glove-message.png'), (158, 405))

        

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
        while self.run_display:
            #check if anything is clicked
            self.game.check_events()
            #if start key is pressed, no longer display this menu
            self.check_input()
            #set Surface to black to reset it
            self.game.display.fill(self.game.BLACK)
            #draw background image
            self.game.display.blit(pygame.image.load('images/splash.png'), (0, 0))
            self.draw_buttons()

 

            #adds Surface to Window and Window to Screen
            self.blit_screen()

    def check_input(self):
        #if return key is pressed
        if self.game.start:
            #stop displaying display screen
            #start displaying game screen
            self.game.playing = True
            self.run_display = False