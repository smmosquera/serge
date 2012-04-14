"""Tests for the Serge engine"""

import unittest
import time
import os
import pygame

from helper import *

import serge.engine
import serge.world
import serge.zone
import serge.render
import serge.visual
import serge.actor
import serge.input
import serge.blocks.utils

class TestEngine(unittest.TestCase, VisualTester):
    """Tests for the Engine"""

    def setUp(self):
        """Set up the tests"""
        self.e = serge.engine.Engine()
        
    def tearDown(self):
        """Tear down the tests"""

    ### Basics ###
    
    def testCanCreate(self):
        """testCanCreate: should be able to create the engine"""
        pass

    def testCanFindCurrent(self):
        """testCanFindCurrent: should be able to find the current engine"""
        self.assertEqual(self.e, serge.engine.CurrentEngine())
    
    
    ### Adding ###
        
    def testCanAddWorld(self):
        """testCanAddWorld: should be able to add a world"""
        w = serge.world.World('test')
        self.e.addWorld(w)
    
    def testFailIfAddWorldTwice(self):
        """testFailIfAddWorldTwice: should fail if adding world twice"""
        w = serge.world.World('test')
        self.e.addWorld(w)
        self.assertRaises(serge.engine.DuplicateWorld, self.e.addWorld, w)
    
    def testFailIfAddSameNamedWorld(self):
        """testFailIfAddSameNamedWorld: should fail if adding a world with the same name"""
        w1 = serge.world.World('test')
        w2 = serge.world.World('test')
        self.e.addWorld(w1)
        self.assertRaises(serge.engine.DuplicateWorld, self.e.addWorld, w2)

    def testWorldKnowsEngine(self):
        """testWorldKnowsEngine: the world should know its engine"""
        w = serge.world.World('test')
        self.e.addWorld(w)
        self.assertEqual(self.e, w.engine)

    def testCanIterateWorlds(self):
        """testCanIterateWorlds: should be able to iterate through worlds"""
        w1 = serge.world.World('1')
        w2 = serge.world.World('2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.assertEqual(set(['1','2']), set([w.name for w in self.e.getWorlds()]))
        
       
    ### Removing ###
        
    def testCanRemoveWorld(self):
        """testCanRemoveWorld: should be able to remove a world"""
        w = serge.world.World('test')
        self.e.addWorld(w)
        self.e.removeWorld(w)
        self.assertRaises(serge.engine.WorldNotFound, self.e.getWorld, 'test')

    def testCanRemoveWorldByName(self):
        """testCanRemoveWorldByName: should be able to remove a world by name"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.removeWorldNamed('test2')
        self.assertEqual(w1, self.e.getWorld('test1'))
        self.assertRaises(serge.engine.WorldNotFound, self.e.getWorld, 'test2')

    def testClearWorlds(self):
        """testClearWorlds: should be able to clear all worlds"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.clearWorlds()
        self.assertRaises(serge.engine.WorldNotFound, self.e.getWorld, 'test1')
        self.assertRaises(serge.engine.WorldNotFound, self.e.getWorld, 'test2')    
        
    def testFailIfRemoveByNameNotPresent(self):
        """testFailIfRemoveByNameNotPresent: should fail if try to remove a world by name and it isn't present"""
        self.assertRaises(serge.engine.WorldNotFound, self.e.getWorld, 'test2')
        
    def testFailIfRemoveNonPresentWorld(self):
        """testFailIfRemoveNonPresentWorld: should fail if remove a world that isn't there"""
        w = serge.world.World('test')
        self.assertRaises(serge.engine.WorldNotFound, self.e.removeWorld, w)
        
    ### Getting ###
    
    def testCanGetWorld(self):
        """testCanGetWorld: should be able to get a world"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.assertEqual(w1, self.e.getWorld('test1'))
        self.assertEqual(w2, self.e.getWorld('test2'))
        
    def testFailIfGettingWorldNotThere(self):
        """testFailIfGettingWorldNotThere: should fail if trying to get a non-existent world"""
        w = serge.world.World('test')
        self.e.addWorld(w)
        self.assertRaises(serge.engine.WorldNotFound, self.e.getWorld, 'test-not')


    ### The current world ###
    
        
    def testCanSetTheCurrentWorld(self):
        """testCanSetTheCurrentWorld: should be able to set the current world"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        #
        self.e.setCurrentWorld(w1)
        self.assertEqual(w1, self.e.getCurrentWorld())
        self.e.setCurrentWorld(w2)
        self.assertEqual(w2, self.e.getCurrentWorld())
        
    def testCanSetCurrentWorldByName(self):
        """testCanSetCurrentWorldByName: should be able to set the current world by name"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        #
        self.e.setCurrentWorldByName('test1')
        self.assertEqual(w1, self.e.getCurrentWorld())
        self.e.setCurrentWorldByName('test2')
        self.assertEqual(w2, self.e.getCurrentWorld())
        
    def testCanGoBackToPreviousWorld(self):
        """testCanGoBackToPreviousWorld: should be able to go back to a previous world"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        w3 = serge.world.World('test3')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.addWorld(w3)
        #
        self.e.setCurrentWorldByName('test1')
        self.assertEqual(w1, self.e.getCurrentWorld())
        self.e.setCurrentWorldByName('test2')
        self.assertEqual(w2, self.e.getCurrentWorld())
        self.e.setCurrentWorld(w3)
        self.assertEqual(w3, self.e.getCurrentWorld())
        #
        # Go back
        self.e.goBackToPreviousWorld()
        self.assertEqual(w2, self.e.getCurrentWorld())
        self.e.setCurrentWorldByName('test1')
        self.assertEqual(w1, self.e.getCurrentWorld())
        self.e.goBackToPreviousWorld()
        self.assertEqual(w2, self.e.getCurrentWorld())
        self.e.goBackToPreviousWorld()
        self.assertEqual(w1, self.e.getCurrentWorld())
        
    def testFailGoBackWhenNoPrevious(self):
        """testFailGoBackWhenNoPrevious: should fail when going back and there is no previous world"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        w3 = serge.world.World('test3')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.addWorld(w3)
        self.assertRaises(serge.engine.WorldNotFound, self.e.goBackToPreviousWorld)

    def testShouldBeAbleToGetACallbackForWorld(self):
        """testShouldBeAbleToGetACallbackForWorld: should be able to get a callback to go to a world"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        w3 = serge.world.World('test3')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.addWorld(w3)
        #
        cb1 = serge.blocks.utils.worldCallback('test1')
        cb2 = serge.blocks.utils.worldCallback('test2')
        #
        cb1(1,2)
        self.assertEqual(w1, self.e.getCurrentWorld())
        cb2(1,2)
        self.assertEqual(w2, self.e.getCurrentWorld())
        cb1(1,2)
        self.assertEqual(w1, self.e.getCurrentWorld())

    def testAddingWorldDoesntChangeCurrentWorld(self):
        """testAddingWorldDoesntChangeCurrentWorld: adding a new world keeps the old current world"""
        w1 = serge.world.World('test1')
        w2 = serge.world.World('test2')
        self.e.addWorld(w1)
        self.e.setCurrentWorld(w1)
        self.e.addWorld(w2)
        self.assertEqual(w1, self.e.getCurrentWorld())

    def testAddingFirstWorldDoesntSetCurrentWorld(self):
        """testAddingFirstWorldDoesntSetCurrentWorld: when adding the first world the current should be still set"""
        w1 = serge.world.World('test1')
        self.e.addWorld(w1)
        self.assertRaises(serge.engine.NoCurrentWorld, self.e.getCurrentWorld)
        
    def testInitialCurrentWorldShouldFail(self):
        """testInitialCurrentWorldShouldFail: when no current world is set should fail"""
        self.assertRaises(serge.engine.NoCurrentWorld, self.e.getCurrentWorld)
        
    def testFailIfCurrentWorldIsRemoved(self):
        """testFailIfCurrentWorldIsRemoved: should fail when getting current world and it is removed"""
        w1 = serge.world.World('test1')
        self.e.addWorld(w1)
        self.e.removeWorld(w1)
        self.assertRaises(serge.engine.NoCurrentWorld, self.e.getCurrentWorld)
        
    def testFailIfSetWithInvalidWorld(self):
        """testFailIfSetWithInvalidWorld: should fail if set current world and not present"""
        w1 = serge.world.World('test1')
        self.assertRaises(serge.engine.WorldNotFound, self.e.setCurrentWorld, w1)
        
    def testFailIfSetByNameWithInvalidName(self):
        """testFailIfSetByNameWithInvalidName: should fail if set current world by name and not present"""
        w1 = serge.world.World('test1')
        self.e.addWorld(w1)
        self.assertRaises(serge.engine.WorldNotFound, self.e.setCurrentWorldByName, 'test1-not')
            
    ### Updating ###
    
    def testCanCallUpdate(self):
        """testCanCallUpdate: should be able to update the current world"""
        w1 = TestWorld('test1')
        w2 = TestWorld('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.setCurrentWorld(w2)
        self.e.updateWorld(1000)
        self.assertEqual(0, w1.counter)
        self.assertEqual(1000, w2.counter)
            
    def testFailUpdateIfNoCurrentWorld(self):
        """testFailUpdateIfNoCurrentWorld: should fail when updating and there is no current world"""
        self.assertRaises(serge.engine.NoCurrentWorld, self.e.updateWorld, 1000)
        
    def testCanRunForCycles(self):
        """testCanRunForCycles: should be able to run for a few cycles"""
        w1 = TestWorld('test1')
        w2 = TestWorld('test2')
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.setCurrentWorld(w2)
        self.e.run(fps=60, endat=time.time()+1)
        self.assertEqual(0, w1.reps)
        self.assert_(abs(w2.reps-60)<=5)
        self.assert_(abs(w2.counter-1000)<=50)
        
        
    def testCanStopRunning(self):
        """testCanStopRunning: should be able to stop running"""
        w1 = TestWorld('test1')
        w2 = TestWorld('test2', 30)
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.setCurrentWorld(w2)
        self.e.run(fps=60, endat=time.time()+1)
        self.assertEqual(0, w1.reps)
        self.assert_(abs(w2.reps-30)<=5)
        self.assert_(abs(w2.counter-500)<=50)
        
    def testCanRunAsync(self):
        """testCanRunAsync: can run the world in a thread"""
        w1 = TestWorld('test1')
        w2 = TestWorld('test2', 30)
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        self.e.setCurrentWorld(w1)
        self.e.runAsync(fps=60, endat=time.time()+5)
        for i in range(5):
            self.assert_(abs(w1.reps-61*i)<=10, 'Failed check on iteration %d, %d cf %d' % (i, w1.reps, 61*i))
            time.sleep(1)    
        time.sleep(3)
        self.assert_(abs(w1.reps-61*5)<=10, 'Failed check on end of iteration%d cf %d' % (w1.reps, 61*5))

    def testCanRunWithNoCurrentWorld(self):
        """testCanRunWithNoCurrentWorld: should be able to run even though there is no current world"""
        self.e.run(fps=60, endat=time.time()+1)
        
    def testCanAttachBuilder(self):
        """testCanAttachBuilder: should be able to attach a builder"""
        d = TestBuilder()
        self.e.attachBuilder(d)
        self.e.run(fps=60, endat=time.time()+1)
        self.assert_(abs(d.counter-60)<=5, 'Failed check on end of iteration%d cf %d' % (d.counter, 60))
        
    def testCanDetachBuilder(self):
        """testCanDetachBuilder: should be able to detach a builder"""
        d = TestBuilder()
        self.e.attachBuilder(d)
        self.e.detachBuilder()
        self.e.run(fps=60, endat=time.time()+1)
        self.assertEqual(0, d.counter)
        
    
    ### Serializing ###
    
    def testCanSerializeEngine(self):
        """testCanSerializeEngine: should be able to serialize the engine"""
        w1 = serge.world.World('one')
        z1=serge.zone.Zone()
        z1.setSpatial(1,2,3,4)
        w1.addZone(z1)        
        #
        w2 = serge.world.World('two')
        z2=serge.zone.Zone()
        z2.setSpatial(10,20,30,40)
        w2.addZone(z2)        
        #
        self.e.addWorld(w1)
        self.e.addWorld(w2)
        #
        l1 = serge.render.Layer('main', 10)
        l2 = serge.render.Layer('second', 20)
        self.e.getRenderer().addLayer(l1)
        self.e.getRenderer().addLayer(l2)
        #
        # Sprites
        serge.visual.Register.clearItems()
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('green', 'greenrect.png')        
        s = serge.visual.Register.getItem('green')
        #
        self.e.setCurrentWorldByName('two')
        #
        stored = self.e.asString()
        #
        # Make sure we clear all sprites
        serge.visual.Register.clearItems()
        serge.visual.Register.base_path = ''
        #
        e = serge.serialize.Serializable.fromString(stored)
        #
        self.assertEqual('one', e.getWorld('one').name)
        self.assertEqual('two', e.getWorld('two').name)
        self.assertEqual([1,2,3,4], list(list(e.getWorld('one').zones)[0].rect))
        self.assertEqual([10,20,30,40], list(list(e.getWorld('two').zones)[0].rect))
        #
        self.assertEqual(10, e.getRenderer().getLayer('main').order)
        self.assertEqual(20, e.getRenderer().getLayer('second').order)
        #
        s = serge.visual.Register.getItem('green')
        self.assertEqual(os.path.join(os.path.abspath(os.curdir), 'test', 'images'), serge.visual.Register.base_path)
        self.assertEqual('two', e.getCurrentWorld().name)


    ### Rendering ###
    
    def testCanRenderInTheRunMethod(self):
        """testCanRenderInTheRunMethod: should be able to render"""
        self.e = serge.engine.Engine()
        w1 = serge.world.World('one')
        z1=serge.zone.Zone()
        z1.setSpatial(0, 0, 200, 200)
        z1.active = True
        w1.addZone(z1)        
        self.e.addWorld(w1)
        #
        l1 = serge.render.Layer('main', 10)
        l2 = serge.render.Layer('second', 20)
        self.e.getRenderer().addLayer(l1)
        self.e.getRenderer().addLayer(l2)
        #
        # Sprites
        serge.visual.Register.clearItems()
        serge.visual.Register.setPath(os.path.join(os.path.abspath(os.curdir), 'test', 'images'))
        serge.visual.Register.registerItem('green', 'greenrect.png')        
        serge.visual.Register.registerItem('blue', 'bluerect.png')        
        #
        # Actors
        a1 = serge.actor.Actor('a')
        a1.setLayerName('main')
        a1.setSpriteName('green')
        a1.setSpatialCentered(60, 60, 50, 50)
        a2 = serge.actor.Actor('b')
        a2.setLayerName('second')
        a2.setSpriteName('blue')
        a2.setSpatialCentered(150, 150, 50, 50)
        w1.addActor(a1)
        w1.addActor(a2)
        #
        self.e.setCurrentWorldByName('one')
        #
        # Run for a bit
        self.e.run(60, time.time()+1)
        #
        # Now check rendered output
        self.checkRect(self.e.getRenderer().getSurface(), (0,255,0,255), 60, 60, 50, 50, 'green')
        self.checkRect(self.e.getRenderer().getSurface(), (0,0,255,255), 150, 150, 50, 50, 'blue')

    ### Handling events ###
    
    def _afterstop(self, obj, arg):
        """Event handler"""
        self._as = True
        
    def testCanHookStop(self):
        """testCanHookStop: can hook the stop event"""
        self.e = serge.engine.Engine()
        self._as = False
        self.e.linkEvent(serge.events.E_AFTER_STOP, self._afterstop)
        #
        self.assertFalse(self._as)
        self.e.runAsync(60)
        time.sleep(0.5)
        self.e.stop()
        time.sleep(0.5)
        self.assertTrue(self._as)
        
    def testCanHookBeforeStop(self):
        """testCanHookBeforeStop: should be able to hook before stopping"""
        self.e = serge.engine.Engine()
        self._as = False
        self.e.linkEvent(serge.events.E_BEFORE_STOP, self._afterstop)
        #
        self.assertFalse(self._as)
        self.e.runAsync(60)
        time.sleep(0.5)
        self.e.stop()
        time.sleep(0.5)
        self.assertTrue(self._as)
        
                    
        
class TestWorld(serge.world.World):
    def __init__(self, name, maxreps=1000):
        """Init"""
        super(TestWorld, self).__init__(name)
        self.counter = 0
        self.reps = 0
        self.maxreps = maxreps
        
    def updateWorld(self, interval):
        """Update me"""
        self.counter += interval        
        self.reps += 1
        if self.reps >= self.maxreps:
            self.engine.stop()
            
class TestBuilder():
    def __init__(self):
        self.counter = 0
        
    def updateBuilder(self, interval):
        """Update the builder"""
        self.counter += 1
        
    def renderTo(self, *args):
        """Render"""
        
if __name__ == '__main__':
    unittest.main()
