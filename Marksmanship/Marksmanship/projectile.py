from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY, COLOR_NAMES
from math import sin, cos, radians, pi
from random import choice, uniform
from matrix33 import Matrix33

PROJECTILE_TYPES = {
        KEY.Q : 'rifle',
        KEY.W : 'rocket',
        KEY.E : 'handgun',
        KEY.R : 'hand_grenade'
    }

class Projectile(object):
    def __init__(self, world, type, position, direction):
        self.world = world
        self.type = type
        self.pos = position
        self.aim = direction
        if self.type == 'rifle':
            self.speed = 1000.0
            self.deviation = 0.0
        elif self.type == 'rocket':
            self.speed = 500.0
            self.deviation = 0.0
        elif self.type == 'handgun':
            self.speed = 800.0
            self.deviation = 0.03 * pi
        elif self.type == 'hand_grenade':
            self.speed = 300.0
            self.deviation = 0.05 * pi
        else:
            self.speed = 0.0
            self.deviation  = 0.0
        self.velocity = self.aim * self.speed
        # Add deviation for the velocity when using an inaccurate gun
        # Indicates whether this is a real or projected projectile
        self.shot = False
    
    def update(self, delta):
        # Update the position of the projectile
        self.pos += self.velocity * delta
        if (self.pos - self.world.bot_target.pos).length() < 24.0 and self.shot == True:
            self.world.bot_target.color = choice(list(COLOR_NAMES.keys()))
    
    def fire(self):
        if self.deviation != 0.0:
            self.add_deviation(self.deviation)
        self.shot = True

    def render(self):
        egi.blue_pen()
        egi.circle(self.pos, 5.0, True)

    def add_deviation(self, deviation):
        # Get a random amount of deviation from a predefined range
        deviation_angle = uniform(-deviation, deviation)
        mat = Matrix33()
        # Add rotation to the matrix
        mat.rotate_update(deviation_angle)
        # Transform the velocity vector to rotate
        mat.transform_vector2d(self.velocity)