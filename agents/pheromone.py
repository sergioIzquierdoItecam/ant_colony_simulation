# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:15:45 2024

@author: Sergio
"""

from mesa import Agent

class Pheromone(Agent):
    def __init__(self, unique_id, model, pos, amount=1):
        super().__init__(unique_id, model)
        self.pos = pos
        # self.rate_evaporation = model.rate_evaporation
        self.amount = amount
        

    def step(self):
        # print('Feromona', self.pos, 'con una cantidad de', self.amount)
        if self.model.evaporation:
            # print('Evaporación', self.amount)
            self.amount = self.amount - self.model.rate_evaporation
        if self.amount <= 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)  # Remueve la feromona del schedule