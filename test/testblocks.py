"""Tests for some of the useful blocks"""

import unittest
import pygame
import os
import time

from helper import *

pygame.init()

import serge.blocks.visualblocks
import serge.blocks.visualeffects
import serge.blocks.effects
import serge.blocks.layout
import serge.blocks.scores
import serge.blocks.themes
import serge.blocks.actors
import serge.blocks.utils
import serge.blocks.directions
import serge.blocks.achievements

import serge.render
import serge.actor
import serge.zone
import serge.world
import serge.engine
import serge.geometry

class TestVisualBlocks(unittest.TestCase, VisualTester):
    """Tests for the VisualBlocks"""

    def setUp(self):
        """Set up the tests"""
        self.r = serge.render.Renderer()
        serge.visual.Register.clearItems()
        
    def tearDown(self):
        """Tear down the tests"""


    ### Simple shapes ###

    def testRectangleBlock(self):
        """testRectangleBlock: a coloured rectange"""
        s = serge.blocks.visualblocks.Rectangle((10, 12), (255,0,0,255))
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.assertEqual(10, s.width)
        self.assertEqual(12, s.height)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 55, 66, 10, 12, 'block')
        #
        # Non filled version - thick should work
        self.r.clearSurface()
        s = serge.blocks.visualblocks.Rectangle((10, 12), (255,0,0,255), 5)
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 55, 66, 10, 12, 'block')
        #
        # Non filled version - thin should fail
        self.r.clearSurface()
        s = serge.blocks.visualblocks.Rectangle((10, 12), (255,0,0,255), 1)
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.assertRaises(Exception, self.checkRect, self.r.surface, (255, 0, 0, 255), 55, 66, 10, 12, 'block')
                        
    def testCircleBlock(self):
        """testCircleBlock: a coloured circle"""
        s = serge.blocks.visualblocks.Circle((40), (255,0,0,255))
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.save(self.r, 1)
        self.checkCircle(self.r.surface, (255, 0, 0, 255), 10, 20, 40, 'block')
        #
        # Non-filled version - thick should work
        self.r.clearSurface()                
        s = serge.blocks.visualblocks.Circle((40), (255,0,0,255), 5)
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.checkCircle(self.r.surface, (255, 0, 0, 255), 10, 20, 40, 'block')
        #
        # Non-filled version - thin should fail
        self.r.clearSurface()                
        s = serge.blocks.visualblocks.Circle((40), (255,255,0,255), 1)
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.save(self.r, 3)
        self.assertRaises(Exception, self.checkCircle, self.r.surface, (255, 255, 0, 255), 10, 20, 40, 'block')

    def testRectangleTransparency(self):
        """testRectangleTransparency: should be able to do transparent rectangle"""
        s = serge.blocks.visualblocks.Rectangle((10, 12), (255,0,0,128))
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.assertEqual(10, s.width)
        self.assertEqual(12, s.height)
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (127, 0, 0, 255), 55, 66, 10, 12, 'block')
        
    def testCircleTransparency(self):
        """testCircleTransparency: should be able to do circle transparent"""
        s = serge.blocks.visualblocks.Circle((40), (255,0,0,128))
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.save(self.r, 1)
        self.checkCircle(self.r.surface, (127, 0, 0, 255), 10, 20, 40, 'block')
        
    def testCircleChangeColour(self):
        """testCircleChangeColour: should be able to change circle colour"""
        s = serge.blocks.visualblocks.Circle((40), (255,0,0,255))
        s.colour = (255, 255, 0, 255)
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.save(self.r, 1)
        self.checkCircle(self.r.surface, (255, 255, 0, 255), 10, 20, 40, 'block')
        
    def testRectangleChangeColour(self):
        """testRectangleChangeColour: should be able to change rectangle colour"""
        s = serge.blocks.visualblocks.Rectangle((10, 12), (255,0,0,255))
        s.colour = (255, 255, 0, 255)
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.assertEqual(10, s.width)
        self.assertEqual(12, s.height)
        self.checkRect(self.r.surface, (255, 255, 0, 255), 55, 66, 10, 12, 'block')
        
        

    def testRectangleWithText(self):
        """testRectangleWithText: a rectangular block with some text"""
        s = serge.blocks.visualblocks.RectangleText('sHs', (0, 255, 0, 255), (20, 40), (255,0,0,255))
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 60, 80, 20, 40, 'block')
        self.assertEqual((0, 255, 0, 255), self.r.surface.get_at((59, 78)))
        
    def testCircleWithText(self):
        """testCircleWithText: a circular block with text"""
        s = serge.blocks.visualblocks.CircleText('H', (0, 255, 0, 255), (40), (255,0,0,255))
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.save(self.r, 1)
        self.checkCircle(self.r.surface, (255, 0, 0, 255), 10, 20, 40, 'block')
        self.assertEqual((0, 255, 0, 255), self.r.surface.get_at((50, 58)))
        
    def testSpriteWithText(self):
        """testSpriteWithText: a sprite with some text"""
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        s = serge.blocks.visualblocks.SpriteText('   H   ', (255, 0, 0, 255), 'green')
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (0, 255, 0, 255), 75, 85, 50, 50, 'block')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))

    def testSpriteWithTextIsDifferentSprite(self):
        """testSpriteWithTextIsDifferentSprite: when using sprites each instance should be a new copy"""
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        s1 = serge.blocks.visualblocks.SpriteText('H', (255, 0, 0, 255), 'green')
        s2 = serge.blocks.visualblocks.SpriteText('H', (255, 0, 0, 255), 'green')
        # Fake out an extra cell
        s1.cells.append(None)
        s1.setCell(1)
        self.assertEqual(1, s1.current_cell)
        self.assertEqual(0, s2.current_cell)
        
    def testToggle(self):
        """testToggle: can have a toggle"""
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerFromFiles('all', p('allrect%d.png'), 4) # four cells
        #
        b = serge.blocks.visualblocks.TextToggle('H', (255, 0, 0, 255), 'all')
        b.renderTo(0, self.r.getSurface(), (50, 60))
        #
        self.checkRect(self.r.surface, (0, 255, 0, 255), 75, 85, 50, 50, 'default')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        #
        b.setCell(0)
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (0, 255, 0, 255), 75, 85, 50, 50, 'cell 0')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        #
        b.setCell(2)
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (0, 0, 255, 255), 75, 85, 50, 50, 'cell 2')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        # Off should be cell 1
        # On should be cell 0
        b.setOn()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (0, 255, 0, 255), 75, 85, 50, 50, 'on')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        b.setOff()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (255, 0, 0, 255), 75, 85, 50, 50, 'off')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        # Can toggle
        b.toggle()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (0, 255, 0, 255), 75, 85, 50, 50, 'toggle 1')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        b.toggle()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (255, 0, 0, 255), 75, 85, 50, 50, 'toggle 2')
        self.assertEqual((255, 0, 0, 255), self.r.surface.get_at((74, 83)))
        
    def testToggleFailsWithSingleCellSprite(self):
        """testToggleFailsWithSingleCellSprite: should fail if try to create a toggle from a single cell sprite"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'), zoom=0.5)
        self.assertRaises(serge.blocks.visualblocks.InvalidSprite,
            serge.blocks.visualblocks.TextToggle, 'H', (255, 0, 0, 255), 'green')
    
    ### Outlined blocks ###
        
    def testOutlinedBlock(self):
        """testOutlinedBlock: should be able to do an outlined block"""
        s = serge.blocks.visualblocks.Rectangle((50, 60), (255,0,0,255), stroke_colour=(0,255,0,255), stroke_width=10)
        s.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 1)
        #
        # Outer rectangle
        self.checkRect(self.r.surface, (0, 255, 0, 255), 75, 90, 50, 60, 'outer')
        #
        # Inner
        self.checkRect(self.r.surface, (255, 0, 0, 255), 75, 90, 30, 40, 'inner', black=(0,255,0,255))
        
    def testFailOutlinedBlockBadParameters(self):
        """testFailOutlinedBlockBadParameters: should fail when specifying bad parameters for outlined block"""
        self.assertRaises(serge.blocks.visualblocks.InvalidParameters,
            serge.blocks.visualblocks.Rectangle, (50, 60), (255,0,0,255), stroke_colour=(0,255,0,255), stroke_width=-1)
        self.assertRaises(serge.blocks.visualblocks.InvalidParameters,
            serge.blocks.visualblocks.Rectangle, (50, 60), (255,0,0,255), stroke_colour=(0,255,0,255), stroke_width=26)
        
    def testOutlinedCircle(self):
        """testOutlinedCircle: should be able to do an outlined circle"""
        s = serge.blocks.visualblocks.Circle((40), (255,0,0,255), stroke_colour=(0,255,0,255), stroke_width=10)
        s.renderTo(0, self.r.getSurface(), (10, 20))
        self.checkCircle(self.r.surface, (0, 255, 0, 255), 10, 20, 40, 'outer')
        self.checkCircle(self.r.surface, (255, 0, 0, 255), 20, 30, 30, 'inner', black=(0,255,0,255))
        
    def testFailOutlinedCircleBadParameters(self):
        """testFailOutlinedCircleBadParameters: should fail when specifying bad parameters for outlined circle"""
        self.assertRaises(serge.blocks.visualblocks.InvalidParameters,
            serge.blocks.visualblocks.Circle, (40), (255,0,0,255), stroke_colour=(0,255,0,255), stroke_width=-1)
        self.assertRaises(serge.blocks.visualblocks.InvalidParameters,
            serge.blocks.visualblocks.Circle, (40), (255,0,0,255), stroke_colour=(0,255,0,255), stroke_width=41)
    
    ### Progress bar types ###
    
    def testCanDoSingleColourProgressBar(self):
        """testCanDoSingleColourProgressBar: should be able to do a single colour progress bar"""
        b = serge.blocks.visualblocks.ProgressBar((100, 20), value_ranges=[(0, 20, (255,0,0,255))])
        #
        b.value = 10
        self.r.clearSurface()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        w, h = 0.5*100, 20
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 50+w/2, 60+h/2, w, h, 'half')
        #        
        b.value = 20
        self.r.clearSurface()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 2)
        w, h = 1.0*100, 20
        self.checkRect(self.r.surface, (255, 0, 0, 255), 50+w/2, 60+h/2, w, h, 'full')

    def testCanDoMultiColourProgressBar(self):
        """testCanDoMultiColourProgressBar: should be able to do multiple colours in progress bar"""
        b = serge.blocks.visualblocks.ProgressBar((100, 20), 
            value_ranges=[(0, 5, (255,0,0,255)), (5, 10, (0,255,0,255)), (10, 20, (255,255,255,255))])
        #
        b.value = 2
        self.r.clearSurface()
        w, h = 2.0/20.0*100, 20
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (255, 0, 0, 255), 50+w/2, 60+h/2, w, h, 'one')
        #        
        b.value = 7
        self.r.clearSurface()
        w, h = 7.0/20.0*100, 20
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (0, 255, 0, 255), 50+w/2, 60+h/2, w, h, 'two')
        #        
        b.value = 12
        self.r.clearSurface()
        w, h = 12.0/20.0*100, 20
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.checkRect(self.r.surface, (255, 255, 255, 255), 50+w/2, 60+h/2, w, h, 'three')

    def testCanDoProgressBarWithBorder(self):
        """testCanDoProgressBarWithBorder: should be able to do border around progress"""
        b = serge.blocks.visualblocks.ProgressBar((100, 20), value_ranges=[(0, 20, (255,0,0,255))],
            border_width=4, border_colour=(255,255,255,255))
        #
        b.value = 10
        self.r.clearSurface()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        w, h = 0.5*100, 20
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 255, 255, 255), 50+w/2, 60+h/2, w, h, 'half')
        #        
        b.value = 20
        self.r.clearSurface()
        b.renderTo(0, self.r.getSurface(), (50, 60))
        self.save(self.r, 2)
        w, h = 1.0*100, 20
        self.checkRect(self.r.surface, (255, 255, 255, 255), 50+w/2, 60+h/2, w, h, 'full')
        
    def testFailProgressBarSetValueOutOfRange(self):
        """testFailProgressBarSetValueOutOfRange: should fail when setting the value out of range"""
        b = serge.blocks.visualblocks.ProgressBar((100, 20), 
            value_ranges=[(0, 5, (255,0,0,255)), (5, 10, (0,255,0,255)), (10, 20, (255,255,255,255))])
        for v in (-10, -1, 22, 200):
            self.assertRaises(serge.blocks.visualblocks.OutOfRange, setattr, b, 'value', v)
        #
        # Should be able to do zero
        b.value = 0
                   
    def testFailProgressBarOverlappingRanges(self):
        """testFailProgressBarOverlappingRanges: should fail if progress bar has overlapping ranges"""
        self.assertRaises(serge.blocks.visualblocks.OverlappingRanges,
            serge.blocks.visualblocks.ProgressBar, (100, 20), 
            value_ranges=[(0, 5, (255,0,0,255)), (4, 10, (0,255,0,255)), (10, 20, (255,255,255,255))])
        
    def testFailProgressBarNonContiguousRanges(self):
        """testFailProgressBarNonContiguousRanges: should fail if progress bar ranges are not contiguous"""
        self.assertRaises(serge.blocks.visualblocks.RangesNotContiguous,
            serge.blocks.visualblocks.ProgressBar, (100, 20), 
            value_ranges=[(0, 5, (255,0,0,255)), (6, 10, (0,255,0,255)), (10, 20, (255,255,255,255))])
        
           
      


class TestLayoutBlocks(unittest.TestCase, VisualTester):
    """Tests for the LayoutBlocks"""

    def setUp(self):
        """Set up the tests"""
        self.e = serge.engine.Engine()
        self.r = serge.render.Renderer()
        self.r.addLayer(serge.render.Layer('back', 0))
        self.w = serge.world.World('main')
        self.r.addLayer(serge.render.Layer('main', 1))
        self.z = serge.zone.Zone()
        self.w.addZone(self.z)
        self.z.active = True
        serge.visual.Register.clearItems()
        
    def tearDown(self):
        """Tear down the tests"""

    def getActor(self, visual, name):
        """Returns a nice actor"""
        a = serge.actor.Actor('test', name)
        a.visual = visual
        a.setSpatial(0, 0, 20, 30)
        a.setLayerName('main')
        return a

    def testHorizontalBarLayoutFixedWidth(self):
        """testHorizontalBarLayoutFixedWidth: can do a fixed width bar"""
        b = serge.blocks.layout.HorizontalBar('bar', width=100, height=100)
        b.setLayerName('main')
        self.w.addActor(b)
        b.setSpatial(50, 60, 100, 100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        #
        b.addActor(self.getActor(s, 'initial'))
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 110, 20, 30, 'one added')
        #
        self.r.clearSurface()
        b.addActor(self.getActor(s, 'second'))
        b.addActor(self.getActor(s, 'third'))
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 2)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 110, 20, 30, 'three added -  middle')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 66, 110, 20, 30, 'three added - left')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 133, 110, 20, 30, 'three added - right')

    def testBarCanTakeScreenWidthOrHeight(self):
        """testBarCanTakeScreenWidthOrHeight: should be able to default to screen width or height"""
        e = serge.engine.Engine()
        b = serge.blocks.layout.HorizontalBar('bar')
        b.setOrigin(0, 0)
        self.assertEqual([0, 0, 640, 480], b.getSpatial())        
        #
        b = serge.blocks.layout.HorizontalBar('bar', height=100)
        b.setOrigin(0, 0)
        self.assertEqual([0, 0, 640, 100], b.getSpatial())        
        #
        b = serge.blocks.layout.HorizontalBar('bar', width=100)
        b.setOrigin(0, 0)
        self.assertEqual([0, 0, 100, 480], b.getSpatial())        
        
    def testBarShouldSetLayer(self):
        """testBarShouldSetLayer: setting the bar for the layer should set the layer for """
        b = serge.blocks.layout.HorizontalBar('bar', width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        a1.setLayerName('one')
        a2.setLayerName('two')
        #
        # Adding should set the layer
        b.setLayerName('three')
        b.addActor(a1)
        b.addActor(a2)
        self.assertEqual('three', a1.getLayerName())
        self.assertEqual('three', a2.getLayerName())
        #
        # Changing the layer should change all
        b.setLayerName('four')
        self.assertEqual('four', a1.getLayerName())
        self.assertEqual('four', a2.getLayerName())
        
    def testVerticalBarLayoutFixedWidth(self):
        """testVerticalBarLayoutFixedWidth: can do a fixed height bar"""
        b = serge.blocks.layout.VerticalBar('bar', width=100, height=100)
        b.setLayerName('main')
        self.w.addActor(b)
        b.setSpatial(60, 50, 100, 100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        #
        b.addActor(self.getActor(s, 'initial'))
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 110, 100, 20, 30, 'one added')
        #
        self.r.clearSurface()
        b.addActor(self.getActor(s, 'second'))
        b.addActor(self.getActor(s, 'third'))
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 2)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 110, 100, 20, 30, 'three added -  middle')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 110, 66, 20, 30, 'three added - left')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 110, 133, 20, 30, 'three added - right')

    def testAddingToBarAddsToWorld(self):
        """testAddingToBarAddsToWorld: should add to world when adding to a bar"""
        b = serge.blocks.layout.VerticalBar('bar', width=100, height=100)
        self.w.addActor(b)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a = self.getActor(s, 'initial')
        b.addActor(a)
        #
        self.assert_(self.w.hasActor(a))
        
    def testBarCanRenderBackground(self):
        """testBarCanRenderBackground: should be able to set the visual background for a bar"""
        b = serge.blocks.layout.VerticalBar('bar', width=100, height=100, background_colour=(0,255,0,255),
            background_layer='back')
        b.moveTo(110, 100)
        v = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a = serge.actor.Actor('a')
        a.visual = v
        b.addActor(a)
        self.w.addActor(b)
        b.setLayerName('main')
        #        
        s = self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 110, 100, 20, 30, 'red on green', black=(0,255,0,255))
        
        
    def testRemovingFromWorldRemovesItems(self):
        """testRemovingFromWorldRemovesItems: when removing a bar should remove items from the world"""
        b = serge.blocks.layout.VerticalBar('bar', 100, 100)
        self.w.addActor(b)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a = self.getActor(s, 'initial')
        b.addActor(a)
        #
        # Should be there after update
        self.w.updateWorld(0)
        self.assert_(self.w.hasActor(a))
        #
        # Should not be in the world after bar is removed
        self.w.removeActor(b)
        self.w.updateWorld(0)       
        self.assert_(not self.w.hasActor(a))

    def testRemovingContainerBeforeAddingChildren(self):
        """testRemovingContainerBeforeAddingChildren: should be able to remove a container before its children are """
        # If you remove a container after adding items then some of the items
        # will not be in the world yet
        b = serge.blocks.layout.VerticalBar('bar', 100, 100)
        self.w.addActor(b)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255)) 
        a = self.getActor(s, 'initial')
        b.addActor(a)
        #
        self.w.removeActor(b)
        self.assert_(not self.w.hasActor(a))
        self.assert_(not self.w.hasActor(b))
    
        
    def testGridLayoutFixedWidth(self):
        """testGridLayoutFixedWidth: can do a grid with fixed sizes"""
        b = serge.blocks.layout.Grid('grid', size=(1, 1), width=100, height=100)
        b.setLayerName('main')
        self.w.addActor(b)
        b.setSpatial(50, 60, 100, 100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        #
        b.addActor((0, 0), self.getActor(s, 'initial'))
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 1)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 110, 20, 30, 'one added')
        #
        # Now change the size of the grid
        b.setGrid((3, 3))
        self.r.clearSurface()
        for x in range(3):
            for y in range(3):
                b.addActor((x, y), self.getActor(s, '%d-%d' % (x, y)))
        #
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 2)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 110, 20, 30, 'all added -  center middle')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 76, 20, 30, 'all added - center left')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 143, 20, 30, 'all added - center right')
        #
        self.checkRect(self.r.surface, (255, 0, 0, 255), 66, 76, 20, 30, 'all added -  left left')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 133, 143, 20, 30, 'all added - right right')

    def testCanAddSequentiallyToGrid(self):
        """testCanAddSequentiallyToGrid: should be able to add sequentially to a grid"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        b.setLayerName('main')
        self.w.addActor(b)
        b.setSpatial(50, 60, 100, 100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        #
        a1 = b.autoAddActor(self.getActor(s, 'initial'))
        a2 = b.autoAddActor(self.getActor(s, 'initial'))
        a3 = b.autoAddActor(self.getActor(s, 'initial'))
        a4 = b.autoAddActor(self.getActor(s, 'initial'))
        #
        self.assertEqual(a1.x, a3.x)
        self.assertEqual(a2.x, a4.x)
        self.assertEqual(a1.y, a2.y)
        self.assertEqual(a3.y, a4.y)
        self.assertNotEqual(a1.x, a2.x)
        self.assertNotEqual(a1.y, a3.x)
        
    def testFailAddingSequentiallyTooMany(self):
        """testFailAddingSequentiallyTooMany: should fail when adding too many sequentials to a grid"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        b.setLayerName('main')
        self.w.addActor(b)
        b.setSpatial(50, 60, 100, 100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        #
        a1 = b.autoAddActor(self.getActor(s, 'initial'))
        a2 = b.autoAddActor(self.getActor(s, 'initial'))
        a3 = b.autoAddActor(self.getActor(s, 'initial'))
        a4 = b.autoAddActor(self.getActor(s, 'initial'))
        #
        self.assertRaises(serge.blocks.layout.OutOfRange, b.autoAddActor, self.getActor(s, 'initial'))
        
    

    def testTestGridImpliedWidth(self):
        """testTestGridImpliedWidth: grid should work with implied size"""
        b = serge.blocks.layout.Grid('grid', size=(3, 2), height=100)
        b.setOrigin(0, 200)        
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        b.addActor((0,0), self.getActor(s, '00'))
        b.addActor((1,0), self.getActor(s, '10'))
        b.addActor((2,0), self.getActor(s, '20'))
        b.addActor((0,1), self.getActor(s, '01'))
        b.addActor((1,1), self.getActor(s, '11'))
        b.addActor((2,1), self.getActor(s, '21'))
        #
        self.assertEqual(225, b.getActorAt((0,0)).y)
        self.assertEqual(275, b.getActorAt((0,1)).y)
        #
        self.assertEqual(106, int(b.getActorAt((0,0)).x))
        self.assertEqual(320, int(b.getActorAt((1,0)).x))
        self.assertEqual(533, int(b.getActorAt((2,0)).x))
        
    def testFailWhenAddingOutOfRange(self):
        """testFailWhenAddingOutOfRange: should fail if try to add an actor out of range"""
        b = serge.blocks.layout.Grid('grid', size=(1, 1), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        self.assertRaises(serge.blocks.layout.OutOfRange, b.addActor, (1, 1), self.getActor(s, 'initial'))
        self.assertRaises(serge.blocks.layout.OutOfRange, b.addActor, (-1, -1), self.getActor(s, 'initial'))
        
    def testCanAccessActorsByLocation(self):
        """testCanAccessActorsByLocation: should be able to get an actor by its location"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        b.addActor((0, 0), a2)
        #
        self.assertEqual(a1, b.getActorAt((1,1)))
        self.assertEqual(a2, b.getActorAt((0,0)))

    def testCanGetLocationFromCoordinates(self):
        """testCanGetLocationFromCoordinates: should be able to get a location from coordinates"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        x, y = b.getCoords((1,1))
        self.assertEqual((1,1), b.getLocation((x, y)))
        
    def testCanGetLocationFromApproximateCoordinates(self):
        """testCanGetLocationFromApproximateCoordinates: should be able to get location when coords not exact"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        x, y = b.getCoords((1,1))
        self.assertEqual((1,1), b.getLocation((x+10, y+10)))
        self.assertEqual((2,2), b.getLocation((x+40, y+40)))
        x, y = b.getCoords((0,0))
        self.assertEqual((0,0), b.getLocation((x+10, y+10)))
        self.assertEqual((0,0), b.getLocation((x-30, y-20)))
        
            
    
        
    def testAddingToGridAddsToWorld(self):
        """testAddingToGridAddsToWorld: when adding an actor to the grid it should add to the world"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        b.addActor((0, 0), a2)
        self.w.addActor(b)
        #
        self.assert_(self.w.hasActor(a1))        
        self.assert_(self.w.hasActor(a2))
        
    def testRemovingGridShouldRemoveFromWorld(self):
        """testRemovingGridShouldRemoveFromWorld: when removing the grid it should remove actors"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        b.addActor((0, 0), a2)
        self.w.addActor(b)
        self.w.updateWorld(0)
        #
        self.assert_(self.w.hasActor(a1))        
        self.assert_(self.w.hasActor(a2))
        #
        self.w.removeActor(b)
        self.w.updateWorld(0)
        #
        self.assert_(not self.w.hasActor(a1))        
        self.assert_(not self.w.hasActor(a2))
    
    def testAddingToGridShouldSetLayer(self):
        """testAddingToGridShouldSetLayer: actor should have its layer set when adding or setting grid layer"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        b.setLayerName('one')
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        #
        self.assertEqual('one', a1.getLayerName())
        b.setLayerName('two')
        self.assertEqual('two', a1.getLayerName())
        
    def testSettingGridRemovesActors(self):
        """testSettingGridRemovesActors: setting the grid size should remove actors from the world"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        b.addActor((1, 1), a1)
        b.addActor((0, 0), a2)
        self.w.addActor(b)
        self.w.updateWorld(0)
        #
        # Set the grid which, upon update should remove all actors
        # We are then going to add a1 and a3
        b.setGrid((2, 2))
        self.w.updateWorld(0) # Need to do an update here to avoid a duplicate actor on a1
        b.addActor((0,0), a1)
        b.addActor((1,1), a3)
        self.w.updateWorld(0)
        #
        # And now a2 should not be there but the others should
        self.assert_(self.w.hasActor(a1))        
        self.assert_(not self.w.hasActor(a2))
        self.assert_(self.w.hasActor(a3))        

    def testCanMoveGrid(self):
        """testCanMoveGrid: should be able to move an actor from a grid"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        b.addActor((0,0), a1)
        b.moveActor((1,1), a1)        
        self.assertEqual(a1, b.getActorAt((1,1)))
        self.assertRaises(serge.blocks.layout.CellEmpty, b.getActorAt, (0,0))

    def testFailMoveGridOutOfRange(self):
        """testFailMoveGridOutOfRange: should fail when moving actor in grid out of range"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        b.addActor((0,0), a1)
        self.assertRaises(serge.blocks.layout.OutOfRange, b.moveActor, (10,10), a1)        

    def testCanFindActorLocation(self):
        """testCanFindActorLocation: should be able to find the location of an actor"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        b.addActor((1, 1), a1)
        b.addActor((0, 0), a2)
        #
        self.assertEqual((1,1), b.findActorLocation(a1))
        self.assertEqual((0,0), b.findActorLocation(a2))

    def testFailFindActorLocationWhenMissing(self):
        """testFailFindActorLocationWhenMissing: should fail when trying to find a location of an actor that is not there"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        self.assertRaises(serge.blocks.layout.UnknownActor, b.findActorLocation, a1)
        
    def testFailAddToGridThatIsOccupied(self):
        """testFailAddToGridThatIsOccupied: should fail if try to add to occupied grid cell"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        self.assertRaises(serge.blocks.layout.CellOccupied, b.addActor, (1, 1), a2)
        
    def testCanRemoveFromCell(self):
        """testCanRemoveFromCell: should be able to remove from a grid cell"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        self.w.addActor(b)
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        self.w.updateWorld(0)
        #
        b.removeActor((1, 1))        
        b.addActor((1, 1), a2)
        #
        # Quick check that a1 should not be in the world
        self.w.updateWorld(0)
        self.assert_(not self.w.hasActor(a1))
        self.assert_(self.w.hasActor(a2))

    def testCanClearAllTheGrid(self):
        """testCanClearAllTheGrid: should be able to clear the grid"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        self.w.addActor(b)
        a1 = self.getActor(s, 'initial')
        a2 = self.getActor(s, 'initial')
        b.addActor((1, 1), a1)
        self.w.updateWorld(0)
        #
        # Now clear
        b.clearGrid()
        self.w.updateWorld(0)
        #
        self.assert_(not self.w.hasActor(a1))
        self.assert_(not self.w.hasActor(a2))
                
    
    def testFailGettingWhenEmptyCell(self):
        """testFailGettingWhenEmptyCell: should fail if getting from a cell that is empty"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        self.assertRaises(serge.blocks.layout.CellEmpty, b.getActorAt, (0, 0))
        
    def testFailWhenRemovingFromAnEmptyCell(self):
        """testFailWhenRemovingFromAnEmptyCell: should fail when trying to remove an actor when there isn't one there"""
        b = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        self.assertRaises(serge.blocks.layout.CellEmpty, b.removeActor, (0, 0))
        
    def testCanHaveMultiGrid(self):
        """testCanHaveMultiGrid: can have a grid with multiple actors at a location"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        a4 = self.getActor(s, 'a4')
        b.addActor((0,0), a1)
        b.addActor((0,0), a2)
        b.addActor((1,1), a3)
        #
        self.assertEqual(set([a1, a2]), set(b.getActorsAt((0,0))))
        self.assertEqual(set([a3]), set(b.getActorsAt((1,1))))
        #
        # Get Actors at shouldn't raise
        self.assertEqual([], b.getActorsAt((1,0)))
        #
        # Adding out of range raises
        self.assertRaises(serge.blocks.layout.OutOfRange, b.addActor, (5,5), a4)
        self.assertRaises(serge.blocks.layout.OutOfRange, b.addActor, (-1,-1), a4)


    def testGetActorsAtReturnsNewList(self):
        """testGetActorsAtReturnsNewList: should return a new list from get actors at"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        a4 = self.getActor(s, 'a4')
        b.addActor((0,0), a1)
        b.addActor((0,0), a2)
        b.addActor((1,1), a3)
        #
        result = b.getActorsAt((0,0))
        self.assertEqual(set([a1, a2]), set(result))
        result[:] = []        
        self.assertEqual(set([a1, a2]), set(b.getActorsAt((0,0))))
        
    def testCanMoveMultiGrid(self):
        """testCanMoveMultiGrid: should be able to move an actor from a multigrid"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        b.addActor((0,0), a1)
        b.moveActor((1,1), a1)        
        self.assertEqual(set([a1]), set(b.getActorsAt((1,1))))
        self.assertEqual(set([]), set(b.getActorsAt((0,0))))

    def testFailMoveMultiGridOutOfRange(self):
        """testFailMoveMultiGridOutOfRange: should fail when moving actor in grid out of range"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        b.addActor((0,0), a1)
        self.assertRaises(serge.blocks.layout.OutOfRange, b.moveActor, (10,10), a1)        

    def testFailGettingActorAtMultiGrid(self):
        """testFailGettingActorAtMultiGrid: should fail if try to get one actor in a """
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        self.assertRaises(AttributeError, getattr, b, 'getActorAt')        
            
    def testCanFindLocationMulti(self):
        """testCanFindLocationMulti: should be able to find an actor location in a multigrid"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        b.addActor((0,0), a1)
        b.addActor((0,0), a2)
        b.addActor((1,1), a3)
        #
        self.assertEqual((0,0), b.findActorLocation(a1))
        self.assertEqual((0,0), b.findActorLocation(a2))
        self.assertEqual((1,1), b.findActorLocation(a3))
        
    def testFailMultiWhenActorInCell(self):
        """testFailMultiWhenActorInCell: should fail in a multi if actor added to same cell"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        b.addActor((0,0), a1)
        self.assertRaises(serge.blocks.layout.AlreadyInCell, b.addActor, (0,0), a1)
       
    def testCanRemoveActorMulti(self):
        """testCanRemoveActorMulti: should be able to remove one actor from a multi"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        b.addActor((0,0), a1)
        b.addActor((0,0), a2)
        b.addActor((1,1), a3)
        #
        b.removeActor((0,0), a1)
        #
        self.assertEqual(set([a2]), set(b.getActorsAt((0,0))))
        self.assertEqual(set([a3]), set(b.getActorsAt((1,1))))
    
    def testFailRemoveActorMult(self):
        """testFailRemoveActorMult: should fail trying to remove an actor that isn't there"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        b.addActor((0,0), a2)
        #
        self.assertRaises(serge.blocks.layout.UnknownActor, b.removeActor, (0,0), a1)
        self.assertRaises(serge.blocks.layout.UnknownActor, b.removeActor, (1,1), a1)
        
    
    def testCanRemoveActorsMulti(self):
        """testCanRemoveActorsMulti: should be able to remove all actors from a multi"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        b.addActor((0,0), a1)
        b.addActor((0,0), a2)
        b.addActor((1,1), a3)
        #
        b.removeActors((0,0))
        #
        self.assertEqual([], b.getActorsAt((0,0)))
        self.assertEqual(set([a3]), set(b.getActorsAt((1,1))))

    def testRemoveActorsMultiRemovesFromWorld(self):
        """testRemoveActorsMultiRemovesFromWorld: should remove actors from world when removing actors"""
        b = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        a1 = self.getActor(s, 'a1')
        a2 = self.getActor(s, 'a2')
        a3 = self.getActor(s, 'a3')
        b.addActor((0,0), a1)
        b.addActor((0,0), a2)
        b.addActor((1,1), a3)
        self.w.addActor(b)
        self.assertEqual(True, self.w.hasActor(a1))
        self.assertEqual(True, self.w.hasActor(a2))
        #
        b.removeActors((0,0))
        #
        self.assertEqual(False, self.w.hasActor(a1))
        self.assertEqual(False, self.w.hasActor(a2))
        
    def testCanAddWithLayerName(self):
        """testCanAddWithLayerName: should be able to add with a layer name"""
        v = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        s = self.getActor(v, 'a1')
        b1 = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        b2 = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        b3 = serge.blocks.layout.VerticalBar('bar', 100, 100)
        b4 = serge.blocks.layout.HorizontalBar('bar', 100, 100)
        #
        b1.addActor((0,0), s, '1')
        self.assertEqual('1', s.getLayerName())
        b2.addActor((0,0), s, '2')
        self.assertEqual('2', s.getLayerName())
        b3.addActor(s, '3')
        self.assertEqual('3', s.getLayerName())
        b4.addActor(s, '4')
        self.assertEqual('4', s.getLayerName())
            
    def testAddActorReturnsActor(self):
        """testAddActorReturnsActor: add actor should return the actor"""
        v = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        s = self.getActor(v, 'a1')
        b1 = serge.blocks.layout.MultiGrid('grid', size=(2, 2), width=100, height=100)
        b2 = serge.blocks.layout.Grid('grid', size=(2, 2), width=100, height=100)
        b3 = serge.blocks.layout.VerticalBar('bar', 100, 100)
        b4 = serge.blocks.layout.HorizontalBar('bar', 100, 100)
        #
        self.assertEqual(s, b1.addActor((0,0), s))
        self.assertEqual(s, b2.addActor((0,0), s))
        self.assertEqual(s, b3.addActor(s))
        self.assertEqual(s, b4.addActor(s))
        
    def testMovingBarShouldMoveAll(self):
        """testMovingBarShouldMoveAll: should move child actors when we move the overall container"""
        b = serge.blocks.layout.HorizontalBar('bar', width=100, height=100)
        b.setLayerName('main')
        self.w.addActor(b)
        b.moveTo(0, 0)
        s = serge.blocks.visualblocks.Rectangle((20, 30), (255,0,0,255))                
        #
        b.addActor(self.getActor(s, 'initial'))
        b.addActor(self.getActor(s, 'second'))
        b.addActor(self.getActor(s, 'third'))
        b.moveTo(100, 110)
        self.w.updateWorld(0)
        self.w.renderTo(self.r, 0)
        self.r.render()
        self.save(self.r, 2)
        self.checkRect(self.r.surface, (255, 0, 0, 255), 100, 110, 20, 30, 'three added -  middle')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 66, 110, 20, 30, 'three added - left')
        self.checkRect(self.r.surface, (255, 0, 0, 255), 133, 110, 20, 30, 'three added - right')
        
        
class TestEffectsBlocks(unittest.TestCase, VisualTester):
    """Tests for the EffectsBlocks"""

    def setUp(self):
        """Set up the tests"""
        self.w = serge.world.World('test')
        self.z1 = serge.zone.Zone()
        self.z1.setSpatial(0, 0, 1000, 1000)
        self.z1.active = True
        self.w.addZone(self.z1)
        

    def tearDown(self):
        """Tear down the tests"""        

    def testCanDoFade(self):
        """testCanDoFade: should be able to do a fade"""
        a = TestActor()
        self.z1.addActor(a)
        fade = serge.blocks.effects.AttributeFade(a, 'counter', start=110, end=10, decay=5) 
        self.w.addActor(fade)
        #
        self.w.updateWorld(0)
        self.assertEqual(110, a.counter)
        #
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        self.w.updateWorld(4000)
        self.assertEqual(10, a.counter)
        self.w.updateWorld(1000)
        self.assertEqual(10, a.counter)
        #
        # Effect should have been removed
        self.assert_(fade not in self.w.getActors())
        
    def testCanRestartFade(self):
        """testCanRestartFade: should be able to stop and restart a fade"""
        a = TestActor()
        self.z1.addActor(a)
        fade = serge.blocks.effects.AttributeFade(a, 'counter', start=110, end=10, decay=5) 
        self.w.addActor(fade)
        #
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        # Pause and nothing should happen
        fade.pause()
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        # Unpause and it should carry on
        fade.unpause()
        self.w.updateWorld(1000)
        self.assertEqual(70, a.counter)
        #
        # Restart and should go back
        fade.restart()
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        # Go to the end
        fade.finish()
        self.w.updateWorld(1000)
        self.assertEqual(10, a.counter)
        
        
    def testCanPersistAnEffect(self):
        """testCanPersistAnEffect: should be able to keep an effect persistent"""
        a = TestActor()
        self.z1.addActor(a)
        fade = serge.blocks.effects.AttributeFade(a, 'counter', start=110, end=10, decay=5, persistent=True) 
        self.w.addActor(fade)
        #
        self.w.updateWorld(1e6)
        self.assertEqual(10, a.counter)
        self.assert_(fade in self.w.getActors())
        
    def testCanDoMethodCall(self):
        """testCanDoMethodCall: should be able to do a simple method call"""
        a = TestActor()
        self.z1.addActor(a)
        fade = serge.blocks.effects.MethodCallFade(a.setCounter, start=110, end=10, decay=5, persistent=True) 
        self.w.addActor(fade)
        #
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        # Pause and nothing should happen
        fade.pause()
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        # Unpause and it should carry on
        fade.unpause()
        self.w.updateWorld(1000)
        self.assertEqual(70, a.counter)
        #
        # Restart and should go back
        fade.restart()
        self.w.updateWorld(1000)
        self.assertEqual(90, a.counter)
        #
        # Go to the end
        fade.finish()
        self.w.updateWorld(1000)
        self.assertEqual(10, a.counter)
       
    def testCanHaveCompletedMethod(self):
        """testCanHaveCompletedMethod: should be able to callback a method when done"""
        a = TestActor()
        self.z1.addActor(a)
        fade = serge.blocks.effects.MethodCallFade(a.setCounter, start=110, end=10, decay=5, done=a.setDone) 
        self.w.addActor(fade)
        #
        # Should not be called initially
        self.w.updateWorld(1000)
        self.assertEqual([0,None], a.done)  
        #
        # When done should be called      
        self.w.updateWorld(9000)
        self.assertEqual([1,fade], a.done)        
        #
        # Should only be called once
        self.w.updateWorld(9000)
        self.assertEqual([1,fade], a.done)        

    def testCanDoAccelerationFade(self):
        """testCanDoAccelerationFade: can have an accelerated fade"""
        a = TestActor()
        self.z1.addActor(a)
        b = TestActor()
        self.z1.addActor(b)
        fade = serge.blocks.effects.MethodCallFade(a.setCounter, start=10, end=110, decay=8, persistent=True, motion='linear') 
        acc = serge.blocks.effects.MethodCallFade(b.setCounter, start=10, end=110, decay=8, persistent=True, motion='accelerated') 
        self.w.addActor(fade)
        self.w.addActor(acc)
        #
        # Linear should stay ahead of accelerated until half way
        self.w.updateWorld(1000)
        self.assert_(a.counter > b.counter, 'Linear should have been further %d, %d' % (a.counter, b.counter))
        #
        # Should be equal at half way
        self.w.updateWorld(3000)
        self.assertEqual(a.counter, b.counter)
        #
        # Accelerated should be ahead now
        self.w.updateWorld(1000)
        self.assert_(a.counter < b.counter, 'Accelerated should have been further %d, %d' % (a.counter, b.counter))
        #
        # Should be equal at end
        self.w.updateWorld(3000)
        self.assertEqual(a.counter, b.counter)
        
    def testFailBadMotion(self):
        """testFailBadMotion: should fail if get a bad motion type"""
        a = TestActor()
        self.assertRaises(serge.blocks.effects.InvalidMotion,
            serge.blocks.effects.MethodCallFade, a.setCounter, start=110, end=10, decay=8, persistent=True, motion='bad') 
       
    def testCanDoAPause(self):
        """testCanDoAPause: should be able to do a pause"""
        a = TestActor()
        self.z1.addActor(a)
        pause = serge.blocks.effects.Pause(time=10, done=a.setDone)  
        self.w.addActor(pause)
        #
        # Should not be called initially
        self.w.updateWorld(1000)
        self.assertEqual([0,None], a.done)  
        #
        # When done should be called      
        self.w.updateWorld(9000)
        self.assertEqual([1,pause], a.done)        
        #
        # Should only be called once
        self.w.updateWorld(9000)
        self.assertEqual([1,pause], a.done)        
        
    
class TestScoreBlocks(unittest.TestCase):
    """Tests for the Score Blocks"""

    def setUp(self):
        """Set up the tests"""
        
        
    def tearDown(self):
        """Tear down the tests"""    

    def testCanAddHighScore(self):
        """testCanAddHighScore: should be able to add a high score"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test')
        t.addScore('test', 'bob', 1)
        
    def testCanGetHighScoreTable(self):
        """testCanGetHighScoreTable: should be able to get the high score table"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test')
        t.addScore('test', 'bob', 1)
        s = t.getCategory('test')
        self.assertEqual([('bob', 1)], s)
        
    def testFailIfGetBadScoreTable(self):
        """testFailIfGetBadScoreTable: should fail if you try to get a bad score table"""
        t = serge.blocks.scores.HighScoreTable()
        self.assertRaises(serge.blocks.scores.BadCategory, t.getCategory, 'test')
            
    def testCanResetHighScores(self):
        """testCanResetHighScores: should be able to reset the high scores"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test')
        t.addScore('test', 'bob', 1)
        t.resetTable()
        self.assertRaises(serge.blocks.scores.BadCategory, t.getCategory, 'test')

    def testCanResetCategory(self):
        """testCanResetCategory: should be able to reset one category"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1')
        t.addCategory('test2')
        t.addScore('test1', 'bob', 1)
        t.addScore('test2', 'bob', 1)
        t.resetCategory('test1')
        #
        self.assertEqual([], t.getCategory('test1'))
        self.assertNotEqual([], t.getCategory('test2'))
            
    def testScoresCanLimitAndSort(self):
        """testScoresCanLimitAndSort: the high score table should be able to sort and be limited"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1', number=5, sort_columns=[1], directions=['ascending'])
        t.addCategory('test2', number=5, sort_columns=[2], directions=['ascending'])
        t.addCategory('test3', number=5, sort_columns=[1], directions=['descending'])
        t.addCategory('test4', number=1, sort_columns=[1], directions=['ascending'])
        #
        values = (('a', 1, 5), ('b', 2, 4), ('c', 3, 3), ('g', -1, -1), ('h', -2, -2), ('d', 4, 2), ('e', 5, 1))
        for n, v, o in values:
            t.addScore('test1', n, v, o)
            t.addScore('test2', n, v, o)
            t.addScore('test3', n, v, o)
            t.addScore('test4', n, v, o)
        #
        self.assertEqual([('e', 5, 1), ('d', 4, 2), ('c', 3, 3), ('b', 2, 4), ('a', 1, 5)], t.getCategory('test1'))
        self.assertEqual([('a', 1, 5), ('b', 2, 4),  ('c', 3, 3), ('d', 4, 2), ('e', 5, 1)], t.getCategory('test2'))
        self.assertEqual([('h', -2, -2), ('g', -1, -1), ('a', 1, 5), ('b', 2, 4),  ('c', 3, 3)], t.getCategory('test3'))
        self.assertEqual([('e', 5, 1)], t.getCategory('test4'))  

    def testMultipleSort(self):
        """testMultipleSort: the high score table should be able to sort on multiple columns"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1', number=5, sort_columns=(1, 2), directions=('descending', 'ascending'))
        t.addCategory('test2', number=5, sort_columns=(2, 1), directions=('descending', 'ascending'))
        #
        values = (('a', 2, 5), ('b', 2, 4), ('c', 3, 3), ('h', 1, 5), ('g', 1, 3))
        for n, v, o in values:
            t.addScore('test1', n, v, o)
            t.addScore('test2', n, v, o)
        #
        self.assertEqual([('h', 1, 5), ('g', 1, 3), ('a', 2, 5), ('b', 2, 4), ('c', 3, 3)], t.getCategory('test1'))
        self.assertEqual([('c', 3, 3), ('g', 1, 3), ('b', 2, 4), ('a', 2, 5), ('h', 1, 5)], t.getCategory('test2'))
        
    def testCanSerializeHighScoreTable(self):
        """testCanSerializeHighScoreTable: should be able to serialize and deserialize a high score table"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test')
        t.addScore('test', 'bob', 1)
        #
        x = serge.serialize.Serializable.fromString(t.asString())
        s = x.getCategory('test')
        self.assertEqual([('bob', 1)], s)
        
    def testFailInvalidSort(self):
        """testFailInvalidSort: should fail if the sort is invalid"""
        t = serge.blocks.scores.HighScoreTable()
        self.assertRaises(serge.blocks.scores.InvalidSort, t.addCategory, 'test1', number=5, sort_columns=1, directions='blahblah')
        
    def testFailInvalidColumns(self):
        """testFailInvalidColumns: should fail if the sort column is more than the number of columns"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1', number=5, sort_columns=[2], directions=['ascending'])
        self.assertRaises(serge.blocks.scores.InvalidSortColumn, t.addScore, 'test1', 10)
    
    def testFailInvalidCategoryForAdding(self):
        """testFailInvalidCategoryForAdding: should fail if add score for invalid category"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1')
        self.assertRaises(serge.blocks.scores.BadCategory, t.addScore, 'test2', 10)
        
    def testFailNoData(self):
        """testFailNoData: should fail if do not provide enough data"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1')
        self.assertRaises(TypeError, t.addScore, 'test2')
        
    def testFailDuplicateCategoryName(self):
        """testFailDuplicateCategoryName: should fail if add a duplicate category"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test1')
        self.assertRaises(serge.blocks.scores.DuplicateCategory, t.addCategory, 'test1')
        
    def testCanSeeCurrentPosition(self):
        """testCanSeeCurrentPosition: should be able to retrieve the current position"""
        t = serge.blocks.scores.HighScoreTable()
        t.addCategory('test', number=5, sort_columns=[1])
        #
        # Adding lower and lower should increase the number
        for i in range(5):
            self.assertEqual(i+1, t.addScore('test', 'bob', 5-i))
        #
        # Adding another should not be on the table
        self.assertEqual(None, t.addScore('test', 'bob', 0))
        #
        # Adding a higher one should be
        self.assertEqual(1, t.addScore('test', 'bob', 10))
                      
       
class TestThemeBlocks(unittest.TestCase):
    """Tests for the ThemeBlocks"""

    base_theme = '''{
                'schema' : ('', {
                    'name' : 'one',
                    'num' : 12,
                    'colour' : (1,2,3),
                }),
                'aaa' : ('schema', {
                }),
                'bbb' : ('schema', {
                    'name' : 'two',
                }),
                'ccc' : ('schema', {
                    'name' : 'three',
                    'num' : 36,
                    'colour' : (100,200,300),
                }),
                'ddd' : ('ccc', {
                    'name' : 'four',
                }),
                '__default__' : 'bbb',
            }'''

    def setUp(self):
        """Set up the tests"""
        self.b = eval(self.base_theme)
        self.m = serge.blocks.themes.Manager()
        
    def tearDown(self):
        """Tear down the tests"""         
        
    def testCanLoadSingleTheme(self):
        """testCanLoadSingleTheme: should be able to load a single theme"""
        self.m.loadFrom(self.base_theme)
        
    def testCanLoadMultipleThemes(self):
        """testCanLoadMultipleThemes: should be able to load multiple themes"""
        self.m.loadFrom(self.base_theme)
        
    def testCanSelectTheme(self):
        """testCanSelectTheme: should be able to select a theme"""
        self.m.loadFrom(self.base_theme)
        self.m.selectTheme('bbb')
        self.assertEqual('two', self.m.getProperty('name'))

    def testCanCheckIfThemeExists(self):
        """testCanCheckIfThemeExists: should be able to check if a theme exists"""
        self.m.loadFrom(self.base_theme)
        self.assertTrue(self.m.hasTheme('bbb'))        
        self.assertTrue(self.m.hasTheme('ddd'))
        self.assertFalse(self.m.hasTheme('not there'))
                
    def testFailSelectMissingTheme(self):
        """testFailSelectMissingTheme: should fail when selecting a missing theme"""
        self.m.loadFrom(self.base_theme)
        self.assertRaises(serge.blocks.themes.ThemeNotFound, self.m.selectTheme, 'xxx')
        
    def testFailLoadFromMissingFile(self):
        """testFailLoadFromMissingFile: should fail when loading a missing theme file"""
        self.assertRaises(serge.blocks.themes.BadThemeFile, self.m.loadFromFile, 'no such theme')
        
    def testCanCascadeThemes(self):
        """testCanCascadeThemes: should be able to cascade one theme from another"""
        self.m.loadFrom(self.base_theme)
        self.m.selectTheme('ddd')
        self.assertEqual('four', self.m.getProperty('name'))
        self.assertEqual(36, self.m.getProperty('num'))
        
    def testCanUseDefaults(self):
        """testCanUseDefaults: themes should be able to use defaults"""
        self.m.loadFrom(self.base_theme)
        self.m.selectTheme('aaa')
        self.assertEqual('one', self.m.getProperty('name'))
        self.assertEqual(12, self.m.getProperty('num'))
    
    def testThereIsADefaultTheme(self):
        """testThereIsADefaultTheme: there should be a default theme"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual('two', self.m.getProperty('name'))
        self.assertEqual(12, self.m.getProperty('num'))
        
    def testThemeSupportsString(self):
        """testThemeSupportsString: themes should support strings"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual('two', self.m.getProperty('name'))
        
    def testThemeSupportsNumbers(self):
        """testThemeSupportsNumbers: themes should support numbers"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual(12, self.m.getProperty('num'))
        
    def testThemeSupportsLists(self):
        """testThemeSupportsLists: themes should support lists and tuples"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual((1,2,3), self.m.getProperty('colour'))
        
    def testFailWithBadSchema(self):
        """testFailWithBadSchema: should fail with a bad schema for the data"""
        self.assertRaises(serge.blocks.themes.BadThemeDefinition, self.m.loadFrom, '{')
        
    def testFailWithMissingDefault(self):
        """testFailWithMissingDefault: should fail with a schema missing a default"""
        self.assertRaises(serge.blocks.themes.MissingDefault, self.m.loadFrom, '{"s": ("", {})}')
    
    def testFailWithMissingSchema(self):
        """testFailWithMissingSchema: should fail with a schema missing a default"""
        self.assertRaises(serge.blocks.themes.MissingSchema, self.m.loadFrom, '{"s": ("s", {}), "__default__":"a"}')
        
    def testFailBadInheritance(self):
        """testFailBadInheritance: should fail if base classes are not ligned up"""
        self.assertRaises(serge.blocks.themes.BadInheritance, self.m.loadFrom, '{"s": ("", {}), "x": ("b", {}), "__default__":"a" }')

    def testCanInitFromDictionary(self):
        """testCanInitFromDictionary: should be able to init from a dictionary"""
        self.m.load(self.b)
        self.assertEqual('two', self.m.getProperty('name'))
        self.assertRaises(serge.blocks.themes.BadInheritance, self.m.load, {"s": ("", {}), "x": ("b", {}), "__default__":"a" })
        
    def testFailPropertyNotFound(self):
        """testFailPropertyNotFound: should fail when trying to find something not there"""
        self.m.loadFrom(self.base_theme)
        self.assertRaises(serge.blocks.themes.PropertyNotFound, self.m.getProperty, 'not there')

    def testCanSetThemeProperty(self):
        """testCanSetThemeProperty: should be able to set theme property"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual('one', self.m.getProperty('name', 'schema'))        
        self.m.setProperty('name', 'haha', from_theme='schema')
        self.assertEqual('haha', self.m.getProperty('name', 'schema'))        
        self.assertEqual('haha', self.m.getProperty('name', 'aaa'))        
                
    def testCanSetThemePropertyDefault(self):
        """testCanSetThemePropertyDefault: should be able to set a property in default theme"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual('two', self.m.getProperty('name'))        
        self.m.setProperty('name', 'haha')
        self.assertEqual('one', self.m.getProperty('name', 'schema'))        
        self.assertEqual('haha', self.m.getProperty('name'))        
    
    def testCanUpdateFromString(self):
        """testCanUpdateFromString: should be able to update from a string"""
        self.m.loadFrom(self.base_theme)
        self.assertEqual('two', self.m.getProperty('name'))
        self.assertRaises(serge.blocks.themes.PropertyNotFound, self.m.getProperty, 'x')
        #
        self.m.updateFromString('name="bob",x=123')
        self.assertEqual('bob', self.m.getProperty('name'))
        self.assertEqual(123, self.m.getProperty('x'))
            
    def testFailUpdateBadString(self):
        """testFailUpdateBadString: should fail when updating from a bad string"""
        self.assertRaises(serge.blocks.themes.InvalidFormat, self.m.updateFromString, 'name:"bob",x=123')
        
    def testCanGetThemeWithDefault(self):
        """testCanGetThemeWithDefault: should be able to get a sub theme"""
        self.m.loadFrom(self.base_theme)
        t = self.m.getTheme('ddd')
        self.assertEqual('four', t.getProperty('name'))
        self.assertEqual(36, t.getProperty('num'))
        
    def testFailGetThemeWithDefault(self):
        """testFailGetThemeWithDefault: should fail when getting a sub theme that doesn't exist"""
        self.m.loadFrom(self.base_theme)
        self.assertRaises(serge.blocks.themes.ThemeNotFound, self.m.getTheme, 'dddaaa')
        
    def testCanGetPropertyValueWithDefault(self):
        """testCanGetPropertyValueWithDefault: should be able to get a property value with a default"""
        self.m.loadFrom(self.base_theme)
        self.assertRaises(serge.blocks.themes.PropertyNotFound, self.m.getProperty, 'x')
        self.assertEqual(123, self.m.getPropertyWithDefault('x', 123))
        
        
class TestVisualEffects(unittest.TestCase, VisualTester):
    """Tests for the VisualEffects"""

    def setUp(self):
        """Set up the tests"""
        self.r = serge.render.Renderer()
        self.l = serge.render.Layer('main', 0)
        self.r.addLayer(self.l)
        serge.visual.Register.clearItems()

        
    def tearDown(self):
        """Tear down the tests"""

    def testCanDoShadow(self):
        """testCanDoShadow: should be able to get a shadow"""
        s = serge.blocks.visualblocks.Rectangle((10, 12), (255,0,0,255))
        s.renderTo(0, self.l.getSurface(), (50, 60))
        self.save(self.l, 1)
        shadow = serge.blocks.visualeffects.Shadow(self.l.getSurface(), (0, 255, 0, 127))
        self.l.clearSurface()
        shadow.renderTo(0, self.l.getSurface(), (0, 0))
        self.save(self.l, 2)
        self.save(shadow, 3)
        self.checkRect(self.l.getSurface(), (0, 255, 0, 127), 55, 66, 10, 12, 'shadow', check_alpha=True, black=(0,255,0,0))
       
    def testCanDoShadowLayer(self):
        """testCanDoShadowLayer: should be able to do a shadow layer"""
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        #
        # Create the world to play in
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        green = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'green', 'front', (75, 75))
        #
        # Get rendering surfaces
        r = e.getRenderer()
        l1 = serge.blocks.visualeffects.ShadowLayer('front', 2, (255,0,0,127), (10,10))
        r.addLayer(l1)
        #
        # Do the rendering
        r.preRender()
        w.renderTo(r, 0)
        r.render()
        self.save(r, 1)
        #
        # Check that green is in front overall
        self.assertEqual((0,255,0,255), self.r.getSurface().get_at((75, 75)))
        self.assertEqual((0,255,0,255), self.r.getSurface().get_at((99, 99)))
        self.assertEqual((126, 0, 0, 255), self.r.getSurface().get_at((103, 103)))
        

