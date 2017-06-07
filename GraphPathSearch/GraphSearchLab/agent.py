from graphics import egi
from point2d import Point2D
from math import sqrt
import box_world
import graph
class Agent(object):
    def __init__(self, pos, radius, world):
        self.pos = pos
        self.radius = radius
        self.world = world
        # The position since the last waypoint update
        self.previous_position = Point2D()
        # The index of the box the agent is heading to
        self.waypoint_index = self.world.start.idx
        # The full distance from self.previous_position to the center position of the target box
        self.full_distance = 0.0 
        # Remaining distance between self.previous_position and the center position of the target box
        self.remaining_distance = 0.0
        # Distance travelled
        self.progress = 0.0 

        self.is_moving = True
    
    def update_waypoint(self, index):
        # Set the last known position since the waypoint update
        self.previous_position = self.pos
        # Update the waypoint index with a new one
        self.waypoint_index = index
        # Calculate the full distance
        self.full_distance = self.distance_to(self.world.boxes[self.waypoint_index]._vc)
        # Reset the progress
        self.progress = 0.0
        # Calculate the remaining distance
        self.remaining_distance = self.full_distance - self.progress

    def update(self, delta):
        # Update the agent's position
        self.remaining_distance -= 5
        if self.full_distance != 0:
            scale = 1 - (float(self.remaining_distance)/float(self.full_distance))
            source = self.previous_position
            destination = self.world.boxes[self.waypoint_index]._vc
            self.pos.x = source.x + (destination.x - source.x)*scale
            self.pos.y = source.y + (destination.y - source.y)*scale
            self.progress = self.full_distance - self.remaining_distance

    def render(self):
        # Draw the agent
        egi.black_pen()
        egi.circle(self.pos, self.radius,)
    
    def arrived(self):
        # Check if the agent has arrived at the current target waypoint or not
        if self.distance_to(self.world.boxes[self.waypoint_index]._vc) <= 5.0 or self.full_distance == 0:
            return True
        else:
            return False

    def distance_to(self, pos):
        # Calculate the distance between the agent's position and another Point2D
        dx = self.pos.x - pos.x
        dy = self.pos.y - pos.y
        return sqrt(dx*dx + dy*dy)
    