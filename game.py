import time

import pygame
from pygame import mixer
from menu import MainMenu
from player import Player

class Game:
    def __init__(self, gloves):
        #self.glove = glove
        ######## APPLICATION SETUP ATTRIBUTES ##########
        #turn game on
        pygame.init()
        # background image
        self.background = pygame.image.load('splash.png')
        self.showhelp = False
        # canvas size
        self.DISPLAY_W, self.DISPLAY_H = self.background.get_width(), self.background.get_height()
        # creates canvas
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        # UI Mode
        self.glove_ui = False
        self.mouse_ui = True

        # Glove
        self.gloves = gloves
        self.lh = self.gloves[0]
        self.rh = self.gloves[1]
        self.IMU_DATA_EVENT = pygame.USEREVENT + 1
        self.imu_data = {'RAx': 0, 'RAy': 0, 'LAx': 0, 'LAy': 0}
        self.last_gestures = {'RUP': 0, 'RDOWN': 0, 'LUP': 0, 'LDOWN': 0, 'RRIGHT': 0, 'RLEFT': 0, 'LRIGHT': 0, 'LLEFT': 0}
        self.gestures = []
        pygame.time.set_timer(self.IMU_DATA_EVENT, 200)

        # Score
        self.song = [(7, 9, 11), (7, 9, 12), (5, 8, 10), (5, 8, 11), (4, 7, 9), (4, 7, 10), (4, 6, 8), (4, 6, 11)]
        self.note_range = 14
        self.highest_note = 6
        self.METRONOME = pygame.USEREVENT + 2
        self.bpm = 60
        self.measure = 0
        self.total_measures = 8
        self.paused = True
        pygame.time.set_timer(self.METRONOME, int(1000 * 60 / self.bpm))

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
        self.curr_mode = 'Multi Mode'
        self.curr_volume = None
        self.curr_chord = None
        self.timbre = "osc"
        self.curr_note = None
        self.mouse_x = None
        self.mouse_y = None
        self.play_music = True

        ######## MUSIC SETUP ##########
        # setup music player
        mixer.init()
        pygame.mixer.set_num_channels(50)

        #dict of notes at different timbres + corresponding WAV files
        self.notes = {
            0: {"timbre1": "timbre1A.wav", "timbre2": "timbre2A.wav", "timbre3": "timbre3A.wav", "osc": "osc/A4.wav"},
            1: {"timbre1": "timbre1B.wav", "timbre2": "timbre2B.wav", "timbre3": "timbre3B.wav", "osc": "osc/B4.wav"},
            2: {"timbre1": "timbre1C.wav", "timbre2": "timbre2C.wav", "timbre3": "timbre3C.wav", "osc": "osc/C5.wav"},
            3: {"timbre1": "timbre1D.wav", "timbre2": "timbre2D.wav", "timbre3": "timbre3D.wav", "osc": "osc/D5.wav"},
            4: {"timbre1": "timbre1E.wav", "timbre2": "timbre2E.wav", "timbre3": "timbre3E.wav", "osc": "osc/E5.wav"},
            5: {"timbre1": "timbre1F.wav", "timbre2": "timbre2F.wav", "timbre3": "timbre3F.wav", "osc": "osc/F5.wav"},
            6: {"timbre1": "timbre1G.wav", "timbre2": "timbre2G.wav", "timbre3": "timbre3G.wav", "osc": "osc/Gs5.wav"},
            7: {"osc": "osc/A5.wav"},
            8: {"osc": "osc/B5.wav"},
            9: {"osc": "osc/C6.wav"},
            10: {"osc": "osc/D6.wav"},
            11: {"osc": "osc/E6.wav"},
            12: {"osc": "osc/F6.wav"},
            13: {"osc": "osc/Gs6.wav"},
            14: {"osc": "osc/A6.wav"},
        }

        #dict of chords
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
        self.char_list = [Player(0), Player(1), Player(2)]
        self.curr_char = None
        self.curr_frame_volume = None
        self.last_frame_volume = None
        self.index = None
        self.last_index = None

        # set initial char frame & on-screen location
        for i, char in enumerate(self.char_list):
            char.frame = char.frame_list[3*i]
            char.set_location(i)

        ######## SPRITESHEET REFERENCES ##########
        # get x,y of frame bounding box
        self.x_frame_start = self.char_list[0].frame_list[0].get_rect().x
        self.y_frame_start = self.char_list[0].frame_list[0].get_rect().y

        # width/height each frame (all the same size, so can grab any image)
        self.width = self.char_list[0].frame_list[0].get_width()
        self.height = self.char_list[0].frame_list[0].get_height()

    def game_loop(self):
        # only plays when player is IN game
        while self.playing:
            for event in pygame.event.get():
                # 1. ####### GAME SETUP #######
                # reset background so you get a white screen
                self.display.blit(pygame.image.load('center.png'), (0, 0))

                #get fresh mouse coordinates
                self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

                #if glove, get fresh glove imu data
                #?

                # checks if player wants to quit game
                if event.type == pygame.QUIT:
                    self.quit_game()

                # checks if we need to switch between splash and game screen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_screens()
                    #for now, tapping x will start/stop the music, this will need to be a button + hand motion.
                    if event.key == pygame.K_x:
                        self.start_or_stop_music()

                if event.type == self.METRONOME:
                    if not self.paused:
                        self.play_measure(self.measure)
                        self.measure += 1
                        if self.measure >= self.total_measures:
                            self.measure = 0

                if self.glove_ui and event.type == self.IMU_DATA_EVENT:
                    self.update_imu()

                    self.read_gestures()

                    self.update_selected_users()
                    self.update_selected_volume()
                    self.update_control_mode()

                    self.draw_singers()

                if False and self.glove_ui and event.type == self.IMU_DATA_EVENT:
                    self.update_imu()
                    self.update_volume()
                    self.update_mode()
                    
                    # 5. ####### MUSIC PLAYING #######
                    if self.last_index != self.index:
                        self.stop_music()
                        self.update_sprite_frame()
                    if self.curr_frame_volume != self.last_frame_volume:
                        self.update_sprite_frame()

                    self.draw_sprite()
                    if self.play_music:
                        self.update_chord_or_note()

                if self.play_music:
                # 2. ####### NEW MOUSECLICK: PLAY MODE SELECTION #######
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        click_x,click_y =  pygame.mouse.get_pos()
                        print( "CLICKED MOUSE-  " , pygame.mouse.get_pos())
                        #Check if back button
                        if click_x >=15 and click_x<=50 and click_y>=15 and click_y<=50:
                            print("Back clicked")
                            self.change_screens()
                            self.reset_canvas()
                            self.reset_key()
                            
                        #Check if help button
                        if click_x >=664 and click_x<=682 and click_y>=20 and click_y<=48:
                            print("Help clicked")
                            self.showhelp = True
                            # self.start_or_stop_music()  # for some reason this is breaking the close function but music needs to be stopped when hep screen is displayed

                        #Check for close button in help menu
                        if self.showhelp == True:
                            if click_x >=565 and click_x<=575 and click_y>=40 and click_y<=50:
                                print("Help closed")
                                self.showhelp = False
                                # self.start_or_stop_music()

                        #changes between single and multimode
                        self.update_mode()

                        # Stop current music, so that correct music starts playing for single/multimode.
                        self.stop_music()

                    # 3. ####### CHORD OR NOTE SELECTION #######
                    if event.type == pygame.MOUSEMOTION and self.mouse_ui:
                        self.update_sprite_frame()

                    # if self.glove_ui:
                    # 2. ####### Left hand moves and stays for 5 seconmds: PLAY MODE SELECTION #######
                        # player1_y = 1
                        # player2_y = 2
                        # player2_y = 3
                        # if <<self.imu_data['Lay'] for 10 seconds>>> > player1_y:
                        #     #changes between single and multimode
                        #     self.update_mode()

                        #     # Stop current music, so that correct music starts playing for single/multimode.
                        #     self.stop_music()

                        # # 3. ####### CHORD OR NOTE SELECTION #######
                        # if <<<changes in imu_data['Rax']:
                        #     self.update_sprite_frame()

                    if self.mouse_ui:
                        # 4. ####### ANIMATION #######
                        self.draw_sprite()

                        # 5. ####### MUSIC PLAYING #######
                        self.update_chord_or_note()
                        self.update_volume()


            # 6. ####### RESET START KEY #######
            self.last_index = self.index
            self.last_frame_volume = self.curr_frame_volume
            self.reset_key()

    def update_imu(self):
        self.gestures += self.rh.getGesture()
        self.imu_data['RAx'] = self.rh.getData("RAx")
        self.imu_data['RAy'] = self.rh.getData("RAy")

        self.gestures += self.lh.getGesture()
        self.imu_data['LAx'] = self.lh.getData("LAx")
        self.imu_data['LAy'] = self.lh.getData("LAy")

        print("RX: " + str(self.imu_data['RAx']) + " RY: " + str(self.imu_data['RAy']))
        print("LX: " + str(self.imu_data['LAx']) + " LY: " + str(self.imu_data['LAy']))
        print(self.gestures)

    def start_or_stop_music(self):
        if self.play_music:
            self.stop_music()
            self.play_music = False
        else:
            self.play_music = True

    def stop_music(self):
        # Stop current music, so that correct music starts playing for single/multimode.
        for channel in range(0, 50):
            pygame.mixer.Channel(channel).stop()

    # def set_frame_location(self, char, index):
    #     char.x_frame_start = index * 150 + 140
    #     char.y_frame_start = 150

    # sets if one or all blobs are selected
    # def set_selected_blob(self, char):
    #     # check if mouse click is within bounding box of char's frame image
    #     if (self.mouse_x > char.x_frame_start) & (self.mouse_x < char.x_frame_start + self.width) & (self.mouse_y > char.y_frame_start) & (self.mouse_y < char.y_frame_start + self.height):
    #         char.IS_SELECTED = True
    #
    #     # all selected, picked random x value it has to be greater then, will be button later
    #     else:
    #         char.IS_SELECTED = False

    def update_mode(self):
        for i, char in enumerate(self.char_list):
            if self.mouse_ui:
                char.set_selected_blob(self.mouse_x, self.mouse_y)
            if self.glove_ui:
                char.set_selected_blob_glove(self.imu_data)
                print(str(i) + " " + str(char.IS_SELECTED))

            if char.IS_SELECTED:
                self.curr_mode = 'Single Mode'
                #char from char_list to reference in single mode
                self.curr_char = char
                self.index = i
            if char.ALL_SELECTED:
                self.curr_mode = 'Multi Mode'

    def play_chord(self, chord):
        #plays all notes in chord list
        if chord == self.curr_chord or chord is None:
            return
        for i, note in enumerate(self.chords[chord]):
            self.play_note(note, i)

    def play_note(self, note, channel=1):
        #plays all notes in note list, continues playing if still within x boundary.
        if note == self.curr_note:
            return
        # pygame.mixer.music.fadeout(500)
        # pygame.time.wait(500)
        file = self.notes[note][self.timbre]
        #print(file)
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Channel(channel).play(sound)

    def play_measure(self, measure_num):
        for i in range(min(len(self.song[measure_num]), len(self.char_list))):
            self.char_list[i].give_note(self.song[measure_num][i], self.sing_note)

    def sing_note(self, note, channel):
        file = self.notes[note][self.timbre]
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Channel(channel).play(sound)

    def update_selected_users(self):
        self.index = None
        for player in self.char_list:
            player.set_selected_blob_glove(self.imu_data)
            if player.IS_SELECTED:
                self.index = player.index

    def update_selected_volume(self):
        if self.index != None:
            self.char_list[self.index].update_volume(self.imu_data['RAy'], self.sing_volume)
        else:
            for player in self.char_list:
                player.update_volume(self.imu_data['RAy'], self.sing_volume)
                
    def sing_volume(self, volume, channel):
        pygame.mixer.Channel(channel).set_volume(volume)

    def update_control_mode(self):
        if self.index == None:
            self.curr_mode = 'Multi Mode'
        else:
            self.curr_mode = 'Single Mode'
            self.curr_char = self.char_list[self.index]

    def draw_singers(self):
        if self.paused:
            for player in self.char_list:
                player.update_face(0)
        else:
            for player in self.char_list:
                player.update_face(3 * int((self.song[self.measure][player.index] * 6) / 14) + player.frame_volume)
        
        if self.curr_mode == 'Multi Mode' or self.paused == True:
            self.display.blit(pygame.image.load('all.png'), (0, 0))
        else:
            if self.index == 0:
                self.display.blit(pygame.image.load('left.png'), (0, 0))
            elif self.index == 1:
                self.display.blit(pygame.image.load('center.png'), (0, 0))
            else:
                self.display.blit(pygame.image.load('right.png'), (0, 0))

        for player in self.char_list:
            player.draw(self.display, player.frame)

        self.draw_icons()
        self.display_help()
        self.window.blit(self.display, (0, 0))
        pygame.display.update()
        
    def read_gestures(self):
        default_gestures = {'RUP': 0, 'RDOWN': 0, 'LUP': 0, 'LDOWN': 0, 'RRIGHT': 0, 'RLEFT': 0, 'LRIGHT': 0, 'LLEFT': 0}
        new_gestures = default_gestures.copy()

        if len(self.gestures) > 0:
            i = 0
            
            while i < len(self.gestures):
                new_gestures[self.gestures[i]] += 1
                self.last_gestures[self.gestures[i]] += 1
                i += 1
            
            self.gestures.clear()
            if self.last_gestures["LUP"] > 0 and self.last_gestures["RUP"] > 0:
                print("UP")
                new_gestures = default_gestures
                self.unpause_music()
            if self.last_gestures["LDOWN"] > 0 and self.last_gestures["RDOWN"] > 0:
                print("DOWN")
                new_gestures = default_gestures
                self.pause_music()

            if self.last_gestures["LLEFT"] > 0 and self.last_gestures["RRIGHT"] > 0:
                print("OUT")
                new_gestures = default_gestures
            if self.last_gestures["LRIGHT"] > 0 and self.last_gestures["RLEFT"] > 0:
                print("IN")
                new_gestures = default_gestures
                
        
        self.last_gestures = new_gestures.copy()

    def pause_music(self):
        self.paused = True
        for channel in range(0, 50):
            pygame.mixer.Channel(channel).pause()

    def unpause_music(self):
        self.paused = False
        for channel in range(0, 50):
            pygame.mixer.Channel(channel).unpause()


    def update_sprite_frame(self):
        #updates sprite's current frame based on multi or single mode
        if self.curr_mode == 'Multi Mode' and self.curr_chord is not None:
            for i, char in enumerate(self.char_list):
                frame = 3 * self.chords[self.curr_chord][i] + self.curr_frame_volume
                char.frame = char.frame_list[frame]
        else:
            if self.curr_note is not None:
                frame = 3 * self.curr_note + self.curr_frame_volume
                self.curr_char.frame = self.curr_char.frame_list[frame]

    def draw_sprite(self):
        #draw all chars in char_list
        if self.curr_mode == 'Multi Mode':
                      # volume update based on y position

            self.display.blit(pygame.image.load('all.png'), (0, 0))
            for char in self.char_list:
                char.draw(self.display, char.frame)

        # same logic but for individual char
        else:
            # draw correct spotlight background depending on char's index in char_list
            if self.index == 0:
                self.display.blit(pygame.image.load('left.png'), (0, 0))
            elif self.index == 1:
                self.display.blit(pygame.image.load('center.png'), (0, 0))
            else:
                self.display.blit(pygame.image.load('right.png'), (0, 0))

            # update frame for selected char
            # display "closed mouth" frame for chars that aren't currently selected
            for char in self.char_list:
                if char == self.curr_char:
                    self.curr_char.draw(self.display, self.curr_char.frame)
                else:
                    char.draw(self.display, char.frame_list[0])

        self.draw_icons()
        self.display_help()
        self.window.blit(self.display, (0, 0))
        pygame.display.update()

    def display_help(self):
        if self.showhelp==True:
            helpscreen = pygame.image.load('help-stage.png')
            helpscreen = pygame.transform.scale(helpscreen, (690,435))
            self.display.blit(helpscreen, (0,0))
        


    def draw_volume(self):
        # if self.curr_volume == 0:
        #     self.display.blit(pygame.image.load('volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        # elif self.curr_volume == 0.5:
        #     self.display.blit(pygame.image.load('volume2.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        # elif self.curr_volume == 1.0:
        #     self.display.blit(pygame.image.load('volume3.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        # else:
        #     self.display.blit(pygame.image.load('volume1.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        return

    def draw_icons(self):
        self.draw_volume()
        self.display.blit(pygame.image.load('backbutton.png'), (10,10))
        self.display.blit(pygame.image.load('help.png'), (self.DISPLAY_W- 40,15))



        

    def update_chord_or_note(self):
        if self.mouse_ui:
            if self.mouse_x is not None:
                if self.curr_mode == 'Multi Mode':
                    # update chord based on x position
                    # play chord will first check to see if this chord is currently playing
                        # if it is, the method returns, chord keeps playing
                        # if it isn't, new chord plays and curr_chord updates
                    if (self.mouse_x > 0) and (self.mouse_x < 100):
                        self.play_chord("Cmaj")
                        self.curr_chord = "Cmaj"
                    elif (self.mouse_x > 100) & (self.mouse_x < 200):
                        self.play_chord("Dmin")
                        self.curr_chord = "Dmin"
                    elif (self.mouse_x > 200) & (self.mouse_x < 300):
                        self.play_chord("Emin")
                        self.curr_chord = "Emin"
                    elif (self.mouse_x > 300) & (self.mouse_x < 400):
                        self.play_chord("Fmaj")
                        self.curr_chord = "Fmaj"
                    elif (self.mouse_x > 400) & (self.mouse_x < 500):
                        self.play_chord("Gmaj")
                        self.curr_chord = "Gmaj"
                    elif (self.mouse_x > 500) & (self.mouse_x < 600):
                        self.play_chord("Amin")
                        self.curr_chord = "Amin"
                    elif (self.mouse_x > 600) & (self.mouse_x < 700):
                        self.play_chord("Bdim")
                        self.curr_chord = "Bdim"

                # single mode
                else:
                    # same logic, but updates note based on x position
                    if self.mouse_x < 100:
                        self.play_note(0)
                        self.curr_note = 0
                    elif (self.mouse_x > 100) & (self.mouse_x < 200):
                        self.play_note(1)
                        self.curr_note = 1
                    elif (self.mouse_x > 200) & (self.mouse_x < 300):
                        self.play_note(2)
                        self.curr_note = 2
                    elif (self.mouse_x > 300) & (self.mouse_x < 400):
                        self.play_note(3)
                        self.curr_note = 3
                    elif (self.mouse_x > 400) & (self.mouse_x < 500):
                        self.play_note(4)
                        self.curr_note = 4
                    elif (self.mouse_x > 500) & (self.mouse_x < 600):
                        self.play_note(5)
                        self.curr_note = 5
                    elif (self.mouse_x > 600) & (self.mouse_x < 700):
                        self.play_note(6)
                        self.curr_note = 6
                    else:
                        return
        if self.glove_ui:
            if self.curr_mode == "Multi Mode":
                x = self.imu_data['LAx'] * 22.5
                if x < 100:
                    self.play_chord("Cmaj")
                    self.curr_chord = "Cmaj"
                elif x < 200:
                    self.play_chord("Dmin")
                    self.curr_chord = "Dmin"
                elif x < 300:
                    self.play_chord("Emin")
                    self.curr_chord = "Emin"
                elif x < 400:
                    self.play_chord("Fmaj")
                    self.curr_chord = "Fmaj"
                elif x < 500:
                    self.play_chord("Gmaj")
                    self.curr_chord = "Gmaj"
                elif x < 600:
                    self.play_chord("Amin")
                    self.curr_chord = "Amin"
                elif x < 700:
                    self.play_chord("Bdim")
                    self.curr_chord = "Bdim"
                else:
                    return
            else:
                x = self.imu_data['LAx'] * 22.5
                if x < 100:
                    self.play_note(0)
                    self.curr_note = 0
                elif x < 200:
                    self.play_note(1)
                    self.curr_note = 1
                elif x < 300:
                    self.play_note(2)
                    self.curr_note = 2
                elif x < 400:
                    self.play_note(3)
                    self.curr_note = 3
                elif x < 500:
                    self.play_note(4)
                    self.curr_note = 4
                elif x < 600:
                    self.play_note(5)
                    self.curr_note = 5
                elif x < 700:
                    self.play_note(6)
                    self.curr_note = 6
                else:
                    return

    def update_volume(self):
        if self.mouse_y is not None and self.mouse_ui:
            # volume update based on y position
            if self.mouse_y > 350:
                # self.display.blit(pygame.image.load('volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 0
                self.curr_frame_volume = 0
            elif (self.mouse_y < 350) & (self.mouse_y > 200):
                # self.display.blit(pygame.image.load('volume2.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 0.5
                self.curr_frame_volume = 1
            elif self.mouse_y < 200:
                # self.display.blit(pygame.image.load('volume3.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 1.0
                self.curr_frame_volume = 2
            else:
                # self.display.blit(pygame.image.load('volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 0.0
                self.curr_frame_volume = 0
            
            
            # for char in self.char_list:
            #     char.draw(self.display, char.frame)
            #     self.window.blit(self.display, (0, 0))
            # pygame.display.update()

            for channel in range(0, 50):
                pygame.mixer.Channel(channel).set_volume(self.curr_volume)

        if self.glove_ui:
            if self.imu_data['RAy'] > 18:
                # self.display.blit(pygame.image.load('volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                #self.curr_volume = 1
                self.curr_frame_volume = 2
            elif self.imu_data['RAy'] > 5:
                # self.display.blit(pygame.image.load('volume3.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                #self.curr_volume = 0.25
                self.curr_frame_volume = 1
            else:
                # self.display.blit(pygame.image.load('volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 0.0
                self.curr_frame_volume = 0
            
            if self.imu_data['RAy'] > 5:
                self.curr_volume = self.imu_data['RAy'] / 31
            
            
            # for char in self.char_list:
            #     char.draw(self.display, char.frame)
            #     self.window.blit(self.display, (0, 0))
            # pygame.display.update()

            for channel in range(0, 50):
                pygame.mixer.Channel(channel).set_volume(self.curr_volume)
            

    def check_events(self):
        #checks for which menu to display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_x,click_y =  pygame.mouse.get_pos()
                print( "CLICKED MOUSE-  " , pygame.mouse.get_pos())

                #Mouse and Glove button clicks
                if click_x >=174 and click_x<=312 and click_y>=324 and click_y<=370:
                    print("Mouse Selected")
                    self.curr_menu.glove_selected= False
                    self.curr_menu.mouse_selected= True
                    self.curr_menu.initial_buttons= False
                    self.glove_ui = False
                    self.mouse_ui = True
                    #Select Mouse UI
                elif click_x >=405 and click_x<=543 and click_y>=324 and click_y<=370:
                    print("Glove Selected")
                    self.curr_menu.glove_selected= True
                    self.curr_menu.mouse_selected= False
                    self.curr_menu.initial_buttons= False
                    self.glove_ui = True
                    self.mouse_ui = False
                    self.lh.setStatus(1)
                    self.rh.setStatus(1)
                    #Select Glove UI

            
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

