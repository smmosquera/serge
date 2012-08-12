"""Visuals which are polygons"""

import pygame

import serge.visual

class PolygonVisual(serge.visual.SurfaceDrawing):
    """A visual that renders a polygon"""

    def __init__(self, points, colour, width=1, closed=False):
        """Initialise the PolygonVisual"""
        self.closed = closed
        self.colour = colour
        self.line_width = width
        self.setPoints(points)

    def setPoints(self, points):
        """Set the points for the polygon"""
        self.points = points
        #
        # Create a surface of a suitable size
        x, y = zip(*points)
        self.width = max(x)+self.line_width
        self.height = max(y)+self.line_width
        self.clearSurface()
        #
        # Draw the points onto the surface
        pygame.draw.lines(self.getSurface(), self.colour, self.closed, self.points, self.line_width)
        
    def setColour(self, colour):
        """Set the colour"""
        self.colour = colour
        self.setPoints(self.points)
        if self.getAngle() != 0:
            self.setAngle(self.getAngle())
