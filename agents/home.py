# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:15:52 2024

@author: Sergio
"""

from mesa import Agent

class Home(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos