from NoDisplayGame import NoDisplayGame
from NoDisplayBoard import NoDisplayBoard
from NoDisplayGates import NoDisplayGates
from MagmaBoy_and_HydroGirl_Game.doors import FireDoor, WaterDoor
from MagmaBoy_and_HydroGirl_Game.character import MagmaBoy, HydroGirl
from MagmaBoy_and_HydroGirl_Game.controller import ArrowsController, WASDController

# import pygame and orther needed libraries
import sys
import pygame
from pygame.locals import *


class Event:
    def __init__(self, _type, key):
        self.type = _type
        self.key = key


class Environment:
    def __init__(self, game, level):
        self.game = game
        self.level = level
        self.n_states = (game.display_size[0] * game.display_size[1]) ** 2
        self.action_list = [Event(pygame.KEYDOWN, K_LEFT), Event(pygame.KEYDOWN, K_RIGHT),
                            Event(pygame.KEYDOWN, K_UP), Event(pygame.KEYUP, K_LEFT),
                            Event(pygame.KEYUP, K_RIGHT), Event(pygame.KEYUP, K_UP),
                            Event(pygame.KEYDOWN, K_a), Event(pygame.KEYDOWN, K_d),
                            Event(pygame.KEYDOWN, K_w), Event(pygame.KEYUP, K_a),
                            Event(pygame.KEYUP, K_d), Event(pygame.KEYUP, K_w),
                            Event(None, None)]
        self.n_actions = len(self.action_list)
        
    def reset(self):
        # load level data
        if self.level == "level1":
            self.board = NoDisplayBoard('MagmaBoy_and_HydroGirl_Game/data/level1.txt')
            self.gate_location = (285, 128)
            self.plate_locations = [(190, 168), (390, 168)]
            self.gate = NoDisplayGates(self.gate_location, self.plate_locations)
            self.gates = [self.gate]
    
            self.fire_door_location = (64, 48)
            self.fire_door = FireDoor(self.fire_door_location)
            self.water_door_location = (128, 48)
            self.water_door = WaterDoor(self.water_door_location)
            self.doors = [self.fire_door, self.water_door]
    
            self.magma_boy_location = (16, 336)
            self.magma_boy = MagmaBoy(self.magma_boy_location)
            self.hydro_girl_location = (35, 336)
            self.hydro_girl = HydroGirl(self.hydro_girl_location)
    
        if self.level == "level2":
            self.board = NoDisplayBoard('MagmaBoy_and_HydroGirl_Game/data/level2.txt')
            self.gates = []
    
            self.fire_door_location = (390, 48)
            self.fire_door = FireDoor(self.fire_door_location)
            self.water_door_location = (330, 48)
            self.water_door = WaterDoor(self.water_door_location)
            self.doors = [self.fire_door, self.water_door]
    
            self.magma_boy_location = (16, 336)
            self.magma_boy = MagmaBoy(self.magma_boy_location)
            self.hydro_girl_location = (35, 336)
            self.hydro_girl = HydroGirl(self.hydro_girl_location)
    
        if self.level == "level3":
            self.board = NoDisplayBoard('MagmaBoy_and_HydroGirl_Game/data/level3.txt')
            self.gates = []
    
            self.fire_door_location = (5 * 16, 4 * 16)
            self.fire_door = FireDoor(self.fire_door_location)
            self.water_door_location = (28 * 16, 4 * 16)
            self.water_door = WaterDoor(self.water_door_location)
            self.doors = [self.fire_door, self.water_door]
    
            self.magma_boy_location = (28 * 16, 4 * 16)
            self.magma_boy = MagmaBoy(self.magma_boy_location)
            self.hydro_girl_location = (5 * 16, 4 * 16)
            self.hydro_girl = HydroGirl(self.hydro_girl_location)
            
        return [[self.magma_boy.x, self.magma_boy.y],
                [self.hydro_girl.x, self.hydro_girl.y]]
    
    def step(self, action):        
        # initialize needed classes
        arrows_controller = ArrowsController()
        wasd_controller = WASDController()
            
        # move player
        arrows_controller.control_player([action], self.magma_boy)
        wasd_controller.control_player([action], self.hydro_girl)
    
        self.game.move_player(self.board, self.gates, [self.magma_boy, self.hydro_girl])
        s_next = [[self.magma_boy.x, self.magma_boy.y],
                  [self.hydro_girl.x, self.hydro_girl.y]]
    
        # check for player at special location
        self.game.check_for_death(self.board, [self.magma_boy, self.hydro_girl])
    
        self.game.check_for_gate_press(self.gates, [self.magma_boy, self.hydro_girl])
    
        self.game.check_for_door_open(self.fire_door, self.magma_boy)
        self.game.check_for_door_open(self.water_door, self.hydro_girl)
            
        done = False
        reward = 1
        
        if len(self.gates) > 0:
            for gate in self.gates:
                if gate.plate_is_pressed:
                    reward += 10
                    
        if self.fire_door.player_at_door:
            reward += 10
        if self.water_door.player_at_door:
            reward += 10
        
        # special events
        if self.hydro_girl.is_dead() or self.magma_boy.is_dead():
            done = True
            reward = 0
        
        if self.game.level_is_done(self.doors):
            done = True
            reward = 100
            
        return s_next, reward, done