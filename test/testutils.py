"""Tests for the utilities that speed up common operations"""

import unittest

import unittest
import pygame
import os

from helper import *

pygame.init()

import serge.blocks.utils

import serge.render
import serge.actor
import serge.zone
import serge.world
import serge.engine
import serge.visual

class TestUtils(unittest.TestCase):
    """Tests for the Utils"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        
        
    def tearDown(self):
        """Tear down the tests"""

    def testCanSetLayersForEngine(self):
        """testCanSetLayersForEngine: should be able to quickly set layers"""
        e = serge.engine.Engine()
        serge.blocks.utils.createLayersForEngine(e, ['one','two','three'])
        r = e.getRenderer()
        #
        # Should be the three layers that we created
        l1 = r.getLayer('one')
        l2 = r.getLayer('two')
        l3 = r.getLayer('three')
        #
        # Should have the right ordering
        self.assertEqual(0, l1.order)
        self.assertEqual(1, l2.order)
        self.assertEqual(2, l3.order)
        #
        # And be active
        self.assertEqual(True, l1.active)
        self.assertEqual(True, l2.active)
        self.assertEqual(True, l3.active)
        #
        # Adding another should add one more in sequence
        serge.blocks.utils.createLayersForEngine(e, ['four'])
        l4 = r.getLayer('four')
        self.assertEqual(3, l4.order)
        self.assertEqual(True, l4.active)

    def testCanSetVirtualLayersForEngine(self):
        """testCanSetVirtualLayersForEngine: should be able to quickly set virtual layers"""
        e = serge.engine.Engine()
        serge.blocks.utils.createVirtualLayersForEngine(e, ['one','two','three'])
        r = e.getRenderer()
        #
        # Should be the three layers that we created
        l1 = r.getLayer('one')
        l2 = r.getLayer('two')
        l3 = r.getLayer('three')
        #
        # Should be virtual
        self.assertEqual(r.getSurface(), l1.getSurface())
        self.assertEqual(r.getSurface(), l2.getSurface())
        self.assertEqual(r.getSurface(), l3.getSurface())
        #
        # Should have the right ordering
        self.assertEqual(0, l1.order)
        self.assertEqual(1, l2.order)
        self.assertEqual(2, l3.order)
        #
        # And be active
        self.assertEqual(True, l1.active)
        self.assertEqual(True, l2.active)
        self.assertEqual(True, l3.active)
        #
        # Adding another should add one more in sequence
        serge.blocks.utils.createLayersForEngine(e, ['four'])
        l4 = r.getLayer('four')
        self.assertEqual(3, l4.order)
        self.assertEqual(True, l4.active)

    def testCanAddWorldsWithZones(self):
        """testCanAddWorldsWithZones: should be able to quickly add worlds with big zones"""
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one', 'two', 'three'])
        #
        # Should be three worlds created
        w1 = e.getWorld('one')
        w2 = e.getWorld('two')
        w3 = e.getWorld('three')
        #
        # Each should have one zone
        self.assertEqual(1, len(w1.zones))
        self.assertEqual(1, len(w2.zones))
        self.assertEqual(1, len(w3.zones))
        #
        # Zones should be active and large
        for w in (w1, w2, w3):
            z = list(w.zones)[0]
            self.assertEqual(True, z.active)   
            self.assert_(z.getSpatial()[0] < -1000)
            self.assert_(z.getSpatial()[1] < -1000)
            self.assert_(z.width > 2000)
            self.assert_(z.height > 2000)

    def testCanAddSpriteActorToWorld(self):
        """testCanAddSpriteActorToWorld: should be able to quickly add an actor for a sprite to the world"""
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('b', 'bluerect.png')        
        #
        # Add it and it should be returned
        a = serge.blocks.utils.addSpriteActorToWorld(w, 'tag', 'name', 'b', 'layer', (100, 200))
        self.assertEqual(a, w.findActorByName('name'))
        #
        # Should be positioned where we wanted it
        self.assertEqual(100, a.x)
        self.assertEqual(200, a.y)
        #
        # Should be on the right layer and have the right metadata
        self.assertEqual('layer', a.getLayerName())
        self.assertEqual('tag', a.tag)
        self.assertEqual('name', a.name)
        #
        # If don't specify a position then it should be centered
        b = serge.blocks.utils.addSpriteActorToWorld(w, 'tag', 'b', 'b', 'layer')
        self.assertEqual(320, b.x)
        self.assertEqual(240, b.y)

    def testCanAddVisualActorToWorld(self):
        """testCanAddVisualActorToWorld: should be able to quickly add an actor with a visual to the world"""
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('b', 'bluerect.png')        
        #
        # Add it and it should be returned
        visual = serge.visual.Sprite()
        a = serge.blocks.utils.addVisualActorToWorld(w, 'tag', 'name', visual, 'layer', (100, 200))
        self.assertEqual(a, w.findActorByName('name'))
        #
        # Should be positioned where we wanted it
        self.assertEqual(100, a.x)
        self.assertEqual(200, a.y)
        #
        # Should be on the right layer and have the right metadata
        self.assertEqual('layer', a.getLayerName())
        self.assertEqual('tag', a.tag)
        self.assertEqual('name', a.name)
        #
        # If don't specify a position then it should be centered
        b = serge.blocks.utils.addSpriteActorToWorld(w, 'tag', 'b', 'b', 'layer')
        self.assertEqual(320, b.x)
        self.assertEqual(240, b.y)
        
    def testCanAddActorToWorld(self):
        """testCanAddActorToWorld: should be able to quickly add an actor to the world"""
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('b', 'bluerect.png')        
        #
        # Add it and it should be returned
        visual = serge.visual.Sprite()
        actor1 = serge.actor.Actor('tag', 'name')
        a = serge.blocks.utils.addActorToWorld(w, actor1, 'b', 'layer', (100, 200))
        self.assertEqual(a, w.findActorByName('name'))
        #
        # Should be positioned where we wanted it
        self.assertEqual(100, a.x)
        self.assertEqual(200, a.y)
        #
        # Should be on the right layer and have the right metadata
        self.assertEqual('layer', a.getLayerName())
        self.assertEqual('tag', a.tag)
        self.assertEqual('name', a.name)
        #
        # If don't specify a position then it should be centered
        actor2 = serge.actor.Actor('tag', 'name')
        b = serge.blocks.utils.addActorToWorld(w, actor2, 'b', 'layer')
        self.assertEqual(320, b.x)
        self.assertEqual(240, b.y)
    
        
if __name__ == '__main__':
    unittest.main()
