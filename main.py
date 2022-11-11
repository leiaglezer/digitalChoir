import sys
import pygame
import threading
from game import Game
from DummyBLE import DummyRightHand
from ApplicationBLE import RightHand
from ApplicationBLE_left import LeftHand

if __name__ == "__main__":
    # everything in init in game will run when this runs.
    # creates game object

    # rh = DummyRightHand()
    # lh = DummyRightHand()
    rh = RightHand()
    lh = LeftHand()

    gloves = (lh, rh)
    g = Game(gloves)

    print("Opening threads")
    r_ble_handler = threading.Thread(target=rh.run)
    r_ble_handler.start()

    l_ble_handler = threading.Thread(target=lh.run)
    l_ble_handler.start()

    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()

    r_ble_handler.join()
    l_ble_handler.join()
    print("Threads ended, application closed")
