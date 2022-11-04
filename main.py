import threading

#from ApplicationBLE import RightHand
#from DummyBLE import DummyRightHand
from game import Game

if __name__ =="__main__":
    #everything in init in game will run when this runs.
    #creates game object
    
    #rh = RightHand()
    #rh = DummyRightHand()
    g = Game()

    #print("Opening thread")
    #ble_handler = threading.Thread(target=rh.run)
    #ble_handler.start()


    while g.running:
        g.curr_menu.display_menu()

        g.game_loop()

    #ble_handler.join()
    #print("Threads ended, application closed")
