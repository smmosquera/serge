"""Tests for Actors"""

import unittest
import os
import pymunk

from helper import *

import serge.actor
import serge.visual
import serge.world
import serge.zone

class TestActor(unittest.TestCase):
    """Tests for the Actor"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        self.w = serge.world.World('test')
        self.z = serge.zone.Zone()
        self.w.addZone(self.z)
        self.z.active = True
        
    def tearDown(self):
        """Tear down the tests"""

    ### Basics ###

    def testCanCreate(self):
        """testCanCreate: should be able to create an actor"""
        a = serge.actor.Actor('thing')
        self.assertEqual('thing', a.tag)
        #
        b = serge.actor.Actor('thing', 'thang')
        self.assertEqual('thing', b.tag)
        self.assertEqual('thang', b.name)
       
    def testCanSetSpatial(self):
        """testCanSetSpatial: should be able to set spatial coords"""
        a = serge.actor.Actor('thing')
        a.setSpatial(50, 50, 5, 5)
        
    def testCanGetSpatial(self):
        """testCanGetSpatial: should be able to get spatial coords"""
        a = serge.actor.Actor('thing')
        a.setSpatial(50, 60, 5, 6)
        x, y, w, h = a.getSpatial()
        self.assertEqual(50, x)
        self.assertEqual(60, y)
        self.assertEqual(5, w)
        self.assertEqual(6, h)

    def testCanMove(self):
        """testCanMove: should be able to move the actor"""
        a = serge.actor.Actor('thing')
        a.setSpatial(50, 60, 5, 6)
        a.move(1, -1)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(51, x)
        self.assertEqual(59, y)
        self.assertEqual(5, w)
        self.assertEqual(6, h)

    def testCanMoveTo(self):
        """testCanMoveTo: should be able to move to a location"""
        a = serge.actor.Actor('thing')
        a.setSpatialCentered(50, 60, 10, 20)
        a.moveTo(55, 66)        
        self.assertEqual(55, a.x)
        self.assertEqual(66, a.y)
        self.assertEqual(10, a.width)
        self.assertEqual(20, a.height)
        
    def testCanMoveToIncrementalNegative(self):
        """testCanMoveToIncrementalNegative: should be able to move incrementally in the negative"""
        # There used to be a bug here
        a = serge.actor.Actor('a')
        a.setSpatial(0., 0., 6., 6.)
        self.assertEqual((3, 3), (a.x, a.y))
        for i in range(200):
            a.x -= .2
            a.y -= .2
        self.assertAlmostEqual(-37, a.x)
        self.assertAlmostEqual(-37, a.y)
        
    def testCanResize(self):
        """testCanResize: should be able to resize"""
        a = serge.actor.Actor('thing')
        a.setSpatial(50, 60, 12, 18)
        a.resizeBy(2, 4)        
        x, y, w, h = a.getSpatial()
        self.assertEqual(49, x)
        self.assertEqual(58, y)
        self.assertEqual(14, w)
        self.assertEqual(22, h)

    def testSettingVisualOnAnActorSetsItsSize(self):
        """testSettingVisualOnAnActorSetsItsSize: setting the visual for an actor should set the size"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('thing')
        a.visual = s
        x, y, w, h = a.getSpatial()
        self.assertEqual((50, 50), (w, h))
                
    def testSettingASpriteNameShouldSetItsSize(self):
        """testSettingASpriteNameShouldSetItsSize: setting the visual via a spire name should set the size"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('thing')
        a.setSpriteName('green')
        x, y, w, h = a.getSpatial()
        self.assertEqual((50, 50), (w, h))
        
    def testZoomShouldResize(self):
        """testZoomShouldResize: zooming an actor should resize it"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('thing')
        a.setSpriteName('green')
        #
        self.assertEqual(50, a.width)
        self.assertEqual(50, a.height)
        #
        a.setZoom(0.5)
        self.assertEqual(25, a.width)
        self.assertEqual(25, a.height)
        #
        a.setZoom(2.0)
        self.assertEqual(100, a.width)
        self.assertEqual(100, a.height)
                    
    ### Updating ###
     
    def testCanUpdateActor(self):
        """testCanUpdateActor: should be able to update an actor"""
        a = serge.actor.Actor('thing')
        a.updateActor(123, None)
                
    ### Serializing ###
       
    def testCanRememberLocation(self):
        """testCanRememberLocation: should be able to remember a location"""
        a = serge.actor.Actor('thing', 'thang')
        a.setSpatial(51, 59, 7, 9)
        a.active = False
        b = serge.serialize.Serializable.fromString(a.asString()) 
        a.move(1, 1)
        a.resizeBy(11,12)       
        a.active = True
        x, y, w, h = b.getSpatial()
        self.assertEqual(51, x)
        self.assertEqual(59, y)
        self.assertEqual(7, w)
        self.assertEqual(9, h)
        self.assertEqual(False, b.active)
        #
        x, y, w, h = a.getSpatial()
        self.assertNotEqual(51, x)
        self.assertNotEqual(59, y)
        self.assertNotEqual(7, w)
        self.assertNotEqual(9, h)
        self.assertNotEqual(False, a.active)

    def testCanRememberSprite(self):
        """testCanRememberSprite: should be able to remember sprite and layer"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('thing', 'thang')
        a.setLayerName('one')
        a.setSpriteName('green')
        b = serge.serialize.Serializable.fromString(a.asString()) 
        self.assertEqual('one', b.getLayerName())                
        self.assertEqual('green', b.getSpriteName())
    
    ### Composite actors ###
    
    def testCompositeActorAddingChildren(self):
        """testCompositeActorAddingChildren: adding a composite actor should add its children"""
        a = serge.actor.CompositeActor('parent')
        a.addChild(serge.actor.Actor('kid1'))
        a.addChild(serge.actor.Actor('kid2'))
        self.w.addActor(a)
        #
        self.assertEqual(set(['parent','kid1','kid2']), set([a.tag for a in self.w.getActors()]))

    def testChildrenAreActorCollections(self):
        """testChildrenAreActorCollections: the children of a composite actor are an actor collection"""
        a = serge.actor.CompositeActor('parent')
        k1 = serge.actor.Actor('kid1', 'k1')
        k2 = serge.actor.Actor('kid2', 'k2')
        a.addChild(k1)
        a.addChild(k2)
        self.assertEqual(k2, a.getChildren().findActorByName('k2'))

    def testCompositesFindChildrenByTag(self):
        """testCompositesFindChildrenByTag: should be able to find children by tag"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.Actor('kid')
        c = serge.actor.Actor('kid')
        d = serge.actor.Actor('not-kid')
        a.addChild(b)
        a.addChild(c)
        a.addChild(d)
        self.w.addActor(a)
        #
        self.assertEqual(set([b, c]), set(a.getChildrenWithTag('kid')))
        #
        a.removeChild(b)
        a.removeChild(c)
        #
        self.assertEqual(set([]), set(a.getChildrenWithTag('kid')))

    def testCompositionAddChildAfterAddingToWorld(self):
        """testCompositionAddChildAfterAddingToWorld: adding child after parent is in world should add to world"""
        a = serge.actor.CompositeActor('parent')
        self.w.addActor(a)
        a.addChild(serge.actor.Actor('kid1'))
        a.addChild(serge.actor.Actor('kid2'))
        #
        self.assertEqual(set(['parent','kid1','kid2']), set([a.tag for a in self.w.getActors()]))
    
    def testCompositeRemovingChildStayingInWorld(self):
        """testCompositeRemovingChildStayingInWorld: should be able to remove actor but keep in world"""
        a = serge.actor.CompositeActor('parent')
        self.w.addActor(a)
        kid = serge.actor.Actor('kid1')
        a.addChild(kid)
        a.addChild(serge.actor.Actor('kid2'))
        a.removeChild(kid, leave_in_world=True)
        #
        self.assertEqual(set(['parent','kid1','kid2']), set([a.tag for a in self.w.getActors()]))
        
    

    def testCompositeAddChildAlreadyInTheWorld(self):
        """testCompositeAddChildAlreadyInTheWorld: adding child that is in the world should be ok"""
        a = serge.actor.CompositeActor('parent')
        self.w.addActor(a)
        dupe = serge.actor.Actor('kid1')
        self.w.addActor(dupe)
        a.addChild(dupe)
        a.addChild(serge.actor.Actor('kid2'))
        #
        self.assertEqual(set(['parent','kid1','kid2']), set([a.tag for a in self.w.getActors()]))
        
    def testCompositeActorRemovingChildren(self):
        """testCompositeActorRemovingChildren: removing a composite actor should remove its children"""
        a = serge.actor.CompositeActor('parent')
        a.addChild(serge.actor.Actor('kid1'))
        a.addChild(serge.actor.Actor('kid2'))
        self.w.addActor(a)
        self.w.removeActor(a)
        #
        self.assertEqual(set([]), set([a.tag for a in self.w.getActors()]))

    def testCompositesCanBeNested(self):
        """testCompositesCanBeNested: should be able to nest composite actors"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.CompositeActor('kid1')
        c = serge.actor.Actor('kid2')
        b.addChild(c)
        a.addChild(b)
        self.w.addActor(a)
        #
        self.assertEqual(set(['parent','kid1','kid2']), set([act.tag for act in self.w.getActors()]))
        #
        self.w.removeActor(a)
        self.assertEqual(set([]), set([a.tag for a in self.w.getActors()]))

    def testNestedCompositesSetActive(self):
        """testNestedCompositesSetActive: setting active property of composites should go to children"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.CompositeActor('kid1')
        c = serge.actor.Actor('kid2')
        b.addChild(c)
        a.addChild(b)
        self.w.addActor(a)
        #
        self.assertEqual(([True, True, True]), ([act.active for act in self.w.getActors()]))
        self.assertEqual(([True, True, True]), ([act.visible for act in self.w.getActors()]))
        #
        a.active = False
        self.assertEqual(([False, False, False]), ([act.active for act in self.w.getActors()]))
        self.assertEqual(([True, True, True]), ([act.visible for act in self.w.getActors()]))
        #
        a.visible = False
        self.assertEqual(([False, False, False]), ([act.active for act in self.w.getActors()]))
        self.assertEqual(([False, False, False]), ([act.visible for act in self.w.getActors()]))

    def testCompositesClearChildren(self):
        """testCompositesClearChildren: should be able to clear  composite actors"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.Actor('kid1')
        c = serge.actor.Actor('kid2')
        a.addChild(b)
        a.addChild(c)
        #
        self.assertTrue(a.hasChild(b))
        self.assertTrue(a.hasChild(c))
        #
        a.removeChildren()
        self.assertFalse(a.hasChild(b))
        self.assertFalse(a.hasChild(c))

    def testNestedCompositesClearChildren(self):
        """testNestedCompositesClearChildren: should be able to clear nested composite actors"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.CompositeActor('kid1')
        c = serge.actor.Actor('kid2')
        a.addChild(b)
        b.addChild(c)
        self.w.addActor(a)
        #
        self.assertEqual(set(['parent','kid1','kid2']), set([act.tag for act in self.w.getActors()]))
        self.assertTrue(a.hasChild(b))
        self.assertTrue(b.hasChild(c))
        #
        a.removeChildren()
        # c should be gone from the world
        self.assertEqual(set(['parent']), set([act.tag for act in self.w.getActors()]))
        self.assertFalse(a.hasChild(b))
        self.assertFalse(b.hasChild(c))
        
    def testRemovingChildFromCompositeRemovesActor(self):
        """testRemovingChildFromCompositeRemovesActor: removing a child from a parent removes that child from the world"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.Actor('kid1')
        c = serge.actor.Actor('kid2')
        a.addChild(b)
        a.addChild(c)
        self.w.addActor(a)
        a.removeChild(b)
        #
        self.assertEqual([c], a.getChildren())
        self.assertEqual(set(['parent', 'kid2']), set([a.tag for a in self.w.getActors()]))
        
    def testRemovingChildFromWorldRemovesFromActor(self):
        """testRemovingChildFromWorldRemovesFromActor: remove a child from the world removes it from the children of the parent"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.Actor('kid1')
        c = serge.actor.Actor('kid2')
        a.addChild(b)
        a.addChild(c)
        self.w.addActor(a)
        self.w.removeActor(b)
        #
        self.assertEqual([c], a.getChildren())
        self.assertEqual(set(['parent', 'kid2']), set([a.tag for a in self.w.getActors()]))
        
    def testNestedCompositesRemoval(self):
        """testNestedCompositesRemoval: removing composite which is a child should remove all children"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.CompositeActor('kid1')
        c = serge.actor.Actor('kid2')
        a.addChild(b)
        b.addChild(c)
        self.w.addActor(a)
        #
        a.removeChild(b)
        self.assertEqual(set(['parent']), set([a.tag for a in self.w.getActors()]))

    def testCompositesClearActors(self):
        """testCompositesClearActors: should be able to use the world's clear actors method"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.Actor('kid1')
        c = serge.actor.Actor('kid2')
        a.addChild(b)
        a.addChild(c)
        self.w.addActor(a)
        #
        self.w.clearActors()
        self.assertEqual(set([]), set([a.tag for a in self.w.getActors()]))

    def testFailRemovingMissingActor(self):
        """testFailRemovingMissingActor: should fail when trying to remove a missing child actor"""
        a = serge.actor.CompositeActor('parent')
        b = serge.actor.CompositeActor('kid1')
        self.assertRaises(serge.actor.InvalidActor, a.removeChild, b)        
            
    def testSerializeAndDeserializeAComposite(self):
        """testSerializeAndDeserializeAComposite: should be able to serialize and deserialize a composite"""
        a = serge.actor.CompositeActor('parent', 'parent')
        b = serge.actor.CompositeActor('kid1')
        b.addChild(serge.actor.Actor('kid2'))
        a.addChild(b)
        self.w.addActor(a)
        #
        # World should come back with all actors 
        nw = serge.serialize.Serializable.fromString(self.w.asString())   
        self.assertEqual(set(['parent','kid1','kid2']), set([a.tag for a in nw.getActors()]))
        nw.removeActor(nw.findActorByName('parent'))
        # ... and acting like composites
        self.assertEqual(set([]), set([a.tag for a in nw.getActors()]))

    ### Events ###
    
    def testCanHookAddedToWorld(self):
        """testCanHookAddedToWorld: should be able to hook when added to the world"""
        def doit(obj, arg):
            self.assertEqual(a, obj)
            self.assertEqual(1, arg)
            doit.seen = True
        #
        doit.seen = False
        a = serge.actor.Actor('a')
        a.linkEvent(serge.events.E_ADDED_TO_WORLD, doit, 1)
        self.w.addActor(a)
        self.assertEqual(True, doit.seen)
        
    def testCanHookWhenRemoved(self):
        """testCanHookWhenRemoved: should be able to hook when removed from the world"""
        def doit(obj, arg):
            self.assertEqual(a, obj)
            self.assertEqual(1, arg)
            doit.seen = True
        #
        doit.seen = False
        a = serge.actor.Actor('a')
        a.linkEvent(serge.events.E_REMOVED_FROM_WORLD, doit, 1)
        self.w.addActor(a)
        self.w.removeActor(a)
        self.assertEqual(True, doit.seen)
        
    ### Mounting actors to other actors - non-physical ###
    
    def testCanMountActor(self):
        """testCanMountActor: should be able to mount an actor"""
        a = serge.actor.MountableActor('main')
        a.moveTo(20, 20)
        b = serge.actor.Actor('b')
        b.moveTo(50,60)
        a.mountActor(b, (10, 20))
        #
        # Should move on mounting
        self.assertEqual((30, 40), (b.x, b.y))
        a.moveTo(123, 456)
        #
        # Should move on moving also
        self.assertEqual((133, 476), (b.x, b.y))
        
    def testCanUnmountActor(self):
        """testCanUnmountActor: should be able to unmount actor"""
        a = serge.actor.MountableActor('main')
        a.moveTo(50, 60)
        b = serge.actor.Actor('b')
        a.mountActor(b, (10, 20))
        self.assertEqual((60, 80), (b.x, b.y))
        a.unmountActor(b)
        a.moveTo(123, 456)
        self.assertEqual((60, 80), (b.x, b.y))
        #
        # Should be able to move b again
        b.moveTo(1,1)
         
    def testFailMountingAlreadyMounted(self):
        """testFailMountingAlreadyMounted: should fail if mounting an already mounted actor"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        a.mountActor(b, (10, 20))
        self.assertRaises(serge.actor.AlreadyMounted, a.mountActor, b, (1,2))
         
    def testFailUnmountingActorNotMounted(self):
        """testFailUnmountingActorNotMounted: should fail if unmounting an actor that is not mounted"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        self.assertRaises(serge.actor.NotMounted, a.unmountActor, b)
        
    def testCanMountMulitpleActors(self):
        """testCanMountMulitpleActors: should be able to mount multiple actors"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        b.moveTo(50,60)
        c = serge.actor.Actor('c')
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        a.mountActor(c, (-10, -20))
        a.moveTo(123, 456)
        self.assertEqual((133, 476), (b.x, b.y))
        self.assertEqual((113, 436), (c.x, c.y))
        
    def testCanRotateMountedActor(self):
        """testCanRotateMountedActor: should be able to rotate a mounted actor"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        b.moveTo(50,60)
        a.mountActor(b, (10, 0))
        a.moveTo(100, 100)
        self.assertEqual((110, 100), (b.x, b.y))
        a.setAngle(90)
        self.assertEqual(90, b.getAngle())
        self.assertEqual((100, 90), (b.x, b.y))        

    def testCanRotateMountedActorManytimes(self):
        """testCanRotateMountedActorManytimes: should be able to rotate mounted actor a few times"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        b.moveTo(50,60)
        a.mountActor(b, (10, 0))
        a.moveTo(100, 100)
        self.assertEqual((110, 100), (b.x, b.y))
        a.setAngle(90)
        a.setAngle(90)
        self.assertEqual(90, b.getAngle())
        self.assertEqual((100, 90), (b.x, b.y))        

    def testCanPreRotateMountedActor(self):
        """testCanPreRotateMountedActor: if actor is pre-rotated then mounting is against initial location"""
        a = serge.actor.MountableActor('main')
        a.setAngle(90)
        b = serge.actor.Actor('b')
        b.moveTo(50,60)
        a.mountActor(b, (10, 0), original_rotation=True)
        a.moveTo(100, 100)
        self.assertEqual(90, b.getAngle())
        self.assertEqual((100, 90), (b.x, b.y))        
            
    def testFailMovingMountedActor(self):
        """testFailMovingMountedActor: should fail when trying to move a mounted actor"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        a.mountActor(b, (10, 0))
        self.assertRaises(serge.actor.PositionLocked, b.moveTo, 100, 100)
        
    def testFailRotatingMountedActor(self):
        """testFailRotatingMountedActor: should fail when rotating a mounted actor"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.Actor('b')
        a.mountActor(b, (10, 0))
        self.assertRaises(serge.actor.PositionLocked, b.setAngle, 90)
        
    def testCanNestMountedActors(self):
        """testCanNestMountedActors: should be able to nest a mounted actor"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.MountableActor('b')
        c = serge.actor.Actor('c')
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        a.moveTo(100, 100)
        self.assertEqual((110, 120), (b.x, b.y))
        self.assertEqual((140, 160), (c.x, c.y))
        
    def testMountedActorsAreInWorld(self):
        """testMountedActorsAreInWorld: when mounting actors they should be in the world"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.MountableActor('b')
        c = serge.actor.Actor('c')
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        #
        w = serge.world.World('main')
        w.addActor(a)
        #
        self.assertEqual(True, w.hasActor(a))
        self.assertEqual(True, w.hasActor(b))
        self.assertEqual(True, w.hasActor(c))
        
    def testMountedActorsGetRemoved(self):
        """testMountedActorsGetRemoved: when removing the mount from the world the mounted actors are removed"""
        a = serge.actor.MountableActor('main')
        b = serge.actor.MountableActor('b')
        c = serge.actor.Actor('c')
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        #
        w = serge.world.World('main')
        w.addActor(a)
        w.removeActor(a)
        #
        self.assertEqual(False, w.hasActor(a))
        self.assertEqual(False, w.hasActor(b))
        self.assertEqual(False, w.hasActor(c))
        
    def testCanSerializeMountable(self):
        """testCanSerializeMountable: should be able to serailize a mountable actor"""
        a = serge.actor.MountableActor('main', 'a')
        b = serge.actor.MountableActor('b', 'b')
        c = serge.actor.Actor('c', 'c')
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        #
        w = serge.world.World('main')
        z = serge.zone.Zone()
        w.addZone(z)
        w.addActor(a)
        w2 = serge.serialize.Serializable.fromString(w.asString())
        #
        aa = w2.findActorByName('a')
        bb = w2.findActorByName('b')
        cc = w2.findActorByName('c')
        #
        aa.moveTo(100, 100)
        self.assertEqual((110, 120), (bb.x, bb.y))
        self.assertEqual((140, 160), (cc.x, cc.y))
        #
        self.assertRaises(serge.actor.PositionLocked, bb.moveTo, 100, 100)
        self.assertRaises(serge.actor.PositionLocked, cc.moveTo, 100, 100)
        self.assertRaises(serge.actor.PositionLocked, bb.setAngle, 10)
        self.assertRaises(serge.actor.PositionLocked, cc.setAngle, 10)
        
    ### Mounting actors to other actors - physical version using pymunk ###
    
    def testCanMountActorPhysical(self):
        """testCanMountActorPhysical: should be able to mount an actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(123, 456)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        b.moveTo(50,60)
        a.mountActor(b, (10, 20))
        self.w.addActor(a)
        #
        # Should move on moving also
        self.assertEqual((133, 476), (b.x, b.y))
    
    def testCanMoveMountedActorPhysical(self):
        """testCanMoveMountedActorPhysical: should be able to move the mounted actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(123, 456)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        b.moveTo(50,60)
        a.mountActor(b, (10, 20))
        self.w.addActor(a)
        self.assertEqual((133, 476), (b.x, b.y))
        #
        a.moveTo(223, 556) 
        self.w.updateWorld(5000)       
        self.assertAlmostEqual(pymunk.Vec2d((10,20)).length, (b.getPhysical().body.position - a.getPhysical().body.position).length, 0)
        
    def testCanMoveMountedPhysicalAfterMotion(self):
        """testCanMoveMountedPhysicalAfterMotion: should be able to move mounted after motion has changed offsets"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(100, 100)
        b = serge.actor.PhysicallyMountableActor('b', mass=10)
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c = serge.actor.Actor('c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        a.getPhysical().body.apply_force((100,0))
        #
        self.w.addActor(a)
        self.z.setPhysicsStepsize(1)
        for i in range(100):
            #print a.x, a.y, b.x, b.y, c.x, c.y
            self.w.updateWorld(100)
            a.getPhysical().body.reset_forces()
        #
        self.assertNotEqual((100, 100), (a.x, a.y))
        self.assertAlmostEqual(pymunk.Vec2d((10,20)).length, pymunk.Vec2d(b.getPhysical().body.position-a.getPhysical().body.position).length, 1)
        self.assertAlmostEqual(pymunk.Vec2d((30,40)).length, pymunk.Vec2d(c.getPhysical().body.position-b.getPhysical().body.position).length, 1)         
        #
        a.moveTo(200,200)
        self.w.updateWorld(1000)
        self.assertNotEqual((200, 200), (a.x, a.y))
        d1 = abs(pymunk.Vec2d((10,20)).length - pymunk.Vec2d(b.getPhysical().body.position-a.getPhysical().body.position).length)
        self.assert_(d1 < 2.0, d1)
        d2 = abs(pymunk.Vec2d((30,40)).length - pymunk.Vec2d(c.getPhysical().body.position-b.getPhysical().body.position).length)
        self.assert_(d2 < 2.0, d2)         
        
        
    def testFailMountActorPhysicallyNoPhysical(self):
        """testFailMountActorPhysicallyNoPhysical: should fail if physically mounting when either is not physical"""
        self.assertRaises(serge.actor.NoPhysicalConditions, serge.actor.PhysicallyMountableActor, 'main')
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.Actor('b')
        self.assertRaises(serge.actor.NoPhysicalConditions, a.mountActor, b, (10,20))
        
    def testCanUnmountActorPhysical(self):
        """testCanUnmountActorPhysical: should be able to unmount actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(50, 60)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 20))
        self.assertEqual((60, 80), (b.x, b.y))
        a.unmountActor(b)
        a.moveTo(123, 456)
        self.w.updateWorld(1000)
        self.assertEqual((60, 80), (b.x, b.y))
        #
        # Should be able to move b again
        b.moveTo(1,1)
         
    def testFailMountingAlreadyMountedPhysical(self):
        """testFailMountingAlreadyMountedPhysical: should fail if mounting an already mounted actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 20))
        self.assertRaises(serge.actor.AlreadyMounted, a.mountActor, b, (1,2))
         
    def testFailUnmountingActorNotMountedPhysical(self):
        """testFailUnmountingActorNotMountedPhysical: should fail if unmounting an actor that is not mounted"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        self.assertRaises(serge.actor.NotMounted, a.unmountActor, b)
        
    def testCanMountMulitpleActorsPhysical(self):
        """testCanMountMulitpleActorsPhysical: should be able to mount multiple actors"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(123, 456)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        b.moveTo(50,60)
        c = serge.actor.Actor('c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        a.mountActor(c, (-10, -20))
        self.w.updateWorld(1000)
        self.assertEqual((133, 476), (b.x, b.y))
        self.assertEqual((113, 436), (c.x, c.y))
        
    def testCanRotateMountedActorPhysical(self):
        """testCanRotateMountedActorPhysical: should be able to rotate a mounted actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(100, 100)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1, update_angle=True))
        b.moveTo(50,60)
        a.mountActor(b, (10, 0))
        self.w.updateWorld(1000)
        self.assertEqual((110, 100), (b.x, b.y))
        a.setAngle(90, sync_physical=True)
        self.w.updateWorld(1000)
        self.assertEqual(90, b.getAngle())
        self.assertEqual((100, 90), (b.x, b.y))        
        
    def testFailMovingMountedActorPhysical(self):
        """testFailMovingMountedActorPhysical: should fail when trying to move a mounted actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 0))
        self.assertRaises(serge.actor.PositionLocked, b.moveTo, 100, 100)
        
    def testFailRotatingMountedActorPhysical(self):
        """testFailRotatingMountedActorPhysical: should fail when rotating a mounted actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 0))
        self.assertRaises(serge.actor.PositionLocked, b.setAngle, 90)
        
    def testCanNestMountedActorsPhysical(self):
        """testCanNestMountedActorsPhysical: should be able to nest a mounted actor"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(100, 100)
        b = serge.actor.PhysicallyMountableActor('b', mass=10)
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c = serge.actor.Actor('c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        #
        self.assertEqual((110, 120), (b.x, b.y))
        self.assertEqual((140, 160), (c.x, c.y))

    def testMovingByForceMovesMounts(self):
        """testMovingByForceMovesMounts: a force should move all actors"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        a.moveTo(100, 100)
        b = serge.actor.PhysicallyMountableActor('b', mass=10)
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c = serge.actor.Actor('c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c.moveTo(40,50)
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        a.getPhysical().body.apply_force((100,0))
        #
        self.w.addActor(a)
        self.z.setPhysicsStepsize(1)
        for i in range(100):
            #print a.x, a.y, b.x, b.y, c.x, c.y
            self.w.updateWorld(100)
            a.getPhysical().body.reset_forces()
        self.assertNotEqual((100, 100), (a.x, a.y))
        self.assertAlmostEqual(pymunk.Vec2d((10,20)).length, pymunk.Vec2d(b.getPhysical().body.position-a.getPhysical().body.position).length, 1)
        self.assertAlmostEqual(pymunk.Vec2d((30,40)).length, pymunk.Vec2d(c.getPhysical().body.position-b.getPhysical().body.position).length, 1)        
    
        
    def testMountedActorsAreInWorldPhysical(self):
        """testMountedActorsAreInWorldPhysical: when mounting actors they should be in the world"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.PhysicallyMountableActor('b', mass=10)
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c = serge.actor.Actor('c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        #
        self.w.addActor(a)
        #
        self.assertEqual(True, self.w.hasActor(a))
        self.assertEqual(True, self.w.hasActor(b))
        self.assertEqual(True, self.w.hasActor(c))
        
    def testMountedActorsGetRemovedPhysical(self):
        """testMountedActorsGetRemovedPhysical: when removing the mount from the world the mounted actors are removed"""
        a = serge.actor.PhysicallyMountableActor('main', mass=10)
        b = serge.actor.PhysicallyMountableActor('b', mass=10)
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c = serge.actor.Actor('c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        #
        self.w.addActor(a)
        self.w.removeActor(a)
        #
        self.assertEqual(False, self.w.hasActor(a))
        self.assertEqual(False, self.w.hasActor(b))
        self.assertEqual(False, self.w.hasActor(c))
        
    def testCanSerializeMountablePhysical(self):
        """testCanSerializeMountablePhysical: should be able to serailize a mountable actor"""
        a = serge.actor.PhysicallyMountableActor('main', 'a', mass=10)
        a.moveTo(100, 100)
        b = serge.actor.PhysicallyMountableActor('b', 'b', mass=10)
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        c = serge.actor.Actor('c', 'c')
        c.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=1))
        a.mountActor(b, (10, 20))
        b.mountActor(c, (30, 40))
        self.w.addActor(a)
        #
        w2 = serge.serialize.Serializable.fromString(self.w.asString())
        #
        aa = w2.findActorByName('a')
        bb = w2.findActorByName('b')
        cc = w2.findActorByName('c')
        #
        w2.updateWorld(1000)
        self.assertEqual((110, 120), (bb.x, bb.y))
        self.assertEqual((140, 160), (cc.x, cc.y))
        #
        self.assertRaises(serge.actor.PositionLocked, bb.moveTo, 100, 100)
        self.assertRaises(serge.actor.PositionLocked, cc.moveTo, 100, 100)
        self.assertRaises(serge.actor.PositionLocked, bb.setAngle, 10)
        self.assertRaises(serge.actor.PositionLocked, cc.setAngle, 10)


class TestActorCollections(unittest.TestCase):
    """Tests for the ActorCollections"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        self.w = serge.world.World('test')
        self.z = serge.zone.Zone()
        self.w.addZone(self.z)
        self.z.active = True
        #
        self.a1 = MyActor('a', 'a1')
        self.a2 = MyActor('a', 'a2')
        self.a3 = MyActor('a', 'a3')
        self.b1 = MyActor('b', 'b1')
        self.b2 = MyActor('b', 'b2')
        #
        self.c = serge.actor.ActorCollection([self.a1, self.a2, self.a3, self.b1, self.b2])
        
    def tearDown(self):
        """Tear down the tests"""
                          
    def testCollectionIsLikeList(self):
        """testCollectionIsLikeList: a collection should be usable as a list"""
        self.assertEqual([self.a1, self.a2, self.a3, self.b1, self.b2], list(self.c))
        self.assertEqual(self.a1, self.c[0])
        self.c.remove(self.a1)
        self.assertEqual(self.a2, self.c[0])
        
    def testCanFindActorsWithTag(self):
        """testCanFindActorsWithTag: should be able to find actors with a tag"""
        self.assertEqual(set([self.a1, self.a2, self.a3]), set(self.c.findActorsByTag('a')))
        self.assertEqual(set([self.b1, self.b2]), set(self.c.findActorsByTag('b')))
        
    def testCanFindActorWithName(self):
        """testCanFindActorWithName: should be able to find actor with a name"""
        self.assertEqual(self.a1, self.c.findActorByName('a1'))
        self.assertEqual(self.b2, self.c.findActorByName('b2'))
        
    def testFailFindActorWithName(self):
        """testFailFindActorWithName: should fail when finding an actor not present"""
        self.assertRaises(serge.actor.InvalidActor, self.c.findActorByName, 'c1')
        
    def testTestContainment(self):
        """testTestContainment: should be able to check containment"""
        #
        # Booleans
        self.assertTrue(self.c.hasActorWithTag('a'))
        self.assertTrue(self.c.hasActorWithTag('b'))
        self.assertFalse(self.c.hasActorWithTag('c'))
        self.assertTrue(self.c.hasActorWithName('a1'))
        self.assertFalse(self.c.hasActorWithName('c1'))       
        #
        # Numeric
        self.assertEqual(3, self.c.numberOfActorsWithTag('a'))
        self.assertEqual(2, self.c.numberOfActorsWithTag('b'))
        self.assertEqual(0, self.c.numberOfActorsWithTag('c'))

    def testCanDoForEach(self):
        """testCanDoForEach: should be able to do a for each on the members of collective"""
        self.c.forEach().doit(123)
        self.assertEqual(123, self.a1.value)
        
    def testCanReturnFromForEach(self):
        """testCanReturnFromForEach: should be able to return from a foreach"""
        result = self.c.forEach().returnit(123)
        self.assertEqual([123]*5, result)
        
    def testCanBreakFromForEach(self):
        """testCanBreakFromForEach: should be able to break from a foreach"""
        result = self.c.forEach().raisename('b1')
        self.assertEqual(['b1']*3, result)
        
    def testCanSetAttributesInForEach(self):
        """testCanSetAttributesInForEach: should be able to set attributes in a for each"""
        self.c.forEach().visible = True
        self.assertTrue(self.a1.visible)
        self.assertTrue(self.b2.visible)
        self.c.forEach().visible = False
        self.assertFalse(self.a1.visible)
        self.assertFalse(self.b2.visible)
        
        
    

class MyActor(serge.actor.Actor):
    """Simple actor with some testing"""
    
    def __init__(self, *args, **kw):
        super(MyActor, self).__init__(*args, **kw)
        self.value = None
        
    def doit(self, value):
        """Set a value"""
        self.value = value
                    
    def returnit(self, value):
        """Return something"""
        return value

    def raisename(self, value):
        """Raise if there is a name"""
        if self.name == value:
            raise StopIteration
        return value
                    
if __name__ == '__main__':
    unittest.main()
