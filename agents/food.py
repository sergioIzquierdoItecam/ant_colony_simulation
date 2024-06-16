# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:15:38 2024

@author: Sergio
"""

from mesa import Agent

class Food(Agent):
    def __init__(self, unique_id, model, initial_amount):
        super().__init__(unique_id, model)
        self.initial_amount = initial_amount
        self.amount = initial_amount  # Cantidad actual que puede cambiar

    def reduce_amount(self):
        self.amount -= 1  # Cada vez que una hormiga recoge comida, reducimos la cantidad
        if self.amount <= 0:
            self.model.grid.remove_agent(self)  # Si la comida se agota, eliminamos el agente de la simulación