class TestDirections(unittest.TestCase):
    """Tests for the Directions"""

    def setUp(self):
        """Set up the tests"""
        
        
    def tearDown(self):
        """Tear down the tests"""     
       
    def testCanGetCardinal(self):
        """testCanGetCardinal: should be able to get cardinal directions"""
        for d, e in (('n', (0,-1)), ('ne', (1,-1)), ('e', (1,0)), ('se', (1,1)), ('s', (0,1)), ('sw', (-1,1)), 
                ('w', (-1,0)), ('nw', (-1, -1))):
            self.assertEqual(e, serge.blocks.directions.getVectorFromCardinal(d))

    def testCanGetCardinalNotUnity(self):
        """testCanGetCardinalNotUnity: should be able to get cardinal directions when not unit vectors"""
        for e, v in (('n', (0,-5)), ('ne', (5,-5)), ('e', (5,0)), ('se', (5,5)), ('s', (0,5)), ('sw', (-5,5)), 
                ('w', (-5,0)), ('nw', (-5, -5))):
            self.assertEqual(e, serge.blocks.directions.getCardinalFromVector(v))
        
    def testCanGetReverseCardinal(self):
        """testCanGetReverseCardinal: should be able to get reverse cardinal"""
        for d, e in (('n', (0,-1)), ('ne', (1,-1)), ('e', (1,0)), ('se', (1,1)), ('s', (0,1)), ('sw', (-1,1)), 
                ('w', (-1,0)), ('nw', (-1, -1))):
            self.assertEqual(d, serge.blocks.directions.getCardinalFromVector(e))
        
    def testCanGetOppositeCardinal(self):
        """testCanGetOppositeCardinal: should be able to get the opposite cardinal"""
        for d in serge.blocks.directions.getCardinals():
            v = serge.blocks.directions.getVectorFromCardinal(d)
            o = serge.blocks.directions.getVectorFromCardinal(serge.blocks.directions.getOppositeCardinal(d))
            self.assertEqual((0,0), (v[0]+o[0], v[1]+o[1]))
        
    def testCanGetOppositeVector(self):
        """testCanGetOppositeVector: should be able to get the opposite vector"""
        for d in serge.blocks.directions.getCardinals():
            v = serge.blocks.directions.getVectorFromCardinal(d)
            o = serge.blocks.directions.getOppositeVector(v)
            self.assertEqual((0,0), (v[0]+o[0], v[1]+o[1]))
            
        
