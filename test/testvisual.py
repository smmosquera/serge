"""Tests for Visual items"""

import unittest
import os
import pygame
import math
import time

from helper import *

import serge.visual
import serge.render
import serge.actor 
import serge.world
import serge.zone
import serge.physical
import serge.blocks.visualblocks

pygame.init()


class TestVisual(unittest.TestCase, VisualTester):
    """Tests for the Visual"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        serge.visual.Fonts.clearItems()
        
    def tearDown(self):
        """Tear down the tests"""

    
    ### Registering ###
    
    def testCanRegisterASprite(self):
        """testCanRegisterASprite: should be able to register a sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))

    def testCanRegisterFilesFromPattern(self):
        """testCanRegisterFilesFromPattern: should be able to register all with a pattern"""
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItemsFromPattern(r'allrect\d\.png')
        for i in (1, 2, 3, 4):
            _ = serge.visual.Register.getItem('allrect%d' % i)
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Register.getItem, 'allrect')
        
    def testCanRegisterMultipleFromTiles(self):
        """testCanRegisterMultipleFromTiles: should be able to register multiple sprites from a tile"""
        r = serge.render.Renderer()
        serge.visual.Register.registerMultipleItems(['green', 'red','blue', 'white'], p('allrect.png'), 4) 
        s = serge.visual.Register.getItem('green')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        #
        s = serge.visual.Register.getItem('red')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,0,0,255), 50, 50, 50, 50, 'red')
        #
        s = serge.visual.Register.getItem('blue')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,0,255,255), 50, 50, 50, 50, 'blue')
        #
        s = serge.visual.Register.getItem('white')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255,255,255), 50, 50, 50, 50, 'white')

    def testCanRegisterMultipleFromRows(self):
        """testCanRegisterMultipleFromRows: should be able to do multiple sprites in more than one row"""
        r = serge.render.Renderer()
        serge.visual.Register.registerMultipleItems(['green', 'red', 'blue', 'blue2'], p('multi2.png'), 2, 2) 
        s = serge.visual.Register.getItem('green')
        s.renderTo(0, r.getSurface(), (25,25))
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        #
        s = serge.visual.Register.getItem('red')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,0,0,255), 50, 50, 50, 50, 'red')
        #
        s = serge.visual.Register.getItem('blue')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,0,255,255), 50, 50, 50, 50, 'blue 1')
        #
        s = serge.visual.Register.getItem('blue2')
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,0,255,255), 50, 50, 50, 50, 'blue 2')
        
    def testFailRegisterMultipleWithWrongNumberOfNames(self):
        """testFailRegisterMultipleWithWrongNumberOfNames: should fail when registering multiple with wrong num of names"""
        self.assertRaises(serge.visual.InvalidNameList, 
            serge.visual.Register.registerMultipleItems, ['green', 'red','blue', 'white'], p('allrect.png'), 3) 

    def testFailRegisterMultipleWithDuplicateNames(self):
        """testFailRegisterMultipleWithDuplicateNames: should fail if registering multiple with duplicated names"""
        self.assertRaises(serge.visual.InvalidNameList, 
            serge.visual.Register.registerMultipleItems, ['green', 'red','blue', 'blue'], p('allrect.png'), 4) 

    def testCanUseBasePath(self):
        """testCanUseBasePath: should be able to use a base pathname"""
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('green', 'greenship.png')        
        
    def testFailIfIncorrectBasePath(self):
        """testFailIfIncorrectBasePath: should fail if specifying an incorrect base path"""
        self.assertRaises(serge.registry.BadPath, 
            serge.visual.Register.setPath, os.path.join(os.path.abspath(os.curdir), 'test', 'images', 'not'))
        
    def testCanUseAbsoluteAsWellAsBasePath(self):
        """testCanUseAbsoluteAsWellAsBasePath: can use an absolute path as well as base"""
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('green', p('greenship.png'))
        
    def testFailRegisteringNonExistentSprite(self):
        """testFailRegisteringNonExistentSprite: should fail if register a missing sprite"""
        self.assertRaises(serge.visual.BadSprite, serge.visual.Register.registerItem, 'green', p('no-greenship.png'))
        
    def testCanGetASprite(self):
        """testCanGetASprite: should be able to get a sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        g = serge.visual.Register.getItem('green')
        
    def testCanDuplicateASprite(self):
        """testCanDuplicateASprite: should be able to duplicate a sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        serge.visual.Register.duplicateItem('green', 'blue')
        g = serge.visual.Register.getItem('green')
        b = serge.visual.Register.getItem('blue')
        self.assertEqual(g.width, b.width)
        self.assertEqual(g.height, b.height)

    def testFailDuplicateMissingSprite(self):
        """testFailDuplicateMissingSprite: should fail when duplicating a missing sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Register.duplicateItem, 'greenxxx', 'blue')
    
    def testFailIfGetAMissingSprite(self):
        """testFailIfGetAMissingSprite: should fail if missing a """
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Register.getItem, 'green')

    def testFailIfSetSameSpriteTwice(self):
        """testFailIfSetSameSpriteTwice: should fail if set the same sprite two times"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        self.assertRaises(serge.registry.DuplicateItem, serge.visual.Register.registerItem, 'green', p('greenship.png'))

    def testCanclearItems(self):
        """testCanclearItems: should be able to clear all sprites"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        serge.visual.Register.registerItem('blue', p('blueship.png'))
        serge.visual.Register.registerItem('yellow', p('yellowship.png'))
        serge.visual.Register.clearItems()
        self.assertEqual([], serge.visual.Register.getNames())        
                       
    def testCanGetListOfSprites(self):
        """testCanGetListOfSprites: should be able to get a list of sprites"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        serge.visual.Register.registerItem('blue', p('blueship.png'))
        serge.visual.Register.registerItem('yellow', p('yellowship.png'))
        self.assertEqual(set(['green', 'blue', 'yellow']), set(serge.visual.Register.getNames()))
    
    def testCanIterateThroughSprites(self):
        """testCanIterateThroughSprites: should be able to iterate through sprites"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        serge.visual.Register.registerItem('blue', p('blueship.png'))
        serge.visual.Register.registerItem('yellow', p('yellowship.png'))
        self.assertEqual(set(['green', 'blue', 'yellow']), set([s[0] for s in serge.visual.Register.getItemDefinitions()]))
        
    def testCanRemoveItem(self):
        """testCanRemoveItem: should be able to remove a sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        serge.visual.Register.removeItem('green')
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Register.getItem, 'green')
        self.assertEqual(0, len(serge.visual.Register.getItemDefinitions()))
               
    def testFailIfRemoveMissingSprite(self):
        """testFailIfRemoveMissingSprite: should fail to remove a missing sprite"""
        self.assertRaises(serge.registry.UnknownItem, serge.visual.Register.removeItem, 'green')
       
    def testCanAddSpriteWithNoFilenameForFixingLayer(self):
        """testCanAddSpriteWithNoFilenameForFixingLayer: should be able to add a sprite with no filename"""
        serge.visual.Register.registerItem('green', '')
        self.assertEqual(None, serge.visual.Register.getItem('green'))
        
    def testSpriteHasDimensionsSet(self):
        """testSpriteHasDimensionsSet: the sprite should have its dimensions set"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        self.assertEqual(50, s.width)
        self.assertEqual(50, s.height)
          
    
    ### Serializing ###
    
    def testCanStoreRestoreRegistry(self):
        """testCanStoreRestoreRegistry: should be able to store and restore registry"""
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('green', 'greenrect.png')        
        serge.visual.Register.registerItem('blue', p('bluerect.png'))        
        reg = serge.serialize.Serializable.fromString(serge.visual.Register.asString())
        #
        self.assertEqual(os.path.join(os.path.abspath(os.curdir), 'test', 'images'), reg.base_path)
        self.assertEqual(set(['green', 'blue']), set(reg.getNames()))
        #
        r = serge.render.Renderer()
        s = reg.getItem('green')
        s.renderTo(0, r.getSurface(), (60, 60))
        self.checkRect(r.getSurface(), (0,255,0,255), 85, 85, 50, 50, 'green')
        #
        s = reg.getItem('blue')
        s.renderTo(0, r.getSurface(), (60, 60))
        self.checkRect(r.getSurface(), (0,1,255,255), 85, 85, 50, 50, 'blue')
    
      
    ### Rendering Surface ###
    
    def testCanRenderSurfaceDrawing(self):
        """testCanRenderSurfaceDrawing: should be able to render a surface drawing"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        d = serge.visual.SurfaceDrawing(50, 50)
        s.renderTo(0, d.getSurface(), (0, 0))
        d.renderTo(0, r.getSurface(), (50-d.cx, 50-d.cy))
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        
    def testCanRotateASurfaceDrawing(self):
        """testCanRotateASurfaceDrawing: should be able to rotate a surface drawing"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        d = serge.visual.SurfaceDrawing(50, 50)
        s.renderTo(0, d.getSurface(), (0, 0))
        d.setAngle(45)
        d.renderTo(0, r.getSurface(), (50-d.cx, 50-d.cy))
        self.save(r, 2)
        self.check45Rect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        
    def testCanScaleASurfaceDrawing(self):
        """testCanScaleASurfaceDrawing: should be able to scale a surface drawing"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        d = serge.visual.SurfaceDrawing(50, 50)
        s.renderTo(0, d.getSurface(), (0, 0))
        d.setScale(0.5)
        d.renderTo(0, r.getSurface(), (50-d.cx, 50-d.cy))
        self.save(r, 3)
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 25, 25, 'green')
    
    ### Rendering Sprites ###
    
    def testCanRenderSprite(self):
        """testCanRenderSprite: should be able to render a sprite"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')

    def testRenderRespectsVisible(self):
        """testRenderRespectsVisible: rendering should respect the visible property"""
        r = serge.render.Renderer()
        l = serge.render.Layer('main', 0)
        w = serge.world.World('main')
        z = serge.zone.Zone()
        z.active = True
        w.addZone(z)
        r.addLayer(l)
        #
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('sprite')
        a.setSpriteName('green')
        a.setLayerName('main')        
        #
        a.moveTo(75, 75)
        z.addActor(a)
        w.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        #
        self.checkRect(r.getSurface(), (0,255,0,255), 75, 75, 50, 50, 'default sprite')
        #
        r.clearSurface()
        a.visible = False
        r.preRender()
        w.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.checkRect(r.getSurface(), (0, 0, 0, 255), 75, 75, 50, 50, 'non visible sprite')
        #
        r.clearSurface()
        a.visible = True
        r.preRender()
        w.renderTo(r, 100)
        r.render()
        self.save(r, 3)
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'visible sprite')
        
    
        
    def testCanMoveASprite(self):
        """testCanMoveASprite: should be able to move a sprite"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s.renderTo(0, r.getSurface(), (30,30))
        self.checkRect(r.getSurface(), (0,255,0,255), 55, 55, 50, 50, 'green')
            
    def testCanRenderMultiCellSprite(self):
        """testCanRenderMultiCellSprite: should be able to render a multi cell sprite"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4) # four cells
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        
    def testCanChangeCellOfSprite(self):
        """testCanChangeCellOfSprite: should be able to change the cell of a sprite"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4) # four cells
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.setCell(1)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        s.setCell(2)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        s.setCell(3)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')

    def testCanCopyMultiCell(self):
        """testCanCopyMultiCell: should be able to copy a multi cell sprite"""
        r = serge.render.Renderer()
        s1 = serge.visual.Register.registerItem('all', p('allrect.png'), 4) # four cells
        s2 = s1.getCopy()
        #
        s1.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s1.setCell(1)
        s1.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        # Check that the copy is unchanged 
        r.clearSurface()      
        s2.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
    
    
    def testFailIfCellNumberOutOfRange(self):
        """testFailIfCellNumberOutOfRange: should fail if cell number is out of range"""
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4) # four cells
        self.assertRaises(serge.visual.InvalidCell, s.setCell, -1)
        self.assertRaises(serge.visual.InvalidCell, s.setCell, 4)
                    
    def testAnimatedSpriteShouldBeAbleToUpdate(self):
        """testAnimatedSpriteShouldBeAbleToUpdate: an animated sprite should be able to update its cell"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, True) # four cells
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # red
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        # blue
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        # white
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')
        # Loops back to blue
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        # red
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 1,255), 50, 50, 50, 50, 'red')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 1,255), 50, 50, 50, 50, 'red')
        # green
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1,255,1,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1,255,1,255), 50, 50, 50, 50, 'green')
        # loops back to red
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 1,255), 50, 50, 50, 50, 'red')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 1,255), 50, 50, 50, 50, 'red')


    def testCanHaveAnimatedWithNoRepeat(self):
        """testCanHaveAnimatedWithNoRepeat: should be able to have an animated sprite with no repeat"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, running=False, loop=False) # four cells
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # not running yet - should still be green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.running = True
        # now running green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # now running, red
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        # blue
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        # white
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')
        # Doesn't Loop stays no white
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white - should not loop')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white - should not loop')
        # still white
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white - should not loop')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white - should not loop')

    def testCanResetAnimation(self):
        """testCanResetAnimation: should be able to reset the animation"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, running=False, loop=False) # four cells
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # not running yet - should still be green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.running = True
        # now running green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # now running, red
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        # blue
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        # white
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')
        # Doesn't Loop stays no white
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white - should not loop')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white - should not loop')
        # Reset it
        s.resetAnimation(True)
        # now running green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # now running, red
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        s.renderTo(500, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')

    def testCanHaveAnimatedSpriteThatOnlyGoesOneDirection(self):
        """testCanHaveAnimatedSpriteThatOnlyGoesOneDirection: an animated sprite can animate in one direction only"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, True, one_direction=False) # four cells
        #
        # First with the normal multi-direction (goes forward and then back)
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # Skip on 5 seconds - should be going backwards
        for idx in range(4):
            s.renderTo(1000, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        #
        # Now with only one direction
        s = serge.visual.Register.registerItem('all1', p('allrect.png'), 4, 1, 1, True, one_direction=True) # four cells
        #
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # Skip on 4 seconds - should be back to the begining
        for idx in range(4):
            s.renderTo(1000, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        #
        # And continues
        self.assertEqual(1, s.direction)
        s.renderTo(1000, r.getSurface(), (25,25))
        self.assertEqual(1, s.direction)
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        
    def testAnimatedSpriteCanMoveMoreThanOneFrame(self):
        """testAnimatedSpriteCanMoveMoreThanOneFrame: an animated sprite can move forward more than one frame per update"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, True, one_direction=False) # four cells
        #
        # First with the normal multi-direction (goes forward and then back)
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # Skip on 2 seconds - should be on blue
        s.renderTo(2000, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')

    def testAnimatedSpriteCanMoveManyFrames(self):
        """testAnimatedSpriteCanMoveManyFrames: an animated sprite can move many frames per update"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, True, one_direction=False) # four cells
        #
        # First with the normal multi-direction (goes forward and then back)
        # green
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        # Skip on 10 seconds - should be going backwards 
        s.renderTo(10000, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        # One more should take us to red
        s.renderTo(1000, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,1, 0,255), 50, 50, 50, 50, 'red')
        # 9 more should take us to all the way back to blue
        s.renderTo(9000, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (1, 1, 255, 255), 50, 50, 50, 50, 'blue')
        
    def testCopyHasLoop(self):
        """testCopyHasLoop: bug when a copy of an item doesn't have a loop attribute"""
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4, 1, 1, running=False, loop=False) # four cells
        self.assertTrue(hasattr(s, 'loop'))
        self.assertTrue(hasattr(s.getCopy(), 'loop'))
                    
    def testCanZoomAnInitialSprite(self):
        """testCanZoomAnInitialSprite: should be able to change the initial zoom of a sprite"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'), zoom=0.5)
        s.renderTo(0, r.getSurface(), (30,30))
        # Should be half as big (was 50 now 25)
        self.checkRect(r.getSurface(), (0,255,0,255), 43, 43, 25, 25, 'green')

    def testShouldFailWithInvalidInitialZoom(self):
        """testShouldFailWithInvalidInitialZoom: should throw an error if initial zoom is invalid"""
        r = serge.render.Renderer()
        self.assertRaises(serge.visual.BadScale, serge.visual.Register.registerItem, 'green', p('greenrect.png'), zoom=0.0)
        
    def testCanSetAnInitialAngle(self):
        """testCanSetAnInitialAngle: should be able to set an initial angle for a sprite"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'), angle=45)
        s.renderTo(0, r.getSurface(), (30,30))
        self.save(r, 1)
        # Should be rotated by 45 degrees
        self.check45Rect(r.getSurface(), (0,255,0,255), 65, 65, 50, 50, 'green')

    def testCanRenderSpriteTransparency(self):
        """testCanRenderSpriteTransparency: should be able to render a sprite with transparency"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s.setAlpha(0.5)
        s.renderTo(0, r.getSurface(), (25,25))
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0, 127,0,255), 50, 50, 50, 50, '0.5 alpha')
        #
        r.clearSurface()
        s.setAlpha(1.0)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, '1.0 again')
        
    def testCanRenderTextTransparency(self):
        """testCanRenderTextTransparency: should be able to render text with transparency"""
        s = serge.visual.Text('Hello', (0,255,0))
        s.setAlpha(0.5)
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.assertEqual((0,39,0,255), r.getSurface().get_at((49, 59)))
        self.assertEqual((0,0,0,255), r.getSurface().get_at((60,56)))
        #
        s.setAlpha(1.0)
        r.clearSurface()
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((49, 58)))
        self.assertEqual((0,0,0,255), r.getSurface().get_at((60,56)))
        
    
    ### Multi cell sprites from files ###
    
    def testMultiCellFromMultiFiles(self):
        """testMultiCellFromMultiFiles: should be able to create a multi cell from multiple files"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerFromFiles('all', p('allrect%d.png'), 4) # four cells
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.setCell(1)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,0, 0,255), 50, 50, 50, 50, 'red')
        s.setCell(2)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0, 0, 255, 255), 50, 50, 50, 50, 'blue')
        s.setCell(3)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')

    def testFailMultiCellIfNotEnoughFiles(self):
        """testFailMultiCellIfNotEnoughFiles: should fail when creating a multi cell from files and there are not enough files"""
        self.assertRaises(serge.visual.NotAllFilesFound,
            serge.visual.Register.registerFromFiles, 'all', p('allrect%d.png'), 5) # there are only four cells
        
    def testCanStoreRestoreRegistryWithMultiFiles(self):
        """testCanStoreRestoreRegistryWithMultiFiles: should be able to store and restore registry when we have multi files"""
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        s = serge.visual.Register.registerFromFiles('all', p('allrect%d.png'), 4) # four cells
        reg = serge.serialize.Serializable.fromString(serge.visual.Register.asString())
        #
        self.assertEqual(os.path.join(os.path.abspath(os.curdir), 'test', 'images'), reg.base_path)
        self.assertEqual(set(['all']), set(reg.getNames()))
        #
        r = serge.render.Renderer()
        s = reg.getItem('all')
        #
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0,255,0,255), 50, 50, 50, 50, 'green')
        s.setCell(1)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,0, 0,255), 50, 50, 50, 50, 'red')
        s.setCell(2)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (0, 0, 255, 255), 50, 50, 50, 50, 'blue')
        s.setCell(3)
        s.renderTo(0, r.getSurface(), (25,25))
        self.checkRect(r.getSurface(), (255,255, 255,255), 50, 50, 50, 50, 'white')

    ### Modifying the rendering of the object ###
    
    def testCanScale(self):
        """testCanScale: should be able to scale the object"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s.renderTo(0, r.getSurface(), (60-25, 60-25))
        # initial
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial')
        # get smaller (0.5)
        s.scaleBy(0.5)        
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25/2, 60-25/2))
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 25, 25, 'half')
        # get bigger (back to 1)
        s.scaleBy(2.0)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25, 60-25))
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'back to initial')
        # get bigger (to 2)
        s.scaleBy(2.0)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25*2, 60-25*2))
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 100, 100, 'double')

    def testCanScaleDirectly(self):
        """testCanScaleDirectly: should be able to set scale directly"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s.renderTo(0, r.getSurface(), (60-25, 60-25))
        # initial
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial')
        # get smaller (0.5)
        s.setScale(0.5)        
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25/2, 60-25/2))
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 25, 25, 'half')
        # get bigger (back to 1)
        s.setScale(1.0)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25, 60-25))
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'back to initial')
        # get bigger (to 2)
        s.setScale(2.0)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25*2, 60-25*2))
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 100, 100, 'double')
        
    def testCanSetActualSize(self):
        """testCanSetActualSize: should be able to set actual size of sprite directly"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s.renderTo(0, r.getSurface(), (60-25, 60-25))
        # initial
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial')
        # get smaller in x (0.5)
        s.setSize(25, 50)        
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25/2, 60-25))
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 25, 50, 'x')
        # get bigger (back to 1)
        s.setSize(50, 50)   
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25, 60-25))
        self.save(r, 2)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'back to initial')
        # get bigger in y (to 2)
        s.setSize(50, 50*2)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60-25, 60-25*2))
        self.save(r, 3)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 100, 'double')
    
    def testFailIfBadScaling(self):
        """testFailIfBadScaling: should fail if try to scale out of range"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        self.assertRaises(serge.visual.BadScale, s.scaleBy, -1)
        self.assertRaises(serge.visual.BadScale, s.scaleBy, 0)
    
    def testCanScaleMultiCell(self):
        """testCanScaleMultiCell: scaling a multi cell should work"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('all', p('allrect.png'), 4) # four cells
        for cell, colour in ((0, (0,255,0,255)), (1, (255,0,0,255)), (2, (0,0,255,255))):
            s.setCell(cell)
            s.renderTo(0, r.getSurface(), (60, 60))
            # initial
            self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'initial')
            # get smaller (0.5)
            s.scaleBy(0.5)        
            r.clearSurface()
            s.renderTo(0, r.getSurface(), (60, 60))
            self.checkRect(r.getSurface(), colour, 72, 72, 25, 25, 'half')
            # get bigger (back to 1)
            s.scaleBy(2.0)
            r.clearSurface()
            s.renderTo(0, r.getSurface(), (60, 60))
            self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'back to initial')
            # get bigger (to 2)
            s.scaleBy(2.0)
            r.clearSurface()
            s.renderTo(0, r.getSurface(), (60, 60))
            self.checkRect(r.getSurface(), colour, 110, 110, 100, 100, 'double')
            # clear up for next loop
            r.clearSurface()
            s.scaleBy(0.5)
        
    def testCanRotateObject(self):
        """testCanRotateObject: should be able to rotate the object"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        colour = (0, 255, 0, 255)
        s.renderTo(0, r.getSurface(), (60, 60))
        # initial
        self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'initial')
        # rotate by 45
        s.rotateBy(45)        
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.save(r, 1)
        self.check45Rect(r.getSurface(), colour, 60+50/math.sqrt(2), 60+50/math.sqrt(2), 50, 50, '45')
        # rotate back
        s.rotateBy(-45)        
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'back to initial')
        
    def testCanFlipHorizontal(self):
        """testCanFlipHorizontal: should be able to flip the object horizontally"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('multi', p('multi.png'))
        s.renderTo(0, r.getSurface(), (60, 60))
        # initial
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'initial green')
        self.assertEqual(r.getSurface().get_at((105,65)), (255,0,0,255), 'initial red')
        # flip
        s.flipHorizontal()
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((105, 65)), (0,255,0,255), 'flipped green')
        self.assertEqual(r.getSurface().get_at((65,65)), (255,0,0,255), 'flipped red')
        # rotate back
        s.flipHorizontal()
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'back green')
        self.assertEqual(r.getSurface().get_at((105,65)), (255,0,0,255), 'back red')

    def testCanSetHorizontalFlip(self):
        """testCanSetHorizontalFlip: should be able to set the horizontal flip"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('multi', p('multi.png'))
        s.renderTo(0, r.getSurface(), (60, 60))
        # initial
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'initial green')
        self.assertEqual(r.getSurface().get_at((105,65)), (255,0,0,255), 'initial red')
        # flip
        s.setHorizontalFlip(True)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((105, 65)), (0,255,0,255), 'flipped green')
        self.assertEqual(r.getSurface().get_at((65,65)), (255,0,0,255), 'flipped red')
        # rotate back
        s.setHorizontalFlip(False)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'back green')
        self.assertEqual(r.getSurface().get_at((105,65)), (255,0,0,255), 'back red')
        
    def testCanFlipVertical(self):
        """testCanFlipVertical: should be able to flip the object vertically"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('multi', p('multi.png'))
        s.renderTo(0, r.getSurface(), (60, 60))
        # initial
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'initial green')
        self.assertEqual(r.getSurface().get_at((65,105)), (0,0,255,255), 'initial blue')
        # flip
        s.flipVertical()
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((65, 105)), (0,255,0,255), 'flipped green')
        self.assertEqual(r.getSurface().get_at((65,65)), (0,0,255,255), 'flipped blue')
        # rotate back
        s.flipVertical()
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'back green')
        self.assertEqual(r.getSurface().get_at((65, 105)), (0,0,255,255), 'back blue')

    def testCanSetVerticalFlip(self):
        """testCanSetVerticalFlip: should be able to set the vertical flip"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('multi', p('multi.png'))
        s.renderTo(0, r.getSurface(), (60, 60))
        # initial
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'initial green')
        self.assertEqual(r.getSurface().get_at((65,105)), (0,0,255,255), 'initial blue')
        # flip
        s.setVerticalFlip(True)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((65, 105)), (0,255,0,255), 'flipped green')
        self.assertEqual(r.getSurface().get_at((65,65)), (0,0,255,255), 'flipped blue')
        # rotate back
        s.setVerticalFlip(False)
        r.clearSurface()
        s.renderTo(0, r.getSurface(), (60, 60))
        self.assertEqual(r.getSurface().get_at((65, 65)), (0,255,0,255), 'back green')
        self.assertEqual(r.getSurface().get_at((65, 105)), (0,0,255,255), 'back blue')
        
    def testCanRotateMultiCell(self):
        """testCanRotateMultiCell: should be able to rotate a multi cell object""" 
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('allrect.png'), 4)
        for cell, colour in ((0, (0,255,0,255)), (1, (255,0,0,255)), (2, (0,0,255,255))):
            s.setCell(cell)
            s.renderTo(0, r.getSurface(), (60, 60))
            self.save(r, 1)
            # initial
            self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'initial')
            # rotate by 45
            s.setAngle(45)        
            r.clearSurface()
            s.renderTo(0, r.getSurface(), (60, 60))
            self.save(r, 2)
            self.check45Rect(r.getSurface(), colour, 95, 95, 50, 50, '45')
            # rotate back
            s.setAngle(0)        
            r.clearSurface()
            s.renderTo(0, r.getSurface(), (60, 60))
            self.save(r, 3)
            self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'back to initial')
            # clear up for next loop
            r.clearSurface()

    def testCanCacheRotation(self):
        """testCanCacheRotation: should be able to cache rotations"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('green', p('allrect.png'), 4)
        times = []
        for cache in (False, True):
            s.cache_rotations = cache
            start = time.time()
            for repeat in range(200):
                for cell, colour in ((0, (0,255,0,255)), (1, (255,0,0,255)), (2, (0,0,255,255))):
                    s.setCell(cell)
                    s.renderTo(0, r.getSurface(), (60, 60))
                    # initial
                    self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'initial')
                    # rotate by 45
                    s.setAngle(45)        
                    r.clearSurface()
                    s.renderTo(0, r.getSurface(), (60, 60))
                    self.check45Rect(r.getSurface(), colour, 95, 95, 50, 50, '45')
                    # rotate back
                    s.setAngle(0)        
                    r.clearSurface()
                    s.renderTo(0, r.getSurface(), (60, 60))
                    self.checkRect(r.getSurface(), colour, 85, 85, 50, 50, 'back to initial')
                    # clear up for next loop
                    r.clearSurface()
            times.append(time.time()-start)
        print 'Times for non/cached are %s' % times
        self.assertTrue(times[0] - times[1] > times[0]/5)
    
    ### Converting alpha mode ###
      
    def testCanSetConvertAlphaInRegister(self):
        """testCanSetConvertAlphaInRegister: should be able to convert alpha during registration"""
        r = serge.render.Renderer()
        s = serge.visual.Register.registerItem('png', p('i2.png'), 4)
        #
        # Base performance
        start = time.time()
        for i in range(100):
            s.renderTo(0, r.getSurface(), (0,0))
        base_time = time.time() - start
        #
        # Enhanced performance
        s = serge.visual.Register.registerItem('fast_png', p('i2.png'), 4, convert_alpha=True)
        start = time.time()
        for i in range(100):
            s.renderTo(0, r.getSurface(), (0,0))
        new_time = time.time() - start
        #
        # Should be at least twice as fast
        self.assertTrue(new_time/base_time < 0.5, 'Not fast enough base %s, new %s, ratio %s. Should be 2x' 
            % (base_time, new_time, new_time/base_time))

    def testConvertAlphaWorksWithGetItem(self):
        """testConvertAlphaWorksWithGetItem: convert alpha should be retained when getting an item"""
        r = serge.render.Renderer()
        serge.visual.Register.registerItem('png', p('i2.png'), 4)
        s = serge.visual.Register.getItem('png')
        #
        # Base performance
        start = time.time()
        for i in range(100):
            s.renderTo(0, r.getSurface(), (0,0))
        base_time = time.time() - start
        #
        # Enhanced performance
        serge.visual.Register.registerItem('fast_png', p('i2.png'), 4, convert_alpha=True)
        s = serge.visual.Register.getItem('fast_png')
        start = time.time()
        for i in range(100):
            s.renderTo(0, r.getSurface(), (0,0))
        new_time = time.time() - start
        #
        # Should be at least twice as fast
        self.assertTrue(new_time/base_time < 0.5, 'Not fast enough base %s, new %s, ratio %s. Should be 2x' 
            % (base_time, new_time, new_time/base_time))
        
    def testConvertAlphaWorksWithSetSprite(self):
        """testConvertAlphaWorksWithSetSprite: should retain convert alpha when setting the sprite by name"""
        r = serge.render.Renderer()
        serge.visual.Register.registerItem('png', p('i2.png'), 4)
        serge.visual.Register.registerItem('fast_png', p('i2.png'), 4, convert_alpha=True)
        a = serge.actor.Actor('a','a')
        a.setSpriteName('png')
        #
        # Base performance
        start = time.time()
        for i in range(100):
            a.visual.renderTo(0, r.getSurface(), (0,0))
        base_time = time.time() - start
        #
        # Enhanced performance
        a.setSpriteName('fast_png')
        start = time.time()
        for i in range(100):
            a.visual.renderTo(0, r.getSurface(), (0,0))
        new_time = time.time() - start
        #
        # Should be at least twice as fast
        self.assertTrue(new_time/base_time < 0.5, 'Not fast enough base %s, new %s, ratio %s. Should be 2x' 
            % (base_time, new_time, new_time/base_time))
       
    
    ### Rotation ###
    
    def testCanRotateCircle(self):
        """testCanRotateCircle: should be able to rotate a circle in a stable way"""
        r = serge.render.Renderer()
        l = serge.render.Layer('main', 0)
        r.addLayer(l)
        colour = (255, 0, 0, 255)
        s = serge.visual.Register.registerItem('ball', p('redball.png'))
        a = serge.actor.Actor('ball')
        a.setSpriteName('ball')
        a.setLayerName('main')
        a.moveTo(100, 100)
        a.renderTo(r, 0)
        r.render()
        #
        # Should be sitting at 100, 100 with radius 32
        self.save(r, 1)
        self.checkCircle(r.getSurface(), colour, 68, 68, 32, 'initial')
        #
        # Use non-filtered rotatation, which is a bit easier to check
        serge.visual.Sprite.rotate = lambda self, img, angle, scale : pygame.transform.rotate(img, angle)
        #
        for i in range(-360, 360, 20):
            r.clearSurface()    
            l.clearSurface()    
            a.setAngle(i)
            self.assertEqual(i, a.getAngle())
            a.renderTo(r, 0)
            r.render()
            self.save(r, 2)
            #
            # Should be in the right place and width and height of actor should be right
            self.checkCircle(r.getSurface(), colour, 68, 68, 31, ('angle %d' % (i*2)), 30)
            self.assertEqual(a.visual.width, a.width)
            self.assertEqual(a.visual.height, a.height)
        
    
       
    ### Actors ###

    def testCanSetActorsSprite(self):
        """testCanSetActorsSprite: should be able to set an actors sprite"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial')

    def testSettingSpriteTwiceShouldHaveNoEffect(self):
        """testSettingSpriteTwiceShouldHaveNoEffect: should bypass changes if set the same name twice"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        s = serge.visual.Register.registerItem('red', p('multi2.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        self.assertEqual(0, a.visual.current_cell)
        #
        # Change the cell and then reset sprite
        a.visual.current_cell = 1
        a.setSpriteName('green')
        self.assertEqual(1, a.visual.current_cell)
        #
        # But should be fine if we change sprite
        a.visual.current_cell = 1
        a.setSpriteName('red')
        self.assertEqual(0, a.visual.current_cell)
        
                    
    def testFailIfActorSpriteIsMissing(self):
        """testFailIfActorSpriteIsMissing: should throw an execption of the sprite is missing"""
        a = serge.actor.Actor('a')
        self.assertRaises(serge.registry.UnknownItem, a.setSpriteName, 'green')
              
    def testFailActorRendersToMissingLayer(self):
        """testFailActorRendersToMissingLayer: should throw an exception if try to render to a missing layer"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main-not')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        self.assertRaises(serge.render.UnknownLayer, a.renderTo, r, 100)
    
    def testSpriteSettingShouldSetWidthAndHeight(self):
        """testSpriteSettingShouldSetWidthAndHeight: when setting a sprite the width and height should be set"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpatialCentered(100, 110, 10, 20)
        a.setSpriteName('green')
        x, y, w, h = a.getSpatialCentered()
        self.assertEqual((100, 110, 50, 50), (x, y, w, h))
        
    

        
    
        
    ### Text ###
    
    def _setAsText(self, a, s):
        """Set an actor as some text"""
        # This is a legacy method that was removed (actor.setAsText)
        a.visual = s
        
    def testCanRenderText(self):
        """testCanRenderText: should be able to render text"""
        s = serge.visual.Text('Hello', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((49, 58)))
        self.assertEqual((0,0,0,255), r.getSurface().get_at((60,56)))

    def testCanRenderTextLeftJustified(self):
        """testCanRenderText: should be able to render text left justified"""
        s = serge.visual.Text('Hello', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        a.moveTo(60, 60)
        a.visual.setJustify('left')
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.assertEqual((0,0,0,255), r.getSurface().get_at((49, 59)))
        self.assertEqual((0,255,0,255), r.getSurface().get_at((65, 66)))
        self.assertEqual(60, a.x)
        self.assertEqual(60, a.y)
        #
        a.visual.setJustify('center')
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((48, 58)))

    def testCanCheckRect(self):
        """testCanCheckRect: should be able to check the rect"""
        s = serge.visual.Text('Hello', (0,255,0), justify='left')
        a = serge.actor.Actor('greet')
        a.visual = s
        a.setLayerName('main')
        a.moveTo(60, 60)
        #
        self.assertEqual(60-a.width/2, a.rect[0])
        self.assertEqual(60-a.height/2, a.rect[1])
        
    def testFailWithInvalidJustify(self):
        """testFailWithInvalidJustify: should fail with invalid justification"""
        s = serge.visual.Text('Hello', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        self.assertRaises(serge.visual.InvalidJustification, a.visual.setJustify, 'leftxxx')
            
    def testCanSetFontSize(self):
        """testCanSetFontSize: should be able to set the font size"""
        s = serge.visual.Text('Hello', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        s.setFontSize(24)
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((39, 58)))
        
    def testCanRotate(self):
        """testCanRotate: should be able to rotate"""
        s = serge.visual.Text('Hello', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        s.setAngle(90)
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 3)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((60, 58)))

    def testCanScaleText(self):
        """testCanScaleText: should be able to scale"""
        s = serge.visual.Text('Hello', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        s.scaleBy(2)
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 4)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((39, 58)))

    def testTextCanHaveMultipleLines(self):
        """testTextCanHaveMultipleLines: should be able to use text with multiple lines"""
        s = serge.visual.Text('Hello\nThere', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.assertEqual((0,255,0,255), r.getSurface().get_at((44, 50)))
        self.assertEqual((0,0,0,255), r.getSurface().get_at((48, 57)))
        self.assertEqual((0,255,0,255), r.getSurface().get_at((45, 63)))
        self.assertEqual((0,0,0,255), r.getSurface().get_at((51, 72)))
    
    def testMultipleLineTextIsAsLongAsLongestList(self):
        """testMultipleLineTextIsAsLongAsLongestList: for multiple lines should use longest line"""
        s1 = serge.visual.Text('a', (0,255,0))
        s2 = serge.visual.Text('a longer bit of text', (0,255,0))
        s3 = serge.visual.Text('a\na longer bit of text', (0,255,0))
        s4 = serge.visual.Text('a longer bit of text\na', (0,255,0))
        s5 = serge.visual.Text('iii\nOO', (0,255,0))
        s6 = serge.visual.Text('OO', (0,255,0))
        #
        self.assertEqual(s2.width, s3.width)
        self.assertEqual(s2.width, s4.width)
        self.assertTrue(s1.width < s3.width)
        self.assertEqual(s5.width, s6.width)
        
    
    def testCanHandleEmptyText(self):
        """testCanHandleEmptyText: should be able to handle empty text"""
        s = serge.visual.Text('', (0,255,0))
        a = serge.actor.Actor('greet')
        self._setAsText(a, s)
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
   
        
    ### Sprite and rectangle equivalence ###
    
    def testSpritesAndRectanglesShouldBeEquivalent(self):
        """testSpritesAndRectanglesShouldBeEquivalent: should be able to use sprites and rectangles the same"""
        r = serge.render.Renderer()
        l = serge.render.Layer('main', 0)
        r.addLayer(l)
        #
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('sprite')
        a.setSpriteName('green')
        a.setLayerName('main')        
        #
        a.setOrigin(500, 500)
        a.moveTo(75, 75)
        a.renderTo(r, 100)
        r.render()
        #
        self.save(r, 1)    
        self.checkRect(r.getSurface(), (0,255,0,255), 75, 75, 50, 50, 'sprite')
        #
        r.clearSurface()
        l.clearSurface()
        a.visual = serge.blocks.visualblocks.Rectangle((50,50), (0,255,0,255))
        a.setOrigin(500, 500)
        a.moveTo(75, 75)
        a.renderTo(r, 100)
        r.render()
        #
        self.save(r, 2)    
        self.checkRect(r.getSurface(), (0,255,0,255), 75, 75, 50, 50, 'rect')
        
    ### Fonts ###
    
    def testCanRegisterAFont(self):
        """testCanRegisterAFont: should be able to register a font"""
        serge.visual.Fonts.registerItem('main', os.path.join('test', 'BerenikaBold', 'BerenikaBold.ttf'))
        
    def testFailRegisterMissingFont(self):
        """testFailRegisterMissingFont: should fail when registering a missing font"""
        self.assertRaises(serge.visual.BadFont,
            serge.visual.Fonts.registerItem, 'main', os.path.join('test', 'BerenikaBold', 'BerenikaBoldXXX.ttf'))
        
    def testUseRegisterdFont(self):
        """testUseRegisterdFont: should be able to use a registered font"""
        serge.visual.Fonts.registerItem('main', os.path.join('test', 'BerenikaBold', 'BerenikaBold.ttf'))
        t = serge.visual.Text('test', (255,0,0,255), 'main')        
    
    ### bugs ###    
    
    def testReverseAnimationBug(self):
        """testReverseAnimationBug: was a bug where the animation would reverse incorrectly"""
        serge.visual.Register.registerItem('walking', p('greenrect.png'), 5, 20, running=True, framerate=10, one_direction=True)
        a = serge.actor.Actor('sprite')
        a.setSpriteName('walking')
        s = a.visual
        self.assertEqual(True, s.one_direction)
        self.assertEqual(True, s.loop)
        self.assertEqual(10, s.framerate)
        self.assertEqual((1, False), s._mapVirtualToRealCell(1))
        
        
      
    
if __name__ == '__main__':
    unittest.main()
