"""Visuals which are polygons"""

import pygame

import serge.visual
from serge.simplevecs import Vec2d

class PolygonVisual(serge.visual.Drawing):
    """A visual that renders a polygon"""

    def __init__(self, points, colour, width=1, closed=False):
        """Initialise the PolygonVisual"""
        super(PolygonVisual, self).__init__()
        self.closed = closed
        self.colour = colour
        self.line_width = width
        self.base_points = points
        #
        # Find a suitable size
        x, y = zip(*points)
        #
        # Shift points so 
        mnx, mxx = min(x), max(x)
        mny, mxy = min(y), max(y)
        cx, cy = (mxx-mnx)/2, (mxy-mny)/2
        x = [xi-cx for xi in x]
        y = [yi-cy for yi in y]
        #
        self.setPoints(zip(x, y))
        #
        # Get dimensions
        self.width = max(x)+self.line_width
        self.height = max(y)+self.line_width

    def setPoints(self, points):
        """Set the points for the polygon"""
        self.points = points
            
    def getPoints(self):
        """Return the points including the effect of rotation"""
        cx, cy, angle = self.width/2, self.height/2, self.getAngle()
        center = Vec2d(cx, cy)
        ret = []
        #
        # Do rotation
        for px, py in self.base_points:
            v = Vec2d(px, py)
            v.rotate_degrees(-angle)
            nx, ny = v
            ret.append((nx, ny))
        #
        # Recenter
        x, y = zip(*ret)
        #
        # Shift points so there are no negatives
        #mx = min(x)
        #my = min(y)
        #x = [xi-mx for xi in x]
        #y = [yi-my for yi in y]
        #
        return zip(x, y)
        
    def setAngle(self, angle):
        """Set the angle of the graphic"""
        self.setPoints(self.getPoints())
        self.angle = angle
        
    def getAngle(self):
        """Return the angle"""
        return self.angle
        
    def renderTo(self, milliseconds, surface, (x, y)):
        """Render the visual"""
        points = [(px+x, py+y) for px, py in self.points]
        pygame.draw.lines(surface, self.colour, self.closed, points, self.line_width)
        
