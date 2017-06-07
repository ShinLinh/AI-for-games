from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY, COLOR_NAMES
from math import sin, cos, radians
from random import random, randrange, choice, uniform
from agent import Agent

class Obstacle(object):
    def __init__(self, world,x, y, radius):
        self.world = world
        self.radius = radius
        self.pos = Vector2D()
        self.pos.x = x 
        self.pos.y = y
        self.tagged = False
        self.distance_from_boundary = 10.0
        self.hiding_position = Vector2D()
        self.bounding_radius = radius + 2.0
    def render(self):
        egi.white_pen()
        egi.circle(self.pos, self.radius)
        
        if self.tagged:
            egi.red_pen()
            egi.text_at_pos(self.pos.x, self.pos.y, 'x')
            egi.text_at_pos(self.hiding_position.x, self.hiding_position.y, 'x')

    def get_hiding_position(self,hunter):
        target = hunter
        away_distance = self.distance_from_boundary + self.radius
        
        vector_to_hunter = (self.pos - hunter.pos).normalise()

        hiding_position = (vector_to_hunter * away_distance) + self.pos
        self.hiding_position = hiding_position
        return hiding_position
