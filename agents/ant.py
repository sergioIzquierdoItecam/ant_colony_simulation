# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:15:23 2024

@author: Sergio
"""

from mesa import Agent
from agents.food import Food
from agents.pheromone import Pheromone
from agents.home import Home
import random

class Ant(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.has_food = False
        self.pheromone_level = 1.0  # Nivel inicial de feromonas cuando recoge comida

    def step(self):
        if not self.has_food:
            self.move_to_food()
        else:
            self.return_to_home()

    def move_to_food(self):
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        food_positions = []
        pheromone_counts = {}

        for neighbor in neighbors:
            cell_contents = self.model.grid.get_cell_list_contents(neighbor)
            if any(isinstance(content, Food) for content in cell_contents):
                food_positions.append(neighbor)
            # Almacenar la cantidad de feromonas en cada casilla vecina
            pheromone_sum = sum(content.amount for content in cell_contents if isinstance(content, Pheromone))
            pheromone_counts[neighbor] = pheromone_sum
        
        if not self.model.evaporation:    
            cell_contents = self.model.grid.get_cell_list_contents(self.pos)
            for content in cell_contents:
                if isinstance(content, Pheromone):
                    # print("Decrementando celda", content.pos, "a", content.amount)
                    content.amount -= 0.1

        if food_positions:
            new_position = random.choice(food_positions)
            self.has_food = True
            self.pheromone_level = 1.0  # Máximas feromonas al recoger comida
            food = next(content for content in self.model.grid.get_cell_list_contents(new_position) if isinstance(content, Food))
            food.reduce_amount()
        else:
            if random.random() <= 0.9 or not(self.model.random_movement):
                max_pheromone = max(pheromone_counts.values(), default=0)
                best_positions = [pos for pos, count in pheromone_counts.items() if count == max_pheromone]
                new_position = random.choice(best_positions) if best_positions else self.pos
            else:
                new_position = random.choice(neighbors)


        self.model.grid.move_agent(self, new_position)

    def return_to_home(self):
        home_position = self.model.home.pos
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = min(possible_steps, key=lambda x: (x[0] - home_position[0]) ** 2 + (x[1] - home_position[1]) ** 2)
        self.model.grid.move_agent(self, new_position)

        # if self.has_food:
        cell_contents = self.model.grid.get_cell_list_contents(new_position)
        pheromone_found = False
        for content in cell_contents:
            if isinstance(content, Pheromone):
                # if self.has_food:
                    # content.amount += self.pheromone_level  # Incrementar la cantidad de feromonas
                # print("Incrementando celda", content.pos, "a", content.amount)
                if self.model.evaporation:
                    content.amount += self.pheromone_level
                else:
                    content.amount += 0.2
                pheromone_found = True
                # else:
                #     content.amount -= 0.1
                #     # pheromone_found = True
 
            if not pheromone_found:
                # self.model.add_pheromone(self, new_position)
                # # Crear nueva feromona si no se encontró ninguna
                pheromone = Pheromone(self.model.next_id()+1, self.model, new_position, amount=self.pheromone_level)
                self.model.grid.place_agent(pheromone, new_position)
                self.model.schedule.add(pheromone)  # Añadir feromona al schedule

            if self.model.evaporation:
                # Disminuir el nivel de feromonas linealmente
                self.pheromone_level -= self.model.rate_discont
                self.pheromone_level = max(self.pheromone_level, 0)

            if self.pos == home_position:
                self.has_food = False
                self.pheromone_level = 0  # Resetear al llegar a casa
