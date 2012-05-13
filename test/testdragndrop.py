"""Tests for drag and drop"""

import unittest
import os
import pygame

from helper import *

import serge.world
import serge.zone
import serge.actor
import serge.render

import serge.blocks.dragndrop
import serge.blocks.visualblocks

class TestDragNDrop(unittest.TestCase):
    """Tests for the DragNDrop"""

    def setUp(self):
        """Set up the tests"""
        self.c = serge.blocks.dragndrop.DragController()
        #
        # Some actors to be dragged
        self.a = serge.actor.Actor('a', 'a')
        self.b = serge.actor.Actor('b', 'b')
        #
        # Some drop targets
        self.d1 = serge.actor.Actor('d1', 'd1')
        self.d1.visual = serge.blocks.visualblocks.Rectangle((10, 10), (0,0,0,0))
        self.d1.moveTo(100, 100)
        self.d2 = serge.actor.Actor('d2', 'd2')
        self.d2.visual = serge.blocks.visualblocks.Rectangle((10, 10), (0,0,0,0))
        self.d2.moveTo(200, 200)
        #
        self.world = serge.world.World('main')
        self.z = serge.zone.Zone()
        self.z.active = True
        self.world.addZone(self.z)
        serge.engine.SetCurrentEngine(serge.engine.Engine())
        self.mouse = serge.engine.CurrentEngine()._mouse = FakeMouse()
        #
        # Add stuff to the world
        for actor in (self.a, self.b, self.c, self.d1, self.d2):
            self.world.addActor(actor)
        
    def tearDown(self):
        """Tear down the tests"""     

    def _start(self, obj, arg):
        """Start of drag"""
        self.start = True

    def _start_switch(self, obj, arg):
        """Start of drag"""
        return self.b
        
    def _stop(self, obj, arg):
        """Stop drag"""
        self.stop = True            

    def _drop(self, obj, arg):
        """Dropped on a target"""
        self.drop = obj, arg       
        
    def _drop_fail(self, obj, arg):
        """Dropped on a target but do not let it happen"""
        self.drop = obj, arg       
        raise serge.blocks.dragndrop.DropNotAllowed
    def _miss(self, obj):
        """Missed a drop"""
        self.miss = obj     

    def _miss_fail(self, obj):
        """Missed a drop but don't let the drop happen"""
        self.miss = 'ouch'
        raise serge.blocks.dragndrop.DropNotAllowed

    def testCanAddActor(self):
        """testCanAddActor: should be able to add an actor"""
        self.c.addActor(self.a)
        self.assertTrue(self.c.draggables.hasActor(self.a))
        
    def testFailAddDuplicate(self):
        """testFailAddDuplicate: should fail if adding a duplicate"""
        self.c.addActor(self.a)
        self.assertRaises(serge.blocks.dragndrop.DuplicateActor, self.c.addActor, self.a)        
        
    def testCanRemoveActor(self):
        """testCanRemoveActor: should be able to remove an actor"""
        self.c.addActor(self.a)
        self.c.removeActor(self.a)
        self.c.addActor(self.a)
        self.assertEqual(True, self.c.draggables.hasActor(self.a))
       
    def testCanStartToDrag(self):
        """testCanStartToDrag: should be able to start to drag"""
        self.c.addActor(self.a)
        self.a.moveTo(0, 0)
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        self.mouse.x = 10
        self.mouse.y = 20
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertTrue(self.c.isDragging())
        self.assertEqual(self.a, self.c.getDraggedActor())
        #
        self.mouse.x = 15
        self.mouse.y = 26
        self.world.updateWorld(100)
        #
        self.assertEqual(5, self.a.x)
        self.assertEqual(6, self.a.y)

    def testCanStopDragging(self):
        """testCanStopDragging: should be able to stop dragging"""
        self.c.addActor(self.a)
        self.a.moveTo(0, 0)
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        self.mouse.x = 10
        self.mouse.y = 20
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertTrue(self.c.isDragging())
        self.assertEqual(self.a, self.c.getDraggedActor())
        #
        self.mouse.x = 15
        self.mouse.y = 26
        self.world.updateWorld(100)
        #
        self.assertEqual(5, self.a.x)
        self.assertEqual(6, self.a.y)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.world.updateWorld(100)
        #
        self.assertEqual(5, self.a.x)
        self.assertEqual(6, self.a.y)
        #        
        self.mouse.x = 30
        self.mouse.y = 30
        self.world.updateWorld(100)
        self.assertEqual(5, self.a.x)
        self.assertEqual(6, self.a.y)
            
    def testOnlyOneActorShouldBeDragging(self):
        """testOnlyOneActorShouldBeDragging: only one actor at a time can be dragging"""
        self.c.addActor(self.a)
        self.c.addActor(self.b)
        self.a.moveTo(0, 0)
        self.b.moveTo(0, 0)
        self.assertFalse(self.c.isDragging())
        self.mouse.x = 10
        self.mouse.y = 20
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.b.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.b))
        self.assertEqual(self.a, self.c.getDraggedActor())
        self.assertTrue(self.c.isDragging())
        #
        self.mouse.x = 15
        self.mouse.y = 26
        self.world.updateWorld(100)
        #
        self.assertEqual(5, self.a.x)
        self.assertEqual(6, self.a.y)
        self.assertEqual(0, self.b.x)
        self.assertEqual(0, self.b.y)
        
    def testRemovedActorShouldNotDrag(self):
        """testRemovedActorShouldNotDrag: an actor should not be draggable when removed"""
        self.c.addActor(self.a)
        self.c.removeActor(self.a)
        self.a.moveTo(0, 0)
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        self.mouse.x = 10
        self.mouse.y = 20
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        #
        self.mouse.x = 15
        self.mouse.y = 26
        self.world.updateWorld(100)
        #
        self.assertEqual(0, self.a.x)
        self.assertEqual(0, self.a.y)
        
    def testCanTurnOffBehaviour(self):
        """testCanTurnOffBehaviour: should be able to turn off dragging"""
        self.c.addActor(self.a)
        self.a.moveTo(0, 0)
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        self.mouse.x = 10
        self.mouse.y = 20
        self.c.active = False
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        #
        self.mouse.x = 15
        self.mouse.y = 26
        self.world.updateWorld(100)
        #
        self.assertEqual(0, self.a.x)
        self.assertEqual(0, self.a.y)
        
    def testCanSpecifyDragStartAndStop(self):
        """testCanSpecifyDragStartAndStop: should be able to specify functions to call for start and stop"""
        self.c.addActor(self.a, self._start, self._stop)
        self.start = self.stop = False
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertTrue(self.start)
        self.assertFalse(self.stop)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertTrue(self.start)
        self.assertTrue(self.stop)

    def testCanSpecifyControllerLevelStartAndStop(self):
        """testCanSpecifyControllerLevelStartAndStop: can specify functions for callback at the controller level"""
        self.c.setCallbacks(self._start, self._stop)
        self.c.addActor(self.a)
        self.start = self.stop = False
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertTrue(self.start)
        self.assertFalse(self.stop)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertTrue(self.start)
        self.assertTrue(self.stop)

    def testCanSpecifyDroppable(self):
        """testCanSpecifyDroppable: should be able to specify something as a drop target"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.addDropTarget(self.d1, self._drop)
        self.c.addDropTarget(self.d2, self._drop)
        
    def testCanDropOntoTarget(self):
        """testCanDropOntoTarget: should be able to drop onto a target"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.addDropTarget(self.d1, self._drop)
        self.c.addDropTarget(self.d2, self._drop)
        self.a.moveTo(0, 0)
        self.drop = None
        self.mouse.x, self.mouse.y = 0, 0
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        #
        # Drag the actor
        self.mouse.x, self.mouse.y = 102, 102
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.d1.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual((self.d1, self.a), self.drop)
        #
        # Now move to second
        self.drop = None
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.mouse.x, self.mouse.y = 202, 202
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.d2.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual((self.d2, self.a), self.drop)
        
    def testCanMissTargetWithDrop(self):
        """testCanMissTargetWithDrop: should be able to miss target with drop"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.setDropCallbacks(None, self._miss)
        self.c.addDropTarget(self.d1, self._drop)
        self.c.addDropTarget(self.d2, self._drop)
        self.a.moveTo(0, 0)
        self.drop = None
        self.miss = None
        self.mouse.x, self.mouse.y = 0, 0
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        #
        # Drag the actor
        self.mouse.x, self.mouse.y = 50, 50
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual(None, self.drop)
        self.assertEqual(self.a, self.miss)
    
    def testCanCancelDropOnMiss(self):
        """testCanCancelDropOnMiss: should be able to cancel a drop on a miss"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.setDropCallbacks(None, self._miss_fail)
        self.c.addDropTarget(self.d1, self._drop)
        self.c.addDropTarget(self.d2, self._drop)
        self.a.moveTo(0, 0)
        self.drop = None
        self.miss = None
        self.mouse.x, self.mouse.y = 0, 0
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        #
        # Drag the actor
        self.mouse.x, self.mouse.y = 50, 50
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual(self.a, self.c.getDraggedActor())
        self.assertTrue(self.c.isDragging())
        
    def testCanCancelDropOnTarget(self):
        """testCanCancelDropOnTarget: should be able to cancel a drop on a hit"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.addDropTarget(self.d1, self._drop_fail)
        self.c.addDropTarget(self.d2, self._drop_fail)
        self.a.moveTo(0, 0)
        self.drop = None
        self.mouse.x, self.mouse.y = 0, 0
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        #
        # Drag the actor
        self.mouse.x, self.mouse.y = 102, 102
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.d1.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertTrue(self.c.isDragging())
        
       
    def testCanRemoveADropTarget(self):
        """testCanRemoveADropTarger: should be able to remove a drop target"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.addDropTarget(self.d1, self._drop)
        self.c.addDropTarget(self.d2, self._drop)
        self.c.removeDropTarget(self.d1)
        self.a.moveTo(0, 0)
        self.drop = None
        self.mouse.x, self.mouse.y = 0, 0
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        #
        # Drag the actor
        self.mouse.x, self.mouse.y = 102, 102
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.d1.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual(None, self.drop)
        
    def testFailRemoveMissingDrop(self):
        """testFailRemoveMissingDrop: should fail when removing a missing drop target"""
        self.assertRaises(serge.blocks.dragndrop.NotATarget, self.c.removeDropTarget, self.d1)
        
    def testFailAddDropTargetTwice(self):
        """testFailAddDropTargetTwice: should fail if adding a drop target twice"""
        self.c.addDropTarget(self.d1, self._drop)
        self.assertRaises(serge.blocks.dragndrop.AlreadyATarget, self.c.addDropTarget, self.d1, self._drop)        

    def testCanAddControllerLevelDropCallback(self):
        """testCanAddControllerLevelDropCallback: should be able to have a controller level drop callback"""
        self.c.addActor(self.a, self._start, self._stop)
        self.c.setDropCallbacks(self._drop, self._miss)
        self.c.addDropTarget(self.d1)
        self.c.addDropTarget(self.d2)
        self.a.moveTo(0, 0)
        self.drop = None
        self.mouse.x, self.mouse.y = 0, 0
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        #
        # Drag the actor
        self.mouse.x, self.mouse.y = 102, 102
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.d1.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual((self.d1, self.a), self.drop)
        #
        # Now move to second
        self.drop = None
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.mouse.x, self.mouse.y = 202, 202
        self.world.updateWorld(100)
        #
        self.a.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.d2.processEvent((serge.events.E_LEFT_CLICK, self.a))
        self.assertEqual((self.d2, self.a), self.drop)
        
    def testCanStartToDragAlteringObject(self):
        """testCanStartToDrag: should be able to start to drag and set a different object to drag"""
        self.c.addActor(self.a)
        self.c.setCallbacks(self._start_switch, None)
        self.a.moveTo(0, 0)
        self.b.moveTo(0, 0)
        self.assertFalse(self.c.isDragging())
        self.assertRaises(serge.blocks.dragndrop.NotDragging, self.c.getDraggedActor)
        self.mouse.x = 10
        self.mouse.y = 20
        self.a.processEvent((serge.events.E_LEFT_MOUSE_DOWN, self.a))
        self.assertTrue(self.c.isDragging())
        self.assertEqual(self.b, self.c.getDraggedActor())
        #
        self.mouse.x = 15
        self.mouse.y = 26
        self.world.updateWorld(100)
        #
        self.assertEqual(5, self.b.x)
        self.assertEqual(6, self.b.y)
        self.assertEqual(0, self.a.x)
        self.assertEqual(0, self.a.y)

    
if __name__ == '__main__':
    unittest.main()
