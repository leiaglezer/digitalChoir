import sys
import pygame
from game import Game

#everything in init in game will run when this runs.
#creates game object
g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
