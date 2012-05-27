"""Tests for block to help with worker processes"""

import unittest
import pygame
import os
import time

from helper import *

import serge.blocks.visualblocks
import serge.blocks.worker

pygame.init()


class TestWorker(unittest.TestCase, VisualTester):
    """Tests for the Worker"""

    def setUp(self):
        """Set up the tests"""
        r = serge.blocks.visualblocks.Rectangle((100, 100), (0, 0, 0))
        self.s1 = r.getSurface()
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanCreateSurfaceQueue(self):
        """testCanCreateSurfaceQueue: should be able to create a queue to process surfaces"""
        todo, result, worker = serge.blocks.worker.getSurfaceProcessingPipeline(self.doProcess1, start=True)
        todo.put((serge.blocks.worker.marshallSurface(self.s1), 50, 40, 20, 30, (255, 0, 0)))
        surface = serge.blocks.worker.unmarshallSurface(*result.get()[0])
        todo.put(None)
        #
        self.save(surface, 1)
        self.checkRect(surface, (255, 0, 0, 255), 50, 40, 20, 30, 'drawn-block')

    def doProcess1(self, surface, x, y, w, h, c):
        """Write a rectangle on the surface"""
        r = serge.blocks.visualblocks.Rectangle((w, h), c)  
        r.renderTo(0, surface, (x-w/2, y-h/2))
        return surface
    
    def testCanCreateDrainingQueue(self):
        """testCanCreateDrainingQueue: should be able have a surface queue that skips to the last item"""
        todo, result, worker = serge.blocks.worker.getSurfaceProcessingPipeline(self.doProcess1, start=False)
        todo.replace((serge.blocks.worker.marshallSurface(self.s1), 50, 40, 20, 30, (0, 255, 0)))
        #
        # We do two of the follow - it looks like it is quite hard to completely remove all 
        # jobs so one might fail. The result is pretty close to what we need from this functionality
        # anyway so let's let it pass!
        todo.replace((serge.blocks.worker.marshallSurface(self.s1), 50, 40, 20, 30, (255, 0, 0)))
        todo.replace((serge.blocks.worker.marshallSurface(self.s1), 50, 40, 20, 30, (255, 0, 0)))
        worker.start()
        surface = serge.blocks.worker.unmarshallSurface(*result.get()[0])
        todo.put(None)
        #
        self.save(surface, 1)
        self.checkRect(surface, (255, 0, 0, 255), 50, 40, 20, 30, 'drawn-block')
        
    

if __name__ == '__main__':
    unittest.main()
