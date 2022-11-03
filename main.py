import sys
import pygame
import threading
from game import Game
from ApplicationBLE import RightHand
from DummyBLE import DummyRightHand


if __name__ =="__main__":
    #everything in init in game will run when this runs.
    #creates game object
    
    # rh = RightHand()
    rh = DummyRightHand()
    g = Game(rh)

    print("Opening thread")
    ble_handler = threading.Thread(target=rh.run)
    ble_handler.start()

    g.curr_menu.display_menu()

    while g.running:
        g.game_loop()

    ble_handler.join()
    print("Threads ended, application closed")
