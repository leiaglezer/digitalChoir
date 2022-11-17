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
        self.background = pygame.image.load('images/splash.png')
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
        self.SOLO_MODE_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.SOLO_MODE_EVENT, 100)

        # Score
        self.song = [(7, 9, 11), (7, 9, 12), (5, 8, 10), (5, 8, 11), (4, 7, 9), (4, 7, 10), (4, 6, 8), (4, 6, 11)]
        self.drums = [[0] * 3 for _ in range(16)]
        self.looped_hit_beats = [[0, 0]]
        self.drum_loop = 0
        self.selected_drum = [0, 0]
        self.tick = 0
        self.note_range = 14
        self.highest_note = 6
        self.METRONOME = pygame.USEREVENT + 2
        self.DRUMS = pygame.USEREVENT + 4
        self.bpm = 60
        self.measure = 0
        self.total_measures = 8
        self.paused = True
        self.pitch_modifiers = [0, 0, 0]
        pygame.time.set_timer(self.METRONOME, int(1000 * 60 / self.bpm))
        pygame.time.set_timer(self.DRUMS, int(1000 * 60 / (2 * self.bpm)))

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
        self.solo_timbre = "osc"
        self.curr_note = None
        self.mouse_x = None
        self.mouse_y = None
        self.play_music = True
        self.drums_vol = 0
        self.solo_mode = False
        self.solo_channel = 3
        self.solo_fade_time = 100
        self.drum_mode = False

        ######## MUSIC SETUP ##########
        # setup music player
        mixer.init()
        pygame.mixer.set_num_channels(50)
        pygame.mixer.Channel(45).set_volume(self.drums_vol)

        #dict of notes at different timbres + corresponding WAV files
        self.notes = {
            0: {"timbre1": "notes/timbre1A.wav", "timbre2": "notes/timbre2A.wav", "timbre3": "notes/timbre3A.wav", "osc": "osc/A4.wav"},
            1: {"timbre1": "notes/timbre1B.wav", "timbre2": "notes/timbre2B.wav", "timbre3": "notes/timbre3B.wav", "osc": "osc/B4.wav"},
            2: {"timbre1": "notes/timbre1C.wav", "timbre2": "notes/timbre2C.wav", "timbre3": "notes/timbre3C.wav", "osc": "osc/C5.wav"},
            3: {"timbre1": "notes/timbre1D.wav", "timbre2": "notes/timbre2D.wav", "timbre3": "notes/timbre3D.wav", "osc": "osc/D5.wav"},
            4: {"timbre1": "notes/timbre1E.wav", "timbre2": "notes/timbre2E.wav", "timbre3": "notes/timbre3E.wav", "osc": "osc/E5.wav"},
            5: {"timbre1": "notes/timbre1F.wav", "timbre2": "notes/timbre2F.wav", "timbre3": "notes/timbre3F.wav", "osc": "osc/F5.wav"},
            6: {"timbre1": "notes/timbre1G.wav", "timbre2": "notes/timbre2G.wav", "timbre3": "notes/timbre3G.wav", "osc": "osc/Gs5.wav"},
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
        self.solo_singer = Player(3)
        self.drummer = Player(45)
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
                self.display.blit(pygame.image.load('images/center.png'), (0, 0))

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
                        if self.measure == 0:
                            self.tick = 0
                            if self.drum_loop == 1:
                                self.play_drums("lofi-1")
                            elif self.drum_loop == 2:
                                self.play_drums("lofi-2")
                        self.play_measure(self.measure)
                        self.measure += 1
                        if self.measure >= self.total_measures:
                            self.measure = 0

                if self.glove_ui and event.type == self.IMU_DATA_EVENT:
                    self.update_imu()

                    self.read_gestures()

                    if self.accepting_controls() and not self.solo_mode and not self.drum_mode:
                        self.update_selected_users()
                        self.update_selected_volume()
                        self.update_control_mode()

                    self.draw_singers()

                if self.glove_ui and event.type == self.SOLO_MODE_EVENT:
                    if self.solo_mode:
                        self.update_imu()
                        self.play_solo()
                    else:
                        self.stop_solo()
                    self.update_selected_drum() # Here for lower latency

                if self.glove_ui and event.type == self.DRUMS:
                    self.play_drum_tick()

                    if self.drum_mode == True:
                        # Updating drum points happens in solo mode to lower latency
                        self.draw_drum_editor()

                    self.tick += 1
                    if self.tick >= 16:
                        self.tick = 0
                    

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
        print(self.pitch_modifiers)

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
        file = self.notes[(note + self.pitch_modifiers[channel]) % (self.note_range + 1)][self.timbre]
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Channel(channel).play(sound)

    def play_drums(self, drums):
        file = "drums/" + drums + ".wav"
        sound = pygame.mixer.Sound(file)
        pygame.mixer.Channel(45).play(sound)

    def set_drums_vol(self, volume):
        pygame.mixer.Channel(45).set_volume(volume)

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
            self.display.blit(pygame.image.load('images/all.png'), (0, 0))
        else:
            if self.solo_mode:
                self.display.blit(pygame.image.load('images/bottomleft.png'), (0, 0))
            elif self.drum_mode:
                self.display.blit(pygame.image.load('images/bottomright.png'), (0, 0))
            elif self.index == 0:
                self.display.blit(pygame.image.load('images/left.png'), (0, 0))
            elif self.index == 1:
                self.display.blit(pygame.image.load('images/center.png'), (0, 0))
            else:
                self.display.blit(pygame.image.load('images/right.png'), (0, 0))

        for player in self.char_list:
            player.draw(self.display, player.frame)
        
        self.draw_singer_volumes()
        self.draw_singer_pitch()
        self.draw_solo_singer()
        self.draw_drummer()

        if self.drum_mode:
            self.draw_drum_editor()

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
            elif self.last_gestures["LDOWN"] > 0 and self.last_gestures["RDOWN"] > 0:
                print("DOWN")
                new_gestures = default_gestures
                self.pause_music()

            elif self.last_gestures["LLEFT"] > 0 and self.last_gestures["RRIGHT"] > 0:
                print("OUT")
                self.solo_mode = True
                self.drum_mode = False
                new_gestures = default_gestures
            elif self.last_gestures["LRIGHT"] > 0 and self.last_gestures["RLEFT"] > 0:
                print("IN")
                self.solo_mode = False
                new_gestures = default_gestures

            elif self.last_gestures["LUP"] > 0 and self.last_gestures["RRIGHT"] > 0:
                self.start_drums()
            elif self.last_gestures["LDOWN"] > 0 and self.last_gestures["RLEFT"] > 0:
                self.stop_drums()
            elif self.last_gestures["RUP"] > 0 and self.last_gestures["RDOWN"] > 0:
                self.drum_loop += 1
                if self.drum_loop > 2:
                    self.drum_loop = 0
                if self.drum_loop != 0:
                    self.drums_vol = 0.5
                    self.set_drums_vol(self.drums_vol)
                else:
                    self.drums_vol = 0.0
                    self.set_drums_vol(self.drums_vol)
            elif not self.drum_mode and self.last_gestures["LRIGHT"] > 0:
                if not self.paused and self.index != None:
                    self.pitch_modifiers[self.index] += 1
            elif not self.drum_mode and self.last_gestures["LLEFT"] > 0:
                if not self.paused and self.index != None:
                    self.pitch_modifiers[self.index] -= 1
            elif self.drum_mode and (self.last_gestures["LRIGHT"] > 0 or self.last_gestures["LLEFT"] > 0):
                self.drums[self.selected_drum[0]][self.selected_drum[1]] = 1 - self.drums[self.selected_drum[0]][self.selected_drum[1]]
                
        
        self.last_gestures = new_gestures.copy()

    def pause_music(self):
        self.paused = True
        for channel in range(0, 50):
            pygame.mixer.Channel(channel).pause()

    def unpause_music(self):
        self.paused = False
        for channel in range(0, 50):
            pygame.mixer.Channel(channel).unpause()

    def accepting_controls(self):
        return self.imu_data['LAy'] > 8 and not self.paused

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

            self.display.blit(pygame.image.load('images/all.png'), (0, 0))
            for char in self.char_list:
                char.draw(self.display, char.frame)

        # same logic but for individual char
        else:
            # draw correct spotlight background depending on char's index in char_list
            if self.index == 0:
                self.display.blit(pygame.image.load('images/left.png'), (0, 0))
            elif self.index == 1:
                self.display.blit(pygame.image.load('images/center.png'), (0, 0))
            else:
                self.display.blit(pygame.image.load('images/right.png'), (0, 0))

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
            helpscreen = pygame.image.load('images/help-stage.png')
            helpscreen = pygame.transform.scale(helpscreen, (690,435))
            self.display.blit(helpscreen, (0,0))
        


    def draw_volume(self):
        # if self.curr_volume == 0:
        #     self.display.blit(pygame.image.load('images/volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        # elif self.curr_volume == 0.5:
        #     self.display.blit(pygame.image.load('images/volume2.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        # elif self.curr_volume == 1.0:
        #     self.display.blit(pygame.image.load('images/volume3.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        # else:
        #     self.display.blit(pygame.image.load('images/volume1.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
        return

    def draw_singer_volumes(self):
        for i in range(3):
            x = (self.DISPLAY_W / 2) - 25 + ((i - 1) * 160)
            y = (self.DISPLAY_H / 7)
            volume = self.char_list[i].volume

            if volume == 0 or self.paused:
                self.display.blit(pygame.image.load('images/volume0.png'), (x, y))
            elif volume > 0.8:
                self.display.blit(pygame.image.load('images/volume3.png'), (x, y))
            elif volume > 0.5:
                self.display.blit(pygame.image.load('images/volume2.png'), (x, y))
            else:
                self.display.blit(pygame.image.load('images/volume1.png'), (x, y))

    def draw_singer_pitch(self):
        for i in range(3):
            x = (self.DISPLAY_W / 2) - 25 + ((i - 1) * 160)
            y = int(4.5 * (self.DISPLAY_H / 7))
            pitch = self.pitch_modifiers[i] % (self.note_range + 1) # 0 - 14, 0 = 7 = 14
            if pitch > 7:
                pitch -= 15
            pitch_image = pygame.image.load('pitch-icons/pitch' + str(pitch) + '.png')
            pitch_image = pygame.transform.scale(pitch_image, (50, 50))
            self.display.blit(pitch_image, (x, y))

    def draw_solo_singer(self):
        if self.solo_singer.current_note == None:
            self.solo_singer.current_note = 0
        if self.solo_singer.volume == None:
            self.solo_singer.volume = 0
        self.solo_singer.x = (self.DISPLAY_W / 8.3) - 20
        self.solo_singer.y = (2.9 * (self.DISPLAY_W / 7)) + 10
        self.solo_singer.draw_solo(self.display)


    def start_drums(self):
        self.drum_mode = True
        pygame.mixer.Channel(40).set_volume(0.8)
        pygame.mixer.Channel(41).set_volume(0.8)
        pygame.mixer.Channel(42).set_volume(0.8)

    def stop_drums(self):
        self.drum_mode = False

    def play_drum_tick(self):
        if self.drums[self.tick][0] == 1:
            file = "drums/kick.wav"
            sound = pygame.mixer.Sound(file)
            pygame.mixer.Channel(40).play(sound)
        if self.drums[self.tick][1] == 1:
            file = "drums/snare.wav"
            sound = pygame.mixer.Sound(file)
            pygame.mixer.Channel(41).play(sound)
        if self.drums[self.tick][2] == 1:
            file = "drums/hihat.wav"
            sound = pygame.mixer.Sound(file)
            pygame.mixer.Channel(42).play(sound)


    def update_selected_drum(self):
        self.selected_drum[0] = int(15 * self.imu_data['RAx'] / 31)
        
        if self.imu_data['RAy'] > 21:
            self.selected_drum[1] = 0
        elif self.imu_data['RAy'] > 10:
            self.selected_drum[1] = 1
        else:
            self.selected_drum[1] = 2
    
    def draw_drum_editor(self):
        x = 40
        y = self.DISPLAY_H / 3
        dy = 35

        panel = pygame.image.load('images/glass_panel.png')
        panel = pygame.transform.scale(panel, (self.DISPLAY_W * 0.95, 200))
        self.display.blit(panel, (x - 40, y - 40))

        for i in range(3):
            for j in range(16 + 1):
                if j == 0:
                    self.draw_drum_icon(i, x, y, dy)
                else:
                    if j <= 4 or (j > 8 and j <= 12):
                        self.draw_drum_tick(j - 1, i, "grey", (x, y, dy))
                    else:
                        self.draw_drum_tick(j - 1, i, "red", (x, y, dy))

    def draw_drum_tick(self, x, y, color, xydy):
        on = "off"
        if self.drums[x][y] == 1:
            on = "on"
        if self.selected_drum[0] == x and self.selected_drum[1] == y:
            on = "on"
            color = "yellow"
        elif x == self.tick:
            on = "off"
            color = "yellow"
        image = pygame.image.load('drum-icons/' + color + '-' + on + '.png')
        image = pygame.transform.scale(image, (30, 30))
        self.display.blit(image, (xydy[0] + (35 * (x + 1)), xydy[1] + (xydy[2] * y)))


    def draw_drum_icon(self, index, x, y, dy):
        y_shift = 0
        image = None
        if index == 0:
            image = pygame.image.load('drum-icons/kick-drum.png')
        elif index == 1:
            image = pygame.image.load('drum-icons/snare-drum.png')
            y_shift = dy
        else:
            image = pygame.image.load('drum-icons/high-hats.png')
            y_shift = 2 * dy
        image = pygame.transform.scale(image, (45, 45))
        self.display.blit(image, (x, y + y_shift))

    def draw_drummer(self):
        x = (4 * self.DISPLAY_W / 5) + 10
        y = (2.7 * self.DISPLAY_H / 3) - 100
        drummer = pygame.image.load('images/drummer-player.png')
        self.display.blit(drummer, (x, y))

        drumstick = pygame.image.load('drum-icons/drumstick.png')
        drumstick = pygame.transform.scale(drumstick, (80, 120))

        hit = False
        for i in range(3):
            if self.drums[self.tick][i] == 1:
                hit = True

        if hit:
            self.blitRotateCenter(self.display, drumstick, (x - 40, y), 70)
        else:
            self.display.blit(drumstick, (x - 55, y - 30))

    def blitRotateCenter(self, surf, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

        surf.blit(rotated_image, new_rect)

    def play_solo(self):
        for player in self.char_list:
            player.volume = 0.3
            pygame.mixer.Channel(player.index).set_volume(0.2)
            self.index = None
        
        initial_volume_data = self.imu_data['RAy']
        volume_modifier_data = self.imu_data['LAy']

        pitch = int(0.0 + self.imu_data['RAx'] * 14.0 / 31.0)
        fx = self.imu_data['LAx']

        if fx >= 20:
            self.solo_fade_time = (fx * 10) - 50
        else:
            self.solo_fade_time = 50 + (fx * 5)

        self.solo_singer.volume = self.convert_volume(initial_volume_data, volume_modifier_data)
        pygame.mixer.Channel(self.solo_channel).set_volume(self.solo_singer.volume)

        if pitch != self.solo_singer.current_note:
            pygame.mixer.Channel(self.solo_channel).fadeout(self.solo_fade_time)
            if self.solo_channel == 20:
                self.solo_channel = 3
            else:
                self.solo_channel += 1

            self.solo_singer.current_note = pitch
            file = self.notes[pitch][self.solo_timbre]
            sound = pygame.mixer.Sound(file)
            pygame.mixer.Channel(self.solo_channel).play(sound, fade_ms=self.solo_fade_time)

    def convert_volume(self, vol, mod):
        return vol / 31

        vol = vol / 31
        mod -= 15 # -15 - 16
        vol = vol + (2 * mod)
        if vol > 31:
            vol = 31
        if vol < 0:
            vol = 0
        return vol

    def stop_solo(self):
        self.solo_singer.current_note = None
        self.solo_singer.volume = 0
        for i in range(3, 20):
            pygame.mixer.Channel(i).fadeout(100)

    def draw_icons(self):
        self.draw_volume()
        self.display.blit(pygame.image.load('images/backbutton.png'), (10,10))
        self.display.blit(pygame.image.load('images/help.png'), (self.DISPLAY_W- 40,15))

        


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
                # self.display.blit(pygame.image.load('images/volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 0
                self.curr_frame_volume = 0
            elif (self.mouse_y < 350) & (self.mouse_y > 200):
                # self.display.blit(pygame.image.load('images/volume2.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 0.5
                self.curr_frame_volume = 1
            elif self.mouse_y < 200:
                # self.display.blit(pygame.image.load('images/volume3.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                self.curr_volume = 1.0
                self.curr_frame_volume = 2
            else:
                # self.display.blit(pygame.image.load('images/volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
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
                # self.display.blit(pygame.image.load('images/volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                #self.curr_volume = 1
                self.curr_frame_volume = 2
            elif self.imu_data['RAy'] > 5:
                # self.display.blit(pygame.image.load('images/volume3.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
                #self.curr_volume = 0.25
                self.curr_frame_volume = 1
            else:
                # self.display.blit(pygame.image.load('images/volume0.png'), (self.DISPLAY_W/2 - 20,self.DISPLAY_H/7))
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

