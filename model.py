# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:15:11 2024

@author: Sergio
"""

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents.ant import Ant
from agents.food import Food
from agents.pheromone import Pheromone
from agents.home import Home
import random
from mesa.datacollection import DataCollector

class AntModel(Model):
    def __init__(self, N, width, height, rate_evaporation, random_movement, source_food, evaporation):
        self.evaporation = evaporation
        self.rate_evaporation = rate_evaporation
        self.rate_discont = 0.02
        self.random_movement = random_movement
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0  # Agregar esta línea para inicializar el contador de ID
        self.home = Home(self.next_id(), self, (width//2, height//2))
        self.grid.place_agent(self.home, (width//2, height//2))
        self.source_food = source_food
        self.total_initial_food = 20
        self.datacollector = DataCollector(
            {
                "Comida Recogida": lambda m: m.total_initial_food*source_food - sum([food.amount for food in m.schedule.agents if isinstance(food, Food)])
            }
        )
        self.running = True
        
        for i in range(self.num_agents):
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            ant = Ant(self.next_id(), self)
            self.grid.place_agent(ant, (width//2, height//2))
            self.schedule.add(ant)

        for i in range(source_food):
            food = Food(self.next_id(), self, 20)
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(food, (x, y))
            self.schedule.add(food)
        
    # def add_pheromone(self, pos, amount=1):
    #     pheromone = Pheromone(self.next_id(), self, pos, amount)
    #     print('Feromona añadida')
    #     self.grid.place_agent(pheromone, pos)
        # self.schedule.add(pheromone)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        # Comprobar si queda comida en la simulación
        remaining_food = sum([agent.amount for agent in self.schedule.agents if isinstance(agent, Food)])
        if remaining_food == 0:
            self.running = False  # Detener la simulación si no queda comida
