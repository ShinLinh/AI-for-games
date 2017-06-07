'''2D Point

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au
'''
from math import sqrt

class Point2D(object):

    __slots__ = ('x', 'y')

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def copy(self):
        return Point2D(self.x, self.y)

    def __str__(self):
        return '(%5.2f,%5.2f)' % (self.x, self.y)
    
    def distance_to(self,p2):
        return  sqrt((self.x - p2.x)*(self.x - p2.x),(self.y - p2.y)*(self.y - p2.y))

#class Collision(object):
    #def __init__(self):
       # self.active = True

    #def check_circle_collide_rectangle(self, circle, rectangle):
        
        #circle_left = circle.x - radius
