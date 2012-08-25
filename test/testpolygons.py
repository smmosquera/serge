"""Tests for Polygon visuals"""

import unittest
import os
import pygame
import math
import time

from helper import *

import serge.render
import serge.blocks.polygons

class TestPolygons(unittest.TestCase, VisualTester):
    """Tests for the Polygons"""

    def setUp(self):
        """Set up the tests"""
        self.r = serge.render.Renderer()
        self.sp = [(0,0), (20, 0), (20, 20), (0, 20), (0, 0)]
        self.np = [(-10,-10), (10, -10), (10, 10), (-10, 10), (-10, -10)]
        self.rp = [(0,0), (20, 0), (20, 10), (0, 10), (0, 0)]
        self.w = (255, 255, 255, 255)
        self.r2 = math.sqrt(2)
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanCreatePolygonVisual(self):
        """testCanCreatePolygonVisual: should be able to crate a polygon visual"""
        v = serge.blocks.polygons.PolygonVisual(self.sp, self.w)
        
    def testPolgonSizeShouldBeCorrect(self):
        """testPolgonSizeShouldBeCorrect: should be able to size a polygon visual correctly"""
        v = serge.blocks.polygons.PolygonVisual(self.sp, self.w)
        self.assertEqual(21, v.width)
        self.assertEqual(21, v.height)
        #
        # And for negative points
        v = serge.blocks.polygons.PolygonVisual(self.np, self.w)
        self.assertEqual(21, v.width)
        self.assertEqual(21, v.height)
        
    def testRenderPolygon(self):
        """testRenderPolygon: should be able to render a polygon"""
        s = self.r.getSurface()
        v = serge.blocks.polygons.PolygonVisual(self.sp, self.w)
        v.renderTo(0, s, (10, 10))
        self.save(s, 2)
        self.assertEqual(self.w, s.get_at((0,0)))
        self.assertEqual(self.w, s.get_at((20,20)))
        self.assertEqual((0,0,0,255), s.get_at((10,10)))
        
    def testRenderPolygonNegativeNumbers(self):
        """testRenderPolygonNegativeNumbers: should be able to render a polygon where the points include negatives"""
        s = self.r.getSurface()
        v = serge.blocks.polygons.PolygonVisual(self.np, self.w)
        v.renderTo(0, s, (10, 10))
        self.save(s, 1)
        self.assertEqual(self.w, s.get_at((0,0)))
        self.assertEqual(self.w, s.get_at((20,20)))
        self.assertEqual((0,0,0,255), s.get_at((10,10)))
        
    def testCanGetRotatedPoints(self):
        """testCanGetRotatedPoints: should be able to get the rotated points"""
        v = serge.blocks.polygons.PolygonVisual(self.rp, self.w)
        v.setAngle(90)
        p = [(int(xi), int(yi)) for xi, yi in v.getPoints()]
        self.assertEqual([(-5, 10), (-4, -10), (5, -10), (4, 10), (-5, 10)], p)
        v.setAngle(0)
        p = [(int(xi), int(yi)) for xi, yi in v.getPoints()]
        self.assertEqual([(-10, -5), (10, -5), (10, 5), (-10, 5), (-10, -5)], p)
                
         

if __name__ == '__main__':
    unittest.main()
