""" Slot_2026.py
 スロットマシーンを作り直す
 画面表示:pygame
"""
import sys, os
import serial
import numpy as np
import pygame
from pygame.locals import *

pic_folder="img"
#use_arduino=True

class Real:
    def __init__(self):
        """
        self.speed
        self.now
        self.target
        self.imgs
        self.area
        """
    def draw(self):
        ...
    def move(self):
        ...
    def stop(self):
        ...

class Slot:
    def __init__(self):
        """
        self.state
        self.level
        self.point
        ?self.role
        
        self.width
        self.height
        
        self.baoudrate
        """
    def start(self):
        ...
    def finish(self):
        ...
    def update(self):
        ...

