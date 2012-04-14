"""Tests for Zone"""

import unittest
import pygame

import serge.zone
import serge.actor
import serge.geometry
import serge.render
import serge.world

class TestZones(unittest.TestCase):
    """Tests for the Zone"""

    def setUp(self):
        """Set up the tests"""
        self.w = serge.world.World('test')
        self.z1 = TestZone()
        self.z2 = TestZone()
        self.z3 = TestZone()
        self.a1 = TestActor()
        self.a2 = TestActor()
        
        
    def tearDown(self):
        """Tear down the tests"""


    ### Zones updating actors ###
    
    def testAnActiveZoneShouldUpdateActors(self):
        """testAnActiveZoneShouldUpdateActors: when updating a zone it should update its actors"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.z1.updateZone(100, None)
        self.assertEqual(100, self.a1.counter)
        self.assertEqual(100, self.a2.counter)
 
    def testInactiveActorsShouldNotUpdate(self):
        """testInactiveActorsShouldNotUpdate: should not update inactive actors in a zone"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.a1.active = False
        self.z1.updateZone(100, None)
        self.assertEqual(0, self.a1.counter)
        self.assertEqual(100, self.a2.counter)
        
           
    ### Adding and removing actors ###
    
    def testCanAddActor(self):
        """testCanAddActor: should be able to add an actor"""
        self.z1.addActor(self.a1)
        
    def testFailAddActorMultiple(self):
        """testFailAddActorMultiple: should fail if adding an actor multiple times"""
        self.z1.addActor(self.a1)
        self.assertRaises(serge.zone.DuplicateActor, self.z1.addActor, self.a1)
        
    def testCanRemoveActor(self):
        """testCanRemoveActor: should be able to remove actor"""
        self.z1.addActor(self.a1)
        self.z1.removeActor(self.a1)
        self.z1.addActor(self.a1)
        
    def testFailRemoveActorNotThere(self):
        """testFailRemoveActorNotThere: should fail if removing an actor that is not there"""
        self.assertRaises(serge.zone.ActorNotFound, self.z1.removeActor, self.a1)
        
    def testCanClearActors(self):
        """testCanClearActors: should be able to clear all actors"""
        self.z1.addActor(self.a1)
        self.z1.clearActors()
        self.assertEqual(0, len(self.z1.actors))
        
    
    ### Finding actors ###
    
    def testCanFindActorByTag(self):
        """testCanFindActorByTag: should be able to find a single actor with a tag"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.a1.tag = 'a'
        self.assertEqual([self.a1], self.z1.findActorsByTag('a'))
        self.assertEqual([], self.z1.findActorsByTag('b'))

    def testCanFindFirstActorByTag(self):
        """testCanFindFirstActorByTag: should be able to find the first actor with a tag"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.a1.tag = 'a'
        self.a2.tag = 'a'
        self.assert_(self.z1.findFirstActorByTag('a') in (self.a1, self.a2))

    def testFailFindFirstActorByTag(self):
        """testFailFindFirstActorByTag: should fail when finding first actor and none found"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.a1.tag = 'a'
        self.a2.tag = 'a'
        self.assertRaises(serge.zone.ActorNotFound, self.z1.findFirstActorByTag, 'b')

    def testCanFindActorsByTag(self):
        """testCanFindActorsByTag: should be able to find actors with a tag"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.a1.tag = 'a'
        self.a2.tag = 'a'
        self.assertEqual(set([self.a1, self.a2]), set(self.z1.findActorsByTag('a')))
        self.assertEqual([], self.z1.findActorsByTag('b'))
               
    def testCanFindActorByName(self):
        """testCanFindActorByName: should be able to find an actor by name"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.a1.name = 'a'
        self.assertEqual(self.a1, self.z1.findActorByName('a'))

    def testFailToFindActorByName(self):
        """testFailToFindActorByName: should fail if finding by name and not found"""
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.assertRaises(serge.zone.ActorNotFound, self.z1.findActorByName, 'a')

    def testCanTestActorContainment(self):
        """testCanTestActorContainment: should be able to check if an actor is in a zone"""
        self.assertEqual(False, self.z1.hasActor(self.a1))
        self.z1.addActor(self.a1)
        self.assertEqual(True, self.z1.hasActor(self.a1))
        
            
    ### Spatial containment ###
    
    def testCanCheckIfLocationInZone(self):
        """testCanCheckIfLocationInZone: should be able to check if a location is in a zone"""
        self.z1.spatial = serge.geometry.Rectangle(-10, -10, 20, 20)
        self.a1.spatial = serge.geometry.Rectangle(5, 5, 1, 1)
        self.a2.spatial = serge.geometry.Rectangle(15, 15, 1, 1)
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.assertEqual(True, self.a1.spatial.isInside(self.z1.spatial))
        self.assertEqual(False, self.a2.spatial.isInside(self.z1.spatial))

    def testContainmentWorksForPartial(self):
        """testContainmentWorksForPartial: should be able to check containment for things on the edge"""
        self.z1.spatial = serge.geometry.Rectangle(-10, -10, 20, 20)
        self.a1.spatial = serge.geometry.Rectangle(5, 5, 100, 100)
        self.a2.spatial = serge.geometry.Rectangle(15, 15, 100, 100)
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        self.assertEqual(True, self.a1.spatial.isOverlapping(self.z1.spatial))
        self.assertEqual(False, self.a2.spatial.isOverlapping(self.z1.spatial))

    def testInitialZoneSize(self):
        """testInitialZoneSize: initial zone size should be big"""
        self.assertEqual([-1000, -1000, 2000, 2000], list(self.z1.getSpatial()))
        
            
                    
    ### Rendering ###
    
    def testCanRenderToLayer(self):
        """testCanRenderToLayer: should be able to render to a layer"""
        self.a1.active = self.a2.active = True
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        r = serge.render.Renderer()
        self.a1.visual = TestVisual('one', r)
        self.a1.setLayerName('one')
        self.a2.setLayerName('one')
        self.a2.visual = TestVisual('one', r)
        l = TestLayer('one', 0)
        r.addLayer(l)
        self.w.addZone(self.z1)
        self.w.renderTo(r, 0)
        self.assertEqual(set([self.a1.visual, self.a2.visual]), set(l.renders))
        
    def testCanRenderToMultipleLayers(self):
        """testCanRenderToMultipleLayers: should be able to render to multiple layers"""
        self.a1.active = self.a2.active = True
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        r = serge.render.Renderer()
        self.a1.visual = TestVisual('one', r)
        self.a2.visual = TestVisual('two', r)
        self.a1.setLayerName('one')
        self.a2.setLayerName('two')
        l1 = TestLayer('one', 0)
        l2 = TestLayer('two', 0)
        r.addLayer(l1)
        r.addLayer(l2)
        self.w.addZone(self.z1)
        self.w.renderTo(r, 0)
        self.assertEqual([self.a1.visual], l1.renders)
        self.assertEqual([self.a2.visual], l2.renders)
       
    def testFailIfRenderingToLayerNotFound(self):
        """testFailIfRenderingToLayerNotFound: should fail when rendering to a non-existent layer"""
        self.a1.active = self.a2.active = True
        self.a1.setLayerName('bad')
        self.z1.addActor(self.a1)
        r = serge.render.Renderer()
        self.a1.visual = TestVisual('aaa', r)
        l = TestLayer('one', 0)
        r.addLayer(l)
        self.w.addZone(self.z1)
        self.assertRaises(serge.render.UnknownLayer, self.w.renderTo, r, 0)
       
    def testInactiveActorsShouldNotRender(self):
        """testInactiveActorsShouldNotRender: should not render actors that are not active"""
        self.a1.active = self.a2.active = True
        self.z1.addActor(self.a1)
        self.z1.addActor(self.a2)
        r = serge.render.Renderer()
        self.a1.visual = TestVisual('one', r)
        self.a2.visual = TestVisual('twp', r)
        self.a1.setLayerName('one')
        self.a2.setLayerName('two')
        l1 = TestLayer('one', 0)
        l2 = TestLayer('two', 0)
        r.addLayer(l1)
        r.addLayer(l2)
        self.a2.active = False
        self.w.addZone(self.z1)
        self.w.renderTo(r, 0)
        self.assertEqual([self.a1.visual], l1.renders)
        self.assertEqual([], l2.renders)
       
   
        
class TestZone(serge.zone.Zone):
    def __init__(self):
        """Initialise"""
        super(TestZone, self).__init__()
        self.counter = 0
        
    def updateZone(self, interval, world):
        """Update the zone"""
        self.counter += interval 
        super(TestZone, self).updateZone(interval, world)   


class TestActor(serge.actor.Actor):
    def __init__(self):
        """Initialise"""
        super(TestActor, self).__init__('', '')
        self.counter = 0
        self.layer_name = 'one'
    
    def updateActor(self, interval, world):
        """Update the actor"""
        self.counter += interval    


class TestLayer(serge.render.Layer):
    """A test layer"""
    
    count = 0
    
    def __init__(self, name, order=0):
        """Initialise the TestLayer"""
        super(TestLayer, self).__init__(name, order)
        self.executed = 1e30
        self.renders = []
                
    def render(self, surface):
        """Render to a surface"""
        TestLayer.count += 1
        self.executed = TestLayer.count

class TestVisual(object):
    """A visual item"""
    
    def __init__(self, layer_name, renderer):
        self.layer_name = layer_name
        self.renderer = renderer
        self.width = 0
        self.height = 0
    
    def renderTo(self, interval, surface, coords):
        """Render me"""
        self.renderer.getLayer(self.layer_name).renders.append(self)

if __name__ == '__main__':
    unittest.main()
