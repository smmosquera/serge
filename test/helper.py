"""Some helper mixins for testing"""

import os
import pygame
import math

def p(f):
    """Return full path to image file"""
    return os.path.join(os.path.abspath(os.curdir), 'test', 'images', f)

def j(*f):
    """Return full path to junk file"""
    return os.path.join(os.path.abspath(os.curdir), 'test', 'junk', *f)

def f(*f):
    """Return full path to file"""
    return os.path.join(os.path.abspath(os.curdir), 'test', 'files', *f)
    
class VisualTester:
    """A mixin to help testing visual items"""
    
    def save(self, r, n):
        """Save the surface"""
        if isinstance(r, pygame.Surface):
            surface = r
        else:
            surface = r.getSurface()
        pygame.image.save(surface, os.path.join('test', 'junk', '%d.png' % n))

    def checkRect(self, surface, colour, cx, cy, w, h, name, accuracy=5, check_alpha=True, black=(0,0,0,255)):
        """Check that a rectangle is in the right place"""
        upto = 4 if check_alpha else 3
        for dy in (-1, +1):
            for dx in (-1, +1):
                got = surface.get_at((int(cx + dx*(w/2+2)), int(cy + dy*(h/2+2))))
                for e,g in zip(black, got)[:upto]:
                    self.assert_(abs(e-g)<=accuracy, 
                        '%s - Failed black test at %d, %d (%s)' % (name, dx, dy, got))
                got = surface.get_at((int(cx + dx*(w/2-2)), int(cy + dy*(h/2-2))))
                for e,g in zip(colour, got)[:upto]:
                    self.assert_(abs(e-g)<=accuracy, 
                        '%s - Failed colour test at %d, %d (%s)' % (name, dx, dy, got))

    def check45Rect(self, surface, colour, cx, cy, w, h, name, accuracy=5, check_alpha=True, black=(0,0,0,255)):
        """Check that a rectangle rotated at 45 degrees is in the right place"""
        upto = 4 if check_alpha else 3
        r2 = math.sqrt(2)
        for dx, dy in ((-1, 0), (0, -1), (0, +1), (+1, 0)):
            got = surface.get_at((int(cx + dx*(r2*w/2+3)), int(cy + dy*(r2*h/2+3))))
            for e,g in zip(black, got)[:upto]:
                self.assert_(abs(e-g)<=accuracy, 
                    '%s - Failed black test at %d, %d (%s)' % (name, dx, dy, got))
            got = surface.get_at((int(cx + dx*(r2*w/2-3)), int(cy + dy*(r2*h/2-3))))
            for e,g in zip(colour, got)[:upto]:
                self.assert_(abs(e-g)<=accuracy, 
                    '%s - Failed colour test at %d, %d (%s)' % (name, dx, dy, got))


    def checkCircle(self, surface, colour, x, y, radius, name, accuracy=5, check_alpha=True, black=(0,0,0,255)):
        """Check that a circle is in the right place"""
        upto = 4 if check_alpha else 3
        cx, cy = x+radius, y+radius
        for dx, dy in ((0, +1), (0, -1), (+1, 0), (-1, 0)):
            got = surface.get_at((cx + dx*(radius + 2), cy + dy*(radius + 2)))
            for e,g in zip(black, got)[:upto]:
                self.assert_(abs(e-g)<=accuracy, 
                    '%s - Failed black test at %d, %d (%s)' % (name, dx, dy, got))
            got = surface.get_at((cx + dx*(radius-1), cy + dy*(radius-1)))
            for e,g in zip(colour, got)[:upto]:
                self.assert_(abs(e-g)<=accuracy, 
                    '%s - Failed colour test at %d, %d (%s)' % (name, dx, dy, got))

    def checkPoint(self, colour, surface, (x, y), name, accuracy=1, check_alpha=True):
        """Check a point is the right colour"""
        upto = 4 if check_alpha else 3
        got = surface.get_at((x, y))
        for e,g in zip(colour, got)[:upto]:
            self.assert_(abs(e-g)<=accuracy, 
                '%s - Failed colour test at %d, %d (%s)' % (name, x, y, got))
        
class FakeKeyboard(object):
    """Allows easy faking of the state of the keyboard"""
    
    def __init__(self):
        """Initialise the keyboard"""
        self.down_states = {}
        self.up_states = {}
        self.clicked_states = {}
        
    def isDown(self, key):
        return self.down_states.get(key, False)

    def isUp(self, key):
        return self.up_states.get(key, False)

    def isClicked(self, key):
        return self.clicked_states.get(key, False)

    def areAnyDown(self):
        """Is any button depressed?"""
        for v in self.down_states.values():
            if v:
                return True
        return False

    def areAnyClicked(self):
        """Is any button clicked?"""
        for v in self.clicked_states.values():
            if v:
                return True
        return False

    def update(self, interval):
        pass


class FakeMouse(object):

    def __init__(self):
        """Initialise the mouse"""
        self.x = self.y = 0 
        
    def getScreenPos(self):
        """Return the screen pos"""
        return (self.x, self.y)
        