class TestAchievements(unittest.TestCase):
    """Tests for the Achievements"""

    def setUp(self):
        """Set up the tests"""
        self.a = serge.blocks.achievements.AchievementManager()
        
    def tearDown(self):
        """Tear down the tests"""     

    def testCanRegisterSimpleAchievement(self):
        """testCanRegisterSimpleAchievement: should be able to register a simple achievement"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        self.a.registerAchievement(ach)
        
    def testFailRegisterDuplicateAchievement(self):
        """testFailRegisterDuplicateAchievement: should fail if register an achievement that is already registered"""
        ach1 = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        ach2 = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        self.a.registerAchievement(ach1)
        self.assertRaises(serge.blocks.achievements.DuplicateAchievement, self.a.registerAchievement, ach2)
                
    def testCanRegisterComplexAchievement(self):
        """testCanRegisterComplexAchievement: should be able to register a complex achievement"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=_achTest, test_type='test')
        self.a.registerAchievement(ach)
            
    def testCanGetListOfAchievements(self):
        """testCanGetListOfAchievements: should be able to get the list of achievements"""
        ach1 = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        ach2 = serge.blocks.achievements.Achievement(name='two', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        self.a.registerAchievement(ach1)
        self.a.registerAchievement(ach2)
        self.assertEqual(set([ach1, ach2]), set(self.a.getAchievements()))

    def testAchievementsListIsOrderedByAdding(self):
        """testAchievementsListIsOrderedByAdding: order of adding achievements should be retained"""
        ach1 = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        ach2 = serge.blocks.achievements.Achievement(name='two', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        self.a.registerAchievement(ach1)
        self.a.registerAchievement(ach2)
        self.assertEqual([ach1, ach2], self.a.getAchievements())
       
    
        
    def testCanSerializeAchievements(self):
        """testCanSerializeAchievements: should be able to serialize the achievements"""
        ach1 = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition_string='x : x>10', test_type='test1')
        ach2 = serge.blocks.achievements.Achievement(name='two', description='description', badge='badge', secret=False, 
            condition_string='x : x>10', test_type='test2')
        self.a.registerAchievement(ach1)
        self.a.registerAchievement(ach2)
        self.a.makeReport('test1', x=11)
        #
        b = serge.serialize.Serializable.fromString(self.a.asString())
        self.assertEqual('one', b.getAchievements()[0].name)
        self.assertEqual('two', b.getAchievements()[1].name)
        self.assertTrue(b.getAchievements()[0].isMet())
        self.assertFalse(b.getAchievements()[1].isMet())
        #
        b.makeReport('test2', x=9)
        self.assertFalse(b.getAchievements()[1].isMet())
        b.makeReport('test2', x=11)
        self.assertTrue(b.getAchievements()[1].isMet())

    def testCanSerializeComplexAchievements(self):
        """testCanSerializeComplexAchievements: should be able to serialize complex achievements"""
        ach1 = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=_achTest, test_type='test1')
        ach2 = serge.blocks.achievements.Achievement(name='two', description='description', badge='badge', secret=False, 
            condition=_achTest, test_type='test2')
        self.a.registerAchievement(ach1)
        self.a.registerAchievement(ach2)
        self.a.makeReport('test1', x=11)
        #
        b = serge.serialize.Serializable.fromString(self.a.asString())
        self.assertEqual('one', b.getAchievements()[0].name)
        self.assertEqual('two', b.getAchievements()[1].name)
        self.assertTrue(b.getAchievements()[0].isMet())
        self.assertFalse(b.getAchievements()[1].isMet())
        #
        b.makeReport('test2', x=9)
        self.assertFalse(b.getAchievements()[1].isMet())
        b.makeReport('test2', x=11)
        self.assertTrue(b.getAchievements()[1].isMet())
        
    def testCanCheckForAchievementMet(self):
        """testCanCheckForAchievementMet: should be able to check an achievement is met"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        self.a.registerAchievement(ach)
        #
        self.a.makeReport('test', x=0)
        self.assertFalse(ach.isMet())
        self.a.makeReport('test', x=20)
        self.assertTrue(ach.isMet())
        self.assertEqual(int(time.time()), int(ach.time))
        
    def testFailCheckAchievementMissingParam(self):
        """testFailCheckAchievementMissingParam: should fail if achievement check fails"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x, y : x>10, test_type='test')
        self.a.registerAchievement(ach)
        #
        self.assertRaises(serge.blocks.achievements.BadReport, self.a.makeReport, 'test', x=0)
 
    def testFailCheckAchievementBadTest(self):
        """testFailCheckAchievementBadTest: should fail if try to check achievement with bad test type"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x, y : x>10, test_type='test')
        self.a.registerAchievement(ach)
        #
        self.assertRaises(serge.blocks.achievements.BadTestType, self.a.makeReport, 'testxxx', x=0)
        
    def testOnceMetAchievementShouldStayMet(self):
        """testOnceMetAchievementShouldStayMet: achievement should not go away if condition goes away"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition=lambda x : x>10, test_type='test')
        self.a.registerAchievement(ach)
        #
        self.a.makeReport('test', x=0)
        self.a.makeReport('test', x=20)
        self.a.makeReport('test', x=0)
        self.assertTrue(ach.isMet())
        
    def testCanUseConditionString(self):
        """testCanUseConditionString: should be able to use condition string"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition_string='x : x>10', test_type='test1')
        self.a.registerAchievement(ach)
        #
        self.a.makeReport('test1', x=9)
        self.assertFalse(ach.isMet())
        self.a.makeReport('test1', x=11)
        self.assertTrue(ach.isMet())
        
    def testFailUseBadConditions(self):
        """testFailUseBadConditions: should fail if using bad conditions"""
        self.assertRaises(serge.blocks.achievements.BadCondition,
            serge.blocks.achievements.Achievement, name='one', description='description', badge='badge', secret=False, 
                test_type='test1')
        self.assertRaises(serge.blocks.achievements.BadCondition,
            serge.blocks.achievements.Achievement, name='one', description='description', badge='badge', secret=False, 
                test_type='test1', condition_string='x : x>10', condition=_achTest)
        self.assertRaises(serge.blocks.achievements.BadCondition,
            serge.blocks.achievements.Achievement, name='one', description='description', badge='badge', secret=False, 
                test_type='test1', condition_string='x : x>')

    def testAchievementMetRaisesAnEvent(self):
        """testAchievementMetRaisesAnEvent: should raise an event when achievement is met"""
        ach = serge.blocks.achievements.Achievement(name='one', description='description', badge='badge', secret=False, 
            condition_string='x : x>10', test_type='test1')
        self.a.registerAchievement(ach)
        self.a.linkEvent(serge.blocks.achievements.E_ACHIEVEMENT_MET, self._achMet)        
        #
        self._done = False
        self.a.makeReport('test1', x=9)
        self.assertFalse(self._done)
        self.a.makeReport('test1', x=11)
        self.assertTrue(self._done)
        self.assertEqual(ach, self._a)
        self._done = False
        self.a.makeReport('test1', x=11)
        self.assertFalse(self._done)

    def _achMet(self, obj, arg):
        """Met an achievement"""
        self._done = True
        self._a = obj

def _achTest(x):
    """Test for achievement condition"""
    return x > 10

       
       
       

        
class TestActor(serge.actor.Actor):
    def __init__(self):
        """Initialise"""
        super(TestActor, self).__init__('', '')
        self.counter = 0
        self.action = None
        self.done = [0,None]

    def setCounter(self, c):
        """Set the counter"""
        self.counter = c    

    def setDone(self, effect):
        """Set the done"""
        self.done = [self.done[0]+1, effect]
        
 
if __name__ == '__main__':
    unittest.main()
