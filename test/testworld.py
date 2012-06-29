"""Tests for the World"""

import unittest

import serge.world
import serge.zone
import serge.actor
import serge.geometry
import serge.input
import serge.engine
import serge.events
import serge.render

class TestWorlds(unittest.TestCase):
    """Tests for the World"""

    def setUp(self):
        """Set up the tests"""
        self.w = TestWorld('test')
        self.z1 = TestZone()
        self.z2 = TestZone()
        self.z3 = TestZone()
        #
        self.a1 = TestActor()
        self.a1.tag = 'a'
        self.a1.name = 'a1'
        self.a2 = TestActor()
        self.a2.tag = 'a'
        self.a2.name = 'a2'
        self.b1 = TestActor()
        self.b1.tag = 'b'
        self.b1.name = 'b1'
        #
        self.z1.addActor(self.a1)
        self.z2.addActor(self.a2)
        #
        self.w2 = TestWorld('test2')
        #
        self.engine = serge.engine.Engine()
        self.engine.getRenderer().addLayer(serge.render.Layer('one', 0))
        self.engine.getRenderer().addLayer(serge.render.Layer('two', 0))

        
    def tearDown(self):
        """Tear down the tests"""

    ### Zones and updating ###
    
    def testSingleZoneUpdating(self):
        """testSingleZoneUpdating: a single zone should be able to update"""
        self.w.addZone(self.z1)
        self.z1.active = True
        self.w.updateWorld(100)
        self.assertEqual(100, self.z1.counter)
        self.assertEqual(0, self.z2.counter)
        self.assertEqual(0, self.z3.counter)

    def testSingleZoneNotActive(self):
        """testSingleZoneNotActive: a single inactive zone should not update"""
        self.w.addZone(self.z1)
        self.z1.active = False
        self.w.updateWorld(100)
        self.assertEqual(0, self.z1.counter)
        self.assertEqual(0, self.z2.counter)
        self.assertEqual(0, self.z3.counter)
                
    def testMultipleZonesOneUpdating(self):
        """testMultipleZonesOneUpdating: with multiple zones but only one active it should only update"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.addZone(self.z3)
        self.z1.active = True
        self.w.updateWorld(100)
        self.assertEqual(100, self.z1.counter)
        self.assertEqual(0, self.z2.counter)
        self.assertEqual(0, self.z3.counter)
        
    def testMultipleZonesTwoUpdating(self):
        """testMultipleZonesOneUpdating: with multiple zones and two active they should update"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.addZone(self.z3)
        self.z1.active = True
        self.z2.active = True
        self.w.updateWorld(100)
        self.assertEqual(100, self.z1.counter)
        self.assertEqual(100, self.z2.counter)
        self.assertEqual(0, self.z3.counter)

    def testFailIfAddAZoneTwice(self):
        """testFailIfAddAZoneTwice: should fail if adding a zone twice"""
        self.w.addZone(self.z1)
        self.assertRaises(serge.world.DuplicateZone, self.w.addZone, self.z1)

    ### Finding actors ###
    
    def testCanFindActorsByTag(self):
        """testCanFindActorsByTag: should be able to find actors by tag"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.assertEqual(set([self.a1, self.a2]), set(self.w.findActorsByTag('a')))
        self.assertEqual(set([]), set(self.w.findActorsByTag('b')))
        
    def testCanFindActorByName(self):
        """testCanFindActorByName: should be able to find an actor by name"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.assertEqual(self.a1, self.w.findActorByName('a1'))
        self.assertEqual(self.a2, self.w.findActorByName('a2'))
        
        
    def testFailFindByName(self):
        """testFailFindByName: should fail if try to find actor by name and not known"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.assertRaises(serge.zone.ActorNotFound, self.w.findActorByName, 'a3')
        
    def testCanGetAllActors(self):
        """testCanGetAllActors: should be able to get all actors"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.assertEqual(set([self.a1, self.a2]), set(self.w.getActors()))        
    
    def testActorsAreACollection(self):
        """testActorsAreACollection: the actors returned are an actor collection"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.assertEqual(self.a1, self.w.getActors().findActorByName('a1'))        
    
    ### Rezoning ###
    
    def testCanRezoneBasedOnSpace(self):
        """testCanRezoneBasedOnSpace: should be able to rezone objects"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        #
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 5, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        #
        self.assertEqual(set([self.a1]), self.z1.actors)
        self.assertEqual(set([self.a2]), self.z2.actors)
        self.w.rezoneActors()
        self.assertEqual(set([self.a2]), self.z1.actors)
        self.assertEqual(set([self.a1]), self.z2.actors)
        
    def testUnzonedActorsAreRetained(self):
        """testUnzonedActorsAreRetained: actors that are in no zone are retained and can come back"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        #
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 15, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        #
        self.assertEqual(set([self.a1]), self.z1.actors)
        self.assertEqual(set([self.a2]), self.z2.actors)
        self.w.rezoneActors()
        self.assertEqual(set([self.a2]), self.z1.actors)
        self.assertEqual(set([]), self.z2.actors) # a1 is in no zone
        #
        self.a1.setSpatial(15, 5, 3, 3)
        self.w.rezoneActors()
        self.assertEqual(set([self.a2]), self.z1.actors)
        self.assertEqual(set([self.a1]), self.z2.actors) # a1 comes back
        
    def testUnzonedActorsAreNotUpdated(self):
        """testUnzonedActorsAreNotUpdated: unzoned actors are not updated"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        #
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 15, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        #
        self.assertEqual(set([self.a1]), self.z1.actors)
        self.assertEqual(set([self.a2]), self.z2.actors)
        self.w.rezoneActors()
        # Now a1 is not zoned
        self.z1.active = self.z2.active = True
        self.w.updateWorld(100)
        self.assertEqual(100, self.a2.counter)
        self.assertEqual(0, self.a1.counter)                
            
    ### Adding and removing actors directly ###

    def testCanClearActors(self):
        """testCanClearActors: should be able to clear all actors"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.addZone(self.z3)
        self.w.clearActors()
        self.assertEqual(0, len(self.z1.actors))
        self.assertEqual(0, len(self.z2.actors))
        self.assertEqual(0, len(self.z3.actors))
        self.assertEqual(0, len(self.w.unzoned_actors))

    def testCanClearActorsExceptTags(self):
        """testCanClearActorsExceptTags: should be able to clear actors except those with some tags"""
        self.a3 = TestActor()
        self.z3.addActor(self.a3)
        self.a3.tag = 'c'
        self.a2.tag = 'b'
        self.a1.tag = 'a'
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.addZone(self.z3)
        self.w.clearActorsExceptTags(['a', 'c'])
        self.assertEqual(1, len(self.z1.actors))
        self.assertEqual(0, len(self.z2.actors))
        self.assertEqual(1, len(self.z3.actors))
        self.assertEqual(0, len(self.w.unzoned_actors))
        
    def testCanClearActorsWithTag(self):
        """testCanClearActorsWithTag: should be able to clear actors with a tag"""
        self.a3 = TestActor()
        self.z3.addActor(self.a3)
        self.a3.tag = 'c'
        self.a2.tag = 'a'
        self.a1.tag = 'a'
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.addZone(self.z3)
        self.w.clearActorsWithTags(['a'])
        self.assertEqual(1, len(self.z3.actors))
        self.assertEqual(0, len(self.z2.actors))
        self.assertEqual(0, len(self.z1.actors))
        self.assertEqual(0, len(self.w.unzoned_actors))
        
        
    
    def testCanAddActorUnzoned(self):
        """testCanAddActorUnzoned: should be able to add an actor and it will be unzoned"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 15, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.assertEqual(set([self.a1]), self.w.unzoned_actors)
        
    def testCanAddActorIntoZone(self):
        """testCanAddActorIntoZone: should be able to add an actor and it will go into a relevant zone"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 5, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.assertEqual(set([]), self.w.unzoned_actors)
        self.assertEqual(set([]), self.z1.actors)
        self.assertEqual(set([self.a1]), self.z2.actors)
        self.assertEqual(set([]), self.z3.actors)

    def testCanAddActorIntoTaggedZones(self):
        """testCanAddActorIntoTaggedZones: should be able to add actors into zones by tag"""
        z1 = serge.zone.TagIncludeZone(['a'])
        z2 = serge.zone.TagIncludeZone(['b'])
        z1.active = z2.active = True
        self.w.addZone(z1)
        self.w.addZone(z2)
        self.w.addActor(self.a1)
        self.w.addActor(self.a2)
        self.w.addActor(self.b1)
        #
        # Actors should have gone to the right zones
        self.assertTrue(z1.hasActor(self.a1))
        self.assertTrue(z1.hasActor(self.a2))
        self.assertTrue(z2.hasActor(self.b1))
    
        
    def testCanRemoveActorUnzoned(self):
        """testCanRemoveActorUnzoned: can remove an actor that isn't in a zone"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 15, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.w.removeActor(self.a1)
        self.assertEqual(set([]), self.w.unzoned_actors)
        
    def testCanRemoveActorInZone(self):
        """testCanRemoveActorInZone: can remove an actor that is in a zone"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 5, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.w.removeActor(self.a1)
        self.assertEqual(set([]), self.w.unzoned_actors)
        self.assertEqual(set([]), self.z1.actors)
        self.assertEqual(set([]), self.z2.actors)
        self.assertEqual(set([]), self.z3.actors)
        
    def testFailRemoveUnknownActor(self):
        """testFailRemoveUnknownActor: should fail if remove an actor that is not known"""
        self.w.clearActors()
        self.assertRaises(serge.world.UnknownActor, self.w.removeActor, self.a1)
        
    def testFailIfAddActorAlreadyInAZone(self):
        """testFailIfAddActorAlreadyInAZone: should fail if add an actor that is already in a zone"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.addZone(self.z3)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 5, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.assertRaises(serge.world.DuplicateActor, self.w.addActor, self.a1)      
        
    def testFailIfAddActorAlreadyInNoZone(self):
        """testFailIfAddActorAlreadyInNoZone: should fail if add an actor that is not zoned"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z2.setSpatial(10, 0, 10, 10)
        self.a1.setSpatial(15, 15, 3, 3)
        self.a2.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.assertRaises(serge.world.DuplicateActor, self.w.addActor, self.a1)      
        
    def testCanAddActorDuringUpdate(self):
        """testCanAddActorDuringUpdate: should be able to add an actor during an update"""
        self.w.addZone(self.z1)
        self.w.clearActors()
        self.z1.setSpatial(0, 0, 10, 10)
        self.z1.active = True
        self.a1 = TestAddingActor('test')
        self.a1.setSpatial(5, 5, 3, 3)
        self.w.addActor(self.a1)
        self.w.updateWorld(100)

    def testRemovingActorNotification(self):
        """testRemovingActorNotification: removing an actor should give the actor a chance to respond"""
        self.w.addZone(self.z1)
        self.z1.active = True        
        self.w.removeActor(self.a1)
        #
        # Should have seen this
        self.assertEqual(True, self.a1.was_removed)

    def testAddingActorNotification(self):
        """testAddingActorNotification: should get notification when an actor is added to the world"""
        self.w.addZone(self.z1)
        self.z1.removeActor(self.a1)
        self.w.addActor(self.a1)
        #
        # Should have seen this
        self.assertEqual(True, self.a1.was_added)
        
    def testCanScheduleDeletion(self):
        """testCanScheduleDeletion: should be able to schedule deletion of an object"""
        self.w.addZone(self.z1)
        self.assertTrue(self.w.hasActor(self.a1))
        self.w.scheduleActorRemoval(self.a1)
        self.assertTrue(self.w.hasActor(self.a1))
        self.w.updateWorld(1000)
        self.assertFalse(self.w.hasActor(self.a1))
                
    def testScheduleDeletionAllowsDuplicates(self):
        """testScheduleDeletionAllowsDuplicates: should be able to have duplicate deletions when scheduled"""
        self.w.addZone(self.z1)
        self.assertTrue(self.w.hasActor(self.a1))
        self.w.scheduleActorRemoval(self.a1)
        self.w.scheduleActorRemoval(self.a1)
        self.assertTrue(self.w.hasActor(self.a1))
        self.w.updateWorld(1000)
        self.assertFalse(self.w.hasActor(self.a1))
        
    def testCanScheduleAndRemoveActorDirectly(self):
        """testCanScheduleAndRemoveActorDirectly: should be able to directly remove scheduled actor"""
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        self.assertTrue(self.w.hasActor(self.a1))
        self.assertTrue(self.w.hasActor(self.a2))
        #
        # Schedule a1 and directly a2
        self.w.scheduleActorRemoval(self.a1)
        self.w.removeActor(self.a2)
        #
        # Now reverse        
        self.w.removeActor(self.a1)
        self.w.scheduleActorRemoval(self.a2)
        #
        # Should be gone
        self.assertFalse(self.w.hasActor(self.a1))
        self.assertFalse(self.w.hasActor(self.a2))
        #
        # Do it
        self.w.updateWorld(1000)
        self.assertFalse(self.w.hasActor(self.a1))
        self.assertFalse(self.w.hasActor(self.a2))

    def testScheduledDeletionCallsRemoveActor(self):
        """testScheduledDeletionCallsRemoveActor: should still call remove actor event when scheduled"""
        self.w.addZone(self.z1)
        self._sched_done = 0
        self.a1.linkEvent(serge.events.E_REMOVED_FROM_WORLD, self._sched1)        
        self.w.scheduleActorRemoval(self.a1)
        self.w.updateWorld(1000)
        #
        # Should have called the event only once
        self.assertEqual(1, self._sched_done)
        
    def testRemovedFromWorldEventIsAfterRemoval(self):
        """testRemovedFromWorldEventIsAfterRemoval: event should only fire when the actor is really gone"""
        def checkIt(o, a):
            self.assertFalse(self.w.hasActor(self.a1))
        #
        self.w.addZone(self.z1)
        self._sched_done = 0
        self.a1.linkEvent(serge.events.E_REMOVED_FROM_WORLD, checkIt)        
        self.w.removeActor(self.a1)
        
    
                
    def _sched1(self, obj, arg):
        """Routed to mark event"""
        self._sched_done += 1
        
        
    ### Testing for mouse hits ###
    
    def testCanGetMouseHit(self):
        """testCanGetMouseHit: should be able to detect mouse hit"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.a2.setSpatial(100, 50, 20, 51)
        self.w.addZone(self.z1)
        self.w.addZone(self.z2) 
        self.a1.setLayerName('one')
        self.a2.setLayerName('one')
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        x, y = 55, 105
        mouse._actors_under_mouse = None
        events = mouse.getActorEvents(self.w)
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a1)]), set(events))
        mouse.current_mouse_state.setState(serge.input.M_RIGHT, True)
        mouse._actors_under_mouse = None
        events = mouse.getActorEvents(self.w)
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a1), ('right-mouse-down', self.a1)]), set(events))
        #
        x, y = 105, 55
        mouse.current_mouse_state.setState(serge.input.M_RIGHT, False)
        mouse._actors_under_mouse = None
        events = mouse.getActorEvents(self.w)
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a2)]), set(events))
        x, y = 100, 100
        mouse._actors_under_mouse = None
        events = mouse.getActorEvents(self.w)
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a1), (serge.events.E_LEFT_MOUSE_DOWN, self.a2)]), set(events))

    def testCanGetMouseClick(self):
        """testCanGetMouseClick: should be able to detect a mouse click"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.a2.setSpatial(100, 50, 20, 51)
        self.w.addZone(self.z1)
        self.w.addZone(self.z2) 
        #
        self.a1.setLayerName('one')
        self.a2.setLayerName('one')
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, False)
        mouse.previous_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        x, y = 55, 105
        events = mouse.getActorEvents(self.w)
        self.assertEquals(set([(serge.events.E_LEFT_CLICK, self.a1)]), set(events))

    def testCanSeeMouseMiss(self):
        """testCanSeeMouseMiss: should be able to detect a mouse miss"""
        self.a1.setSpatial(50, 100, 50, 30)
        self.a2.setSpatial(100, 50, 20, 50)
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        x, y = 49, 49
        events = mouse.getActorEvents(self.w)
        self.assertEquals(set([]), set(events))
        
    def testCanFilterHitsByLayers(self):
        """testCanFilterHitsByLayers: should be able to filter the layers that a mouse event affects"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.a2.setSpatial(100, 50, 20, 51)
        self.w.addZone(self.z1)
        self.w.addZone(self.z2) 
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        self.a1.layer = 'one'
        self.a2.layer = 'two'
        #
        x, y = 100, 100
        events = mouse.getActorEvents(self.w, ['one'])
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a1)]), set(events))
        events = mouse.getActorEvents(self.w, ['two'])
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a2)]), set(events))
        events = mouse.getActorEvents(self.w, ['one', 'two'])
        self.assertEquals(set([(serge.events.E_LEFT_MOUSE_DOWN, self.a1), (serge.events.E_LEFT_MOUSE_DOWN, self.a2)]), set(events))
        
       
    ### Handling events ###
    
    def testCanHandleMouseClick(self):
        """testCanHandleMouseClick: should be able to handle mouse click events"""
        self.w.processEvents([((serge.events.E_LEFT_CLICK, 'mouse'), self.a1)])
        self.assertEqual((serge.events.E_LEFT_CLICK, 'mouse'), self.a1.action)
        self.assertEqual(None, self.a2.action)

    def testClicksDontAffectInactiveActors(self):
        """testClicksDontAffectInactiveActors: an inactive actor should ignore an event"""
        self.a1.active = False
        self.w.processEvents([((serge.events.E_LEFT_CLICK, 'mouse'), self.a1)])
        self.assertEqual(None, self.a1.action)
        self.assertEqual(None, self.a2.action)
        
    def testEngineCanHandleMouseEvents(self):
        """testEngineCanHandleMouseEvents: engine should be able to handle mouse events"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.a2.setSpatial(100, 50, 20, 51)
        self.w.addZone(self.z1)
        self.w.addZone(self.z2) 
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        mouse.getStaticScreenPos = lambda : (x, y)
        #
        self.a1.layer = 'one'
        self.a2.layer = 'two'
        #
        x, y = 55, 100
        #
        engine.addWorld(self.w)
        engine.setCurrentWorld(self.w)
        engine._mouse = mouse
        engine.processEvents()
        #
        self.assertEqual(serge.events.E_LEFT_MOUSE_DOWN, self.a1.action[0])
        self.assertEqual(mouse, self.a1.action[1])
        self.assertEqual(None, self.a2.action)
        
    def testEngineCanAutoLinkEvents(self):
        """testEngineCanAutoLinkEvents: should be able to automatically link events to a callback"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.w.addZone(self.z1)
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        self.a1.layer = 'one'
        x, y = 55, 100
        #
        global test
        test = 0
        def doit(obj, x):
            global test
            test += x
        #
        # Link events
        self.a1.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, doit, 10)
        #
        engine.addWorld(self.w)
        engine.setCurrentWorld(self.w)
        engine._mouse = mouse
        engine.processEvents()
        #
        self.assertEqual(10, test)
        
    def testEngineCanDelinkEvents(self):
        """testEngineCanDelinkEvents: should be able to delink events from callbacks"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.w.addZone(self.z1)
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        self.a1.layer = 'one'
        x, y = 55, 100
        #
        global test
        test = 0
        def doit(obj, x):
            global test
            test += x
        #
        # Link events
        self.a1.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, doit, 10)
        self.a1.unlinkEvent(serge.events.E_LEFT_MOUSE_DOWN)
        #
        engine.addWorld(self.w)
        engine.setCurrentWorld(self.w)
        engine._mouse = mouse
        engine.processEvents()
        #
        self.assertEqual(0, test)
        self.assertEqual(serge.events.E_LEFT_MOUSE_DOWN, self.a1.action[0])
        self.assertEqual(mouse, self.a1.action[1])
        
    def testEngineCallsWorldWhenSelecting(self):
        """testEngineCallsWorldWhenSelecting: enging should call method on world when selecting it"""
        self.assertEqual(0, self.w.activations)
        self.assertEqual(0, self.w.deactivations)
        #
        engine = serge.engine.Engine()
        #
        # Adding should do nothing
        engine.addWorld(self.w)
        engine.addWorld(self.w2)
        self.assertEqual(0, self.w.activations)
        #
        # Setting current should activate
        engine.setCurrentWorld(self.w)
        self.assertEqual(1, self.w.activations)
        self.assertEqual(0, self.w.deactivations)
        #
        # Setting again should do nothing
        engine.setCurrentWorld(self.w)
        self.assertEqual(1, self.w.activations)
        self.assertEqual(0, self.w.deactivations)
        #
        # Another world
        engine.setCurrentWorld(self.w2)
        self.assertEqual(1, self.w.activations)
        self.assertEqual(1, self.w.deactivations)
        self.assertEqual(1, self.w2.activations)
        #
        # And back
        engine.setCurrentWorld(self.w)
        self.assertEqual(2, self.w.activations)
        self.assertEqual(1, self.w.deactivations)
        self.assertEqual(1, self.w2.deactivations)

    def testCanConsumeMouseEvent(self):
        """testCanConsumeMouseEvent: should be able to consume a mouse event to prevent others seeing it"""
        self.a1.setSpatial(50, 100, 51, 30)
        self.a2.setSpatial(50, 100, 51, 30)
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        self.a1.layer = 'one'
        self.a2.layer = 'one'
        x, y = 55, 100
        #
        global test, consume
        test = 0
        consume = False
        def doit(obj, x):
            global test
            test += x
            if consume:
                return serge.events.E_LEFT_MOUSE_DOWN
            else:
                return None
        #
        # Link events
        self.a1.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, doit, 10)
        self.a2.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, doit, 1)
        #
        # First non consuming
        engine.addWorld(self.w)
        engine.setCurrentWorld(self.w)
        engine._mouse = mouse
        engine.processEvents()
        #
        # Should fire twice
        self.assertEqual(11, test)
        #
        # Now with consuming - only one of the events should work
        consume = True
        test = 0
        engine.processEvents()
        self.assertTrue(test in (1, 10))
        
    def testStaticZonedActorsAreHandledFirst(self):
        """testStaticZonedActorsAreHandledFirst: should be able to specify an event handler as important by putting on static"""
        # Here is the key to ordering the event listeners
        self.engine.getRenderer().getLayer('two').setStatic(True)
        #
        self.a1.setSpatial(0, 0, 1000, 1000)
        self.a2.setSpatial(0, 0, 1000, 1000)
        self.w.addZone(self.z1)
        self.w.addZone(self.z2)
        engine = self.engine
        mouse = serge.input.Mouse(engine)
        # Fake a click
        mouse.current_mouse_state.setState(serge.input.M_LEFT, True)
        mouse.getScreenPos = lambda : (x, y)
        #
        self.a1.layer = 'one'
        self.a2.layer = 'two'
        x, y = 55, 100
        #
        global test, consume
        test = 0
        consume = True
        def doit(obj, x):
            global test
            test += x
            if consume:
                return serge.events.E_LEFT_MOUSE_DOWN
            else:
                return None
        #
        # Link events - normally a2 would fire first being the last
        # registered but since a2 is on a static layer now it will be the first
        self.a1.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, doit, 10)
        self.a2.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, doit, 1)
        #
        # First non consuming
        engine.addWorld(self.w)
        engine.setCurrentWorld(self.w)
        engine._mouse = mouse
        engine.processEvents()
        self.assertEqual(1, test)        


    ### World Events ###
    
    def testCanHookWorldActivated(self):
        """testCanHookWorldActivated: should be able to hook world activated"""
        #
        # Callback to remember stuff
        def doit(obj, arg):
            doit.a = obj
            doit.b = arg
        #
        # Construct the engine and worlds neede
        e = serge.engine.Engine()
        w1 = TestWorld('1')
        w2 = TestWorld('2')
        e.addWorld(w1)
        e.addWorld(w2)
        #
        # Link events
        w1.linkEvent(serge.events.E_ACTIVATE_WORLD, doit, 1)
        w2.linkEvent(serge.events.E_ACTIVATE_WORLD, doit, 2)
        #
        # Should be able to point to 1
        e.setCurrentWorld(w1)
        self.assertEqual(w1, doit.a)
        self.assertEqual(1, doit.b)
        #
        # Should be able to point to 2
        e.setCurrentWorld(w2)
        self.assertEqual(w2, doit.a)
        self.assertEqual(2, doit.b)
        #
        # After unlinking should point to 2
        w1.unlinkEvent(serge.events.E_ACTIVATE_WORLD)
        e.setCurrentWorld(w1)
        self.assertEqual(w2, doit.a)
        self.assertEqual(2, doit.b)
        
    def testCanHookWorldDeactivated(self):
        """testCanHookWorldDeactivated: should be able to hook when the world is deactivated"""
        #
        # Callback to remember stuff
        def doit(obj, arg):
            doit.a = obj
            doit.b = arg
        #
        # Construct the engine and worlds neede
        e = serge.engine.Engine()
        w1 = TestWorld('1')
        w2 = TestWorld('2')
        e.addWorld(w1)
        e.addWorld(w2)
        #
        # Link events
        w1.linkEvent(serge.events.E_DEACTIVATE_WORLD, doit, 1)
        w2.linkEvent(serge.events.E_DEACTIVATE_WORLD, doit, 2)
        #
        # Nothing happens on link
        e.setCurrentWorld(w1)
        #
        # When 1 is deactivated should go to 1
        e.setCurrentWorld(w2)
        self.assertEqual(w1, doit.a)
        self.assertEqual(1, doit.b)
        #
        # Then the same for 2
        e.setCurrentWorld(w1)        
        self.assertEqual(w2, doit.a)
        self.assertEqual(2, doit.b)
        
    def testCanHookPreRender(self):
        """testCanHookPreRender: should be able to hook before rendering"""
        self.w.addZone(self.z1)
        r = serge.render.Renderer()
        #
        # Callback to check stuff
        def doit(obj, arg):
            doit.called = True
            self.assertEqual(obj, self.w)
            self.assertEqual(0, self.a1.rendered)
            self.assertEqual(1, arg)
        #
        # Hook into the pre-render
        self.w.linkEvent(serge.events.E_BEFORE_RENDER, doit, 1)
        self.w.renderTo(r, 0)
        #
        self.assertEqual(True, doit.called)
        
        
    def testCanHookPostRendering(self):
        """testCanHookPostRendering: should be able to hook after rendering"""
        self.w.addZone(self.z1)
        self.z1.active = True
        self.a1.active = True
        e = serge.engine.Engine()
        #
        # Callback to check stuff
        def doit(obj, arg):
            doit.called = True
            self.assertEqual(obj, self.w)
            self.assertEqual(1, self.a1.rendered)
            self.assertEqual(1, arg)
        #
        # Hook into the pre-render
        self.w.linkEvent(serge.events.E_AFTER_RENDER, doit, 1)
        self.w.renderTo(e.getRenderer(), 0)
        #
        self.assertEqual(True, doit.called)
        
              

class TestWorld(serge.world.World):
    """A simple test world"""
    
    def __init__(self, *args, **kw):
        """Initialise the TestWorld"""
        super(TestWorld, self).__init__(*args, **kw)
        self.activations = 0
        self.deactivations = 0
        
    def activateWorld(self):
        """Called when the world is set as the current world"""
        super(TestWorld, self).activateWorld()
        self.activations += 1
                
    def deactivateWorld(self):
        """Called when the world is deactivated"""
        super(TestWorld, self).deactivateWorld()
        self.deactivations += 1


        
class TestZone(serge.zone.Zone):
    def __init__(self):
        """Initialise"""
        super(TestZone, self).__init__()
        self.counter = 0
        self.spatial = serge.geometry.Point(0, 0)
        
    def updateZone(self, interval, world):
        """Update the zone"""
        self.counter += interval 
        super(TestZone, self).updateZone(interval, world)   

class TestActor(serge.actor.Actor):
    def __init__(self):
        """Initialise"""
        super(TestActor, self).__init__('', '')
        self.counter = 0
        self.action = None
        self.was_removed = False
        self.was_added = False
        self.rendered = 0
    
    def updateActor(self, interval, world):
        """Update the actor"""
        self.counter += interval  

    def handleEvent(self, event):
        """Handle a named event"""
        self.action = event    

    def removedFromWorld(self, world):
        """Remove us from the world"""
        super(TestActor, self).removedFromWorld(world)
        self.was_removed = True

    def addedToWorld(self, world):
        """Added us to the world"""
        self.was_added = True

    def renderTo(self, *args):
        """Being rendered"""
        self.rendered += 1

class TestAddingActor(serge.actor.Actor):
    """An actor that tries to add another during an update"""
    
    def updateActor(self, interval, world):
        """Update the actor"""
        new = TestAddingActor('new')
        world.addActor(new)



if __name__ == '__main__':
    unittest.main()
