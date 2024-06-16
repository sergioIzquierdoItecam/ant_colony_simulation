# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:15:59 2024

@author: Sergio
"""

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import TextElement, ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization import Slider, Checkbox, StaticText
# from mesa.visualization.UserParam import UserSettableParameter
from model import AntModel
from agents.ant import Ant
from agents.food import Food
from agents.pheromone import Pheromone
from agents.home import Home

class FoodText(TextElement):
    def render(self, model):
        total_food = sum([food.amount for food in model.schedule.agents if isinstance(food, Food)])
        return f"Total Comida: {total_food}"

def agent_portrayal(agent):
    if isinstance(agent, Ant):
        return {"Shape": "circle", "Color": "black", "Filled": "true", "Layer": 0, "r": 0.5}
    elif isinstance(agent, Food):
        return {"Shape": "rect", "Color": "green", "Filled": "true", "Layer": 0, "w": 0.5, "h": 0.5}
    elif isinstance(agent, Pheromone):
        # El tamaño del punto de la feromona depende de la cantidad de feromonas
        return {"Shape": "circle", "Color": "red", "Filled": "true", "Layer": 0, "r": 0.1 + min(0.8,agent.amount * 0.1)}
    elif isinstance(agent, Home):
        return {"Shape": "rect", "Color": "blue", "Filled": "true", "Layer": 0, "w": 1, "h": 1}

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
food_text = FoodText()  # Crear el elemento de texto para la comida
# Definir el gráfico
chart = ChartModule(
    [{"Label": "Comida Recogida", "Color": "green"}],
    data_collector_name='datacollector'
)
port = 5861

model_params = {
    # The following line is an example to showcase StaticText.
    "title": StaticText("Parámetros:"),
    "N": Slider("Número de hormigas", 10, 10, 200, 10),
    'evaporation': Checkbox("Evaporación", True),
    "source_food": Slider("Casillas con comida", 1, 1, 20, 1),
    "rate_evaporation": Slider("Tasa de evaporación de feromonas", 0.05, 0.05, 1.0, 0.05),
    # "rate_discont": Slider("Tasa de descuento por lejanía", 0.05, 0.02, 1.0, 0.05),
    "random_movement": Checkbox("Movimiento estocástico", True),
    "width": 20,
    "height": 20,
}

server = ModularServer(AntModel,
                       [grid, food_text, chart],  # Añade el gráfico aquí
                       "Colonia de hormigas",
                       model_params,
                       port=port)
if __name__ == '__main__':
    server.launch()

