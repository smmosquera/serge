"""Tests for some of the useful blocks"""

import unittest
import pygame
import os

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

from serge.simplevecs import Vec2d

class TestActorBlocks(unittest.TestCase, VisualTester):
    """Tests for the ActorBlocks"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        self.w = serge.world.World('test')
        self.r = serge.render.Renderer()        
        self.r.addLayer(serge.render.Layer('a', 0))
        self.z = serge.zone.Zone()
        self.z.active = True
                
        
    def tearDown(self):
        """Tear down the tests"""                
    
    ### Screen Actor ###
    
    def testScreenActorHasNiceProperties(self):
        """testScreenActorHasNiceProperties: the screen actor should have nice properties"""
        e = serge.engine.Engine()
        w = serge.world.World('this')
        e.addWorld(w)
        a = serge.blocks.actors.ScreenActor('me')
        #
        def added_callback(obj, arg):
            added_callback.seen = True
        added_callback.seen = False
        a.linkEvent(serge.events.E_ADDED_TO_WORLD, added_callback)
        #
        w.addActor(a)
        #
        #
        # Should have attributes
        for attr in ['keyboard', 'mouse', 'engine', 'world', 'broadcaster']:
            self.assert_(hasattr(a, attr), 'does not have attribute "%s"' % attr)
        #
        # Should be correct
        self.assertEqual(w, a.world)
        self.assertEqual(e, a.engine)
        #
        # The normal callback should also have worked
        self.assertEqual(True, added_callback.seen)
    
    ### Repeated Visual ###
       
    def testCanDoLivesActor(self):
        """testCanDoLivesActor: should be able to have a lives actor"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.blocks.actors.RepeatedVisualActor('a', 'a', repeat=2, spacing=100)
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60+50, 60)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial 1')
        self.checkRect(r.getSurface(), (0,255,0,255), 160, 60, 50, 50, 'initial 2')
        #
        # Now reduce lives
        r.preRender()
        a.reduceRepeat()
        a.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'second 1')
        self.checkRect(r.getSurface(), (0,0,0,255), 160, 60, 50, 50, 'second 2')
        #
        # Now increase
        r.preRender()
        a.setRepeat(2)
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'second 1')
        self.checkRect(r.getSurface(), (0,255,0,255), 160, 60, 50, 50, 'second 2')
        #
        self.assertEqual(2, a.getRepeat())        
        #
        # Now use reset
        a.reduceRepeat()
        self.assertEqual(1, a.getRepeat())        
        a.reduceRepeat()
        self.assertEqual(0, a.getRepeat())        
        a.increaseRepeat()
        self.assertEqual(1, a.getRepeat())        
        a.resetRepeat()
        self.assertEqual(2, a.getRepeat())        

    def testLivesActorVertical(self):
        """testLivesActorVertical: should be able to do lives actor vertically"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.blocks.actors.RepeatedVisualActor('a', 'a', repeat=2, spacing=100, orientation='vertical')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60+50)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('main', 0))
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial 1')
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 160, 50, 50, 'initial 2')
        #
        # Now reduce lives
        r.preRender()
        a.reduceRepeat()
        a.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'second 1')
        self.checkRect(r.getSurface(), (0,0,0,255), 60, 160, 50, 50, 'second 2')
        #
        # Now increase
        r.preRender()
        a.setRepeat(2)
        a.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'second 1')
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 160, 50, 50, 'second 2')
        #
        self.assertEqual(2, a.getRepeat())        
        #
        # Now use reset
        a.reduceRepeat()
        self.assertEqual(1, a.getRepeat())        
        a.reduceRepeat()
        self.assertEqual(0, a.getRepeat())        
        a.increaseRepeat()
        self.assertEqual(1, a.getRepeat())        
        a.resetRepeat()
        self.assertEqual(2, a.getRepeat())                

    def testRepeatedActorClickArea(self):
        """testRepeatedActorClickArea: the click area for a repeated actor should be the total size"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.blocks.actors.RepeatedVisualActor('a', 'a', repeat=2, spacing=100, orientation='vertical')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60+50)
        #
        for x, y in ((60, 60), (60, 160), (60-24, 60-24), (60+24, 160+24)):
            pt = serge.geometry.Point(x, y)
            self.assertTrue(pt.isInside(a), 'Not inside %d, %d' % (x, y))
        for x, y in ((60-26, 60-26), (60+26, 160+26)):
            pt = serge.geometry.Point(x, y)
            self.assertFalse(pt.isInside(a), 'Not outside %d, %d' % (x, y))
        #
        # When reducing repeat, should go down
        a.reduceRepeat()
        self.assertFalse(serge.geometry.Point(60, 160).isInside(a))
        a.increaseRepeat()
        self.assertTrue(serge.geometry.Point(60, 160).isInside(a))
        
    ### Toggled Menu ###
    
    def testCanCreateToggleMenu(self):
        """testCanCreateToggleMenu: should be able to create a toggled menu item"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        menu.moveTo(100, 100)
        menu.layout.setLayerName('a')
        self.w.addActor(menu)
        self.w.renderTo(self.r, 0)
        self.r.render()
        #
        self.save(self.r, 1)
        self.checkPoint((0,255,0,255), self.r.getSurface(), (100, 25), 'one')
        self.checkPoint((255,0,0,255), self.r.getSurface(), (100, 175), 'two')        

    def testCanClearSelection(self):
        """testCanClearSelection: should be able to clear the selected item"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        menu.moveTo(100, 100)
        menu.layout.setLayerName('a')
        self.w.addActor(menu)
        menu.clearSelection()
        self.w.renderTo(self.r, 0)
        self.r.render()
        #
        self.save(self.r, 1)
        self.checkPoint((255,0,0,255), self.r.getSurface(), (100, 25), 'one')
        self.checkPoint((255,0,0,255), self.r.getSurface(), (100, 175), 'two')        

    def testFailToggledMenuNoItems(self):
        """testFailToggledMenuNoItems: should fail if toggled menu creates no items"""
        self.assertRaises(serge.blocks.actors.InvalidMenu,
            serge.blocks.actors.ToggledMenu, 'm', 'm', items=[],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))

    def testFailToggleMenuDuplicates(self):
        """testFailToggleMenuDuplicates: should fail if there are duplicates in toggled menu"""
        self.assertRaises(serge.blocks.actors.InvalidMenu,
            serge.blocks.actors.ToggledMenu, 'm', 'm', items=['one', 'one'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        
    def testCanSelectDifferentItemsInToggledMenu(self):
        """testCanSelectDifferentItemsInToggledMenu: should be able to switch selection in toggle menu"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        menu.moveTo(100, 100)
        menu.layout.setLayerName('a')
        menu.selectItem('two')
        #
        self.w.addActor(menu)
        self.w.renderTo(self.r, 0)
        self.r.render()
        #
        self.save(self.r, 1)
        self.checkPoint((0,255,0,255), self.r.getSurface(), (100, 175), 'two')
        self.checkPoint((255,0,0,255), self.r.getSurface(), (100, 25), 'one')        
        self.assertEqual('two', menu.getSelection())
        self.assertEqual(1, menu.getSelectionIndex())

    def testCanSelectDifferentItemsInToggledMenuByIndex(self):
        """testCanSelectDifferentItemsInToggledMenuByIndex: should be able to switch selection in toggle menu by index"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        menu.moveTo(100, 100)
        menu.layout.setLayerName('a')
        menu.selectItemIndex(1)
        #
        self.w.addActor(menu)
        self.w.renderTo(self.r, 0)
        self.r.render()
        #
        self.save(self.r, 1)
        self.checkPoint((0,255,0,255), self.r.getSurface(), (100, 175), 'two')
        self.checkPoint((255,0,0,255), self.r.getSurface(), (100, 25), 'one')        
        self.assertEqual('two', menu.getSelection())
        self.assertEqual(1, menu.getSelectionIndex())
        
    def testFailSelectInvalidItemInToggledMenu(self):
        """testFailSelectInvalidItemInToggledMenu: should fail if select an invalid item in a toggled menu"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        self.assertRaises(serge.blocks.actors.InvalidMenuItem, menu.selectItem, 'three')
        
    def testToggledMenuSelectionCallsCallback(self):
        """testToggledMenuSelectionCallsCallback: should call a callback when selecting an item in toggled menu"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=200, height=200),
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0), callback=self._test)
        menu.moveTo(100, 100)
        menu.layout.setLayerName('a')
        self._done = False
        menu.selectItem('two')
        self.assertTrue(self._done)
        #
        # Reselecting should not do anythnig
        self._done = False
        menu.selectItem('two')
        self.assertFalse(self._done)
        
    def _test(self, obj, arg):
        """Test callback"""
        self._done = True

    def testMovingMenuShouldMoveItem(self):
        """testMovingMenuShouldMoveItem: should move items when moving the menu"""
        menu = serge.blocks.actors.ToggledMenu('m', 'm', items=['one','two'],
            layout=serge.blocks.layout.VerticalBar('m', 'm', width=100, height=200), height=100,
            default='one', on_colour=(0, 255, 0), off_colour=(255, 0, 0))
        menu.moveTo(100, 100)
        menu.layout.setLayerName('a')
        self.w.addActor(menu)
        self.w.renderTo(self.r, 0)
        self.r.render()
        #
        self.save(self.r, 1)
        self.checkPoint((0,255,0,255), self.r.getSurface(), (100, 25), 'one')
        self.checkPoint((255,0,0,255), self.r.getSurface(), (100, 175), 'two')        
    
    
    ### Physics actors ###  
    
    def testCanCreatePhysicsActor(self):
        """testCanCreatePhysicsActor: should be able to create a physics actor"""
        a = serge.blocks.actors.SimplePhysicsActor('a', 'a', Vec2d(0,0), 0)
        
    def testPhysicsActorVelocity(self):
        """testPhysicsActorVelocity: physics actor moves with velocity"""
        a = serge.blocks.actors.SimplePhysicsActor('a', 'a', Vec2d(1,2), 0)
        a.moveTo(0,0)
        #
        a.updateActor(1000, None)
        self.assertEqual((1,2), (a.x, a.y))
        
    def testPhysicsActorRotates(self):
        """testPhysicsActorRotates: physics actos should be able to rotate"""
        a = serge.blocks.actors.SimplePhysicsActor('a', 'a', Vec2d(1,2), 10)
        a.moveTo(0,0)
        a.setAngle(0)
        #
        a.updateActor(1000, None)
        self.assertEqual(10, a.getAngle())
        
    def testPhysicsActorBounds(self):
        """testPhysicsActorBounds: should be able to check bounds for physics actor"""
        a = serge.blocks.actors.SimplePhysicsActor('a', 'a', Vec2d(1,2), 10, bounds=((-10, 10), (-100, 100)))
        self.w.addZone(self.z)
        self.w.addActor(a)
        self.assertEqual(True, self.w.hasActor(a))
        #
        # Allow to move
        self.w.updateWorld(9000)
        self.assertEqual(True, self.w.hasActor(a))
        #
        # Move so actor would be out of bounds
        self.w.updateWorld(2000)
        self.assertEqual(False, self.w.hasActor(a))
                
           
    
               
if __name__ == '__main__':
    unittest.main()
