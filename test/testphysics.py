"""Tests for the Physics engine"""

import unittest

import serge.world
import serge.zone
import serge.actor
import serge.geometry
import serge.input
import serge.engine
import serge.physical
import serge.blocks.utils
import serge.blocks.visualblocks

from helper import *

class TestPhysics(unittest.TestCase, VisualTester):
    """Tests for the Physics"""

    def setUp(self):
        """Set up the tests"""
        self.w = serge.world.World('test')
        self.z1 = serge.zone.Zone()
        self.z1.active = True
        self.w.addZone(self.z1)
        serge.visual.Register.clearItems()
        
    def tearDown(self):
        """Tear down the tests"""

    def testAddActorVelocity(self):
        """testAddActorVelocity: should be able to add an object with velocity"""
        a = serge.actor.Actor('test')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(1.0, 0.0)))
        a.moveTo(2,0)
        self.w.addActor(a)
        self.w.updateWorld(1000.0)
        #
        # Should move 1 meter per second
        self.assertAlmostEqual(3.0, a.x)
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(4.0, a.x)
      
    def testRemoveObjectNoChange(self):
        """testRemoveObjectNoChange: should be able to remove an object and it should not change"""
        a = serge.actor.Actor('test')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(1.0, 0.0)))
        a.moveTo(0,0)
        self.w.addActor(a)
        self.w.updateWorld(1000.0)
        #
        # Should move 1 meter per second
        self.assertAlmostEqual(1.0, a.x)
        self.w.removeActor(a)
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1.0, a.x)
        
    def testChangeObjectVelocity(self):
        """testChangeObjectVelocity: should be able to change an objects velocity after it has been added"""
        a = serge.actor.Actor('test')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(1.0, 0.0)))
        a.moveTo(0,0)
        self.w.addActor(a)
        self.w.updateWorld(1000.0)
        #
        # Should move 1 meter per second and then 2
        self.assertAlmostEqual(1.0, a.x)
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(2.0, 0.0)))
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(3.0, a.x)
        
    def testAddActorForce(self):
        """testAddActorForce: forces should apply to an object"""
        a = serge.actor.Actor('test')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(0.0, 0.0), force=(1.0, 0.0)))
        a.moveTo(0,0)
        self.w.addActor(a)
        self.w.updateWorld(1000.0)
        #
        # Should accelerate at 1 meter per second per second
        self.assertAlmostEqual(1.0, a.getPhysical().velocity[0])
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(2.0, a.getPhysical().velocity[0])
        
    def testGlobalForce(self):
        """testGlobalForce: should be able to exert a global force"""
        a = serge.actor.Actor('test')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(0.0, 0.0)))
        a.moveTo(0,0)
        self.w.addActor(a)
        self.w.setGlobalForce((1.0, 0.0))
        self.w.updateWorld(1000.0)
        #
        # Should accelerate at 1 meter per second per second
        self.assertAlmostEqual(1.0, a.getPhysical().velocity[0])
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(2.0, a.getPhysical().velocity[0])
        
    def testAddMultipleObjects(self):
        """testAddMultipleObjects: should be able to add multiple objects"""
        for i in range(1, 1000):
            a = serge.actor.Actor('test', str(i))
            a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=0.05, velocity=(i, 0.0)))
            a.moveTo(i,0)
            self.w.addActor(a)
        #
        self.w.updateWorld(1000.0)
        for i in range(1, 1000):
            a = self.w.findActorByName(str(i))
            self.assertAlmostEqual(i*2, a.x)
    
    ### Setting the size ###
    
    def testCanSetSizeFromCircle(self):
        """testCanSetSizeFromCircle: should be able to set the size from a circle"""
        a = serge.actor.Actor('test', 'a')
        a.visual = serge.blocks.visualblocks.Circle(40, (0,0,0,0))
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, velocity=(1, 0.0),
             visual_size=serge.geometry.CIRCLE))
        self.assertEqual(40, a.getPhysical().radius)
        
    def testCanSetSizeFromRectangle(self):
        """testCanSetSizeFromRectangle: should be able to set the size from a rectangle"""
        a = serge.actor.Actor('test', 'a')
        a.visual = serge.blocks.visualblocks.Rectangle((40, 50), (0,0,0,0))
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, velocity=(1, 0.0),
         visual_size=serge.geometry.RECTANGLE))
        self.assertEqual(40, a.getPhysical().width)
        self.assertEqual(50, a.getPhysical().height)
        
    def testCanSetSizeFromSprite(self):
        """testCanSetSizeFromSprite: should be able to set the size from a sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        a = serge.actor.Actor('test', 'a')
        a.setSpriteName('green')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, velocity=(1, 0.0), 
            visual_size=serge.geometry.RECTANGLE))
        self.assertEqual(40, a.getPhysical().width)
        self.assertEqual(31, a.getPhysical().height)

    def testCanSetSizeFromCircularSprite(self):
        """testCanSetSizeFromCircularSprite: should be able to set the size from a circular sprite"""
        serge.visual.Register.registerItem('green', p('greenship.png'))
        a = serge.actor.Actor('test', 'a')
        a.setSpriteName('green')
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, velocity=(1, 0.0), 
            visual_size=serge.geometry.CIRCLE))
        self.assertEqual(20, a.getPhysical().radius)
        
    def testFailVisualSizeWithNoVisual(self):
        """testFailVisualSizeWithNoVisual: should fail if setting visual size and no visual set"""
        a = serge.actor.Actor('test', 'a')
        self.assertRaises(serge.physical.InvalidDimensions, a.setPhysical, serge.physical.PhysicalConditions(mass=1.0, velocity=(1, 0.0), visual_size=True))
        
    def testFailWithInvalidVisualSize(self):
        """testFailWithInvalidVisualSize: should fail with an invalid visual size"""
        a = serge.actor.Actor('test', 'a')
        a.visual = serge.blocks.visualblocks.Rectangle((40, 50), (0,0,0,0))
        self.assertRaises(serge.physical.InvalidDimensions, a.setPhysical, serge.physical.PhysicalConditions(mass=1.0, velocity=(1, 0.0), visual_size=1234))
    
    def testPhysicalBodyWithoutDimensions(self):
        """testPhysicalBodyWithoutDimensions: can create a body without dimensions"""
        a = serge.actor.Actor('a')
        a.setPhysical(serge.physical.PhysicalBody(mass=1, velocity=(1,0)))
        a.moveTo(100,100)
        self.w.addActor(a)
        #
        # Put another object in there which would collide with a if it
        # really had a physical extent
        b = serge.actor.Actor('b')
        b.setPhysical(serge.physical.PhysicalConditions(mass=1, radius=0.1))
        b.moveTo(100.5, 100)
        self.w.addActor(b)
        #
        self.assertEqual((100,100), (a.x, a.y))        
        self.w.updateWorld(1000)
        self.assertAlmostEqual(101, a.x)        
        
    ### Collisions ###
        
    def testTwoBodyCollision(self):
        """testTwoBodyCollision: should be able to have a two body collision"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0.,0.)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(-1.0, 0.0)))
        a2.moveTo(4.,0.)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Should bounce at 1 second
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        #
        #
        for i in range(100):
            self.w.updateWorld(10.0)
        self.assert_(a1.x < 0.1, 'Not less than 0.1 (%d)' % a1.x)
        self.assert_(a2.x > 3.9, 'Not greated than 3.9 (%d)' % a2.x)

    def testCanCopyPhysics(self):
        """testCanCopyPhysics: should be able to copy the physics parameters"""
        a1 = serge.actor.Actor('a1')
        physics = serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0))
        a1.setPhysical(physics.copy())
        a1.moveTo(0.,0.)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(physics.copy())
        a2.getPhysical().velocity = (-1, 0)
        a2.moveTo(4.,0.)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Should bounce at 1 second
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        #
        #
        for i in range(100):
            self.w.updateWorld(10.0)
        self.assert_(a1.x < 0.1, 'Not less than 0.1 (%d)' % a1.x)
        self.assert_(a2.x > 3.9, 'Not greated than 3.9 (%d)' % a2.x)
        
    

    def testCanSetPhysicsStepSizeBig(self):
        """testCanSetPhysicsStepSizeBig: should be able to set the physics stepsize large"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0.,0.)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(-1.0, 0.0)))
        a2.moveTo(4.,0.)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Big step size should miss the collision
        self.w.setPhysicsStepsize(1000.0)
        self.w.updateWorld(2000.0)
        self.assertAlmostEqual(2, a1.x)
        self.assertAlmostEqual(2, a2.x)
        
    def testCanSetPhysicsStepSizeSmall(self):
        """testCanSetPhysicsStepSizeSmall: should be able to set the physics stepsize small"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0.,0.)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(-1.0, 0.0)))
        a2.moveTo(4.,0.)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Should be able to do this in one go with small step size
        self.w.setPhysicsStepsize(10.0)
        self.w.updateWorld(2000.0)
        self.assert_(a1.x < 0.1, 'Not less than 0.1 (%d)' % a1.x)
        self.assert_(a2.x > 3.9, 'Not greated than 3.9 (%d)' % a2.x)
    
        
    def testCollidingWithStationaryObject(self):
        """testCollidingWithStationaryObject: should be able to collide with a stationary object"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(radius=1.0, fixed=True))
        a2.moveTo(3,0)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Should bounce at 1 second
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        #
        for i in range(100):
            self.w.updateWorld(10.0)
        self.assert_(a1.x < 0.1)
        self.assertAlmostEqual(3, a2.x)

    def testCollidingWithNonCircular(self):
        """testCollidingWithNonCircular: should be able to collide with a non-circular object"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(width=2.0, height=20.0, fixed=True))
        a2.moveTo(3,10)
        a3 = serge.actor.Actor('a3')
        a3.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a3.moveTo(0,-6)
        self.w.addActor(a1)
        self.w.addActor(a2)
        self.w.addActor(a3)
        #
        # Should bounce at 1 second
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        self.assertAlmostEqual(1, a3.x)
        #
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(0, a1.x)
        self.assertAlmostEqual(3, a2.x)
        self.assertAlmostEqual(2, a3.x)

    
        
    def testCanSerializeAndDeserialize(self):
        """testCanSerializeAndDeserialize: should be able to store and restore a physics based object"""
        a = serge.actor.Actor('test', 'test')
        a.visual = serge.blocks.visualblocks.Circle(40, (0,0,0,0))
        a.setPhysical(serge.physical.PhysicalConditions(mass=1.0, radius=1.0, velocity=(1.0, 0.0), update_angle=True, visual_size=serge.geometry.CIRCLE))
        a.moveTo(0,0)
        self.w.addActor(a)
        self.w.updateWorld(1000.0)
        #
        # Serialize and deserialize
        world = serge.serialize.Serializable.fromString(self.w.asString())
        world.updateWorld(1000.0)
        actor = world.findActorByName('test')
        self.assertAlmostEqual(2.0, actor.x)        
        self.assertEqual(True, actor.getPhysical().update_angle)
        self.assertEqual(serge.geometry.CIRCLE, actor.getPhysical().visual_size)
        self.assertEqual(40, actor.getPhysical().radius)
        
    def testFailIfIncorrectDimension(self):
        """testFailIfIncorrectDimension: should fail if dimensions dont make sense"""
        self.assertRaises(serge.physical.InvalidDimensions, serge.physical.PhysicalConditions, fixed=True, radius=1.0, width=1.0)
        self.assertRaises(serge.physical.InvalidDimensions, serge.physical.PhysicalConditions, fixed=True, radius=1.0, height=1.0)
        self.assertRaises(serge.physical.InvalidDimensions, serge.physical.PhysicalConditions, fixed=True, radius=1.0, height=1.0, width=1.0)
        self.assertRaises(serge.physical.InvalidDimensions, serge.physical.PhysicalConditions, fixed=True, width=1.0)
        self.assertRaises(serge.physical.InvalidDimensions, serge.physical.PhysicalConditions, fixed=True, height=1.0)

    def testFailIfNeitherFixedNorMass(self):
        """testFailIfNeitherFixedNorMass: need to have either mass or fixed"""
        self.assertRaises(serge.physical.InvalidMass, serge.physical.PhysicalConditions, radius=1.0)
    

    ### Collision stuff ###
    
    def testCanGetCallbackForCollision(self):
        """testCanGetCallbackForCollision: should be able to get a callback on collisions"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(radius=1.0, fixed=True))
        a2.moveTo(3,0)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        collision = set()
        def doCollision(first, second):
            collision.add((first.tag, second.tag))
        #
        a1.linkEvent('collision', doCollision, a1)
        a2.linkEvent('collision', doCollision, a2)
        #
        # Should bounce at 1 second
        self.w.updateWorld(2000.0)
        #
        self.assertEqual(set(((a1.tag,a2.tag), (a2.tag,a1.tag))), collision)
        
    def testShouldBeAbleToLayerCollisions(self):
        """testShouldBeAbleToLayerCollisions: should be able to use collision layers to match collisions"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(layers=2, radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(layers=2, radius=1.0, fixed=True))
        a2.moveTo(3,0)
        a3 = serge.actor.Actor('a3')
        a3.setPhysical(serge.physical.PhysicalConditions(layers=4, radius=1.0, fixed=True))
        a3.moveTo(1.5,0.5)
        self.w.addActor(a1)
        self.w.addActor(a2)
        self.w.addActor(a3)
        #
        collision = set()
        def doCollision(first, second):
            collision.add((first.tag, second.tag))
        #
        a1.linkEvent('collision', doCollision, a1)
        a2.linkEvent('collision', doCollision, a2)
        a3.linkEvent('collision', doCollision, a3)
        #
        # Should bounce at 1 second
        self.w.updateWorld(2000.0)
        #
        self.assertEqual(set(((a1.tag,a2.tag), (a2.tag,a1.tag))), collision)
        
    def testShouldBeAbleToGroupCollisions(self):
        """testShouldBeAbleToGroupCollisions: should be able to use collision groups to match collisions"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(group=2, radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(group=2, radius=1.0, fixed=True))
        a2.moveTo(3,0)
        a3 = serge.actor.Actor('a3')
        a3.setPhysical(serge.physical.PhysicalConditions(group=3, radius=1.0, fixed=True))
        a3.moveTo(1.5,0.5)
        self.w.addActor(a1)
        self.w.addActor(a2)
        self.w.addActor(a3)
        #
        collision = set()
        def doCollision(first, second):
            collision.add((first.tag, second.tag))
        #
        a1.linkEvent('collision', doCollision, a1)
        a2.linkEvent('collision', doCollision, a2)
        a3.linkEvent('collision', doCollision, a3)
        #
        # Should bounce at 1 second
        self.w.updateWorld(2000.0)
        #
        self.assertEqual(set((('a3','a2'), ('a2', 'a3'), ('a1','a3'), ('a3','a1'))), collision)
    
    
    ### Modifying the actor modifies the physics ###
    
    def testCanMoveActorToMovePhysics(self):
        """testCanMoveActorToMovePhysics: when moving the actor the physics object should move"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(radius=1.0, fixed=True, velocity=(-1,0)))
        a2.moveTo(5,0)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Move to
        a2.moveTo(4,0)
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        #
        # Move
        a1.moveTo(0,0)
        a2.moveTo(5,0)
        a2.move(-1,0)        
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        #
        # x, y
        a1.moveTo(0,0)
        a2.moveTo(5,5)
        a2.x = 4
        a2.y = 1
        self.w.updateWorld(1000.0)
        self.assertAlmostEqual(1, a1.x)
        self.assertAlmostEqual(3, a2.x)
        self.assertAlmostEqual(1, a2.y)
        
    def testRotatingActorRotatesPhysics(self):
        """testRotatingActorRotatesPhysics: rotating the actor should rotate the physics"""
        a1 = serge.actor.Actor('a1')
        a1.setPhysical(serge.physical.PhysicalConditions(radius=1.0, mass=1.0, velocity=(1.0, 0.0)))
        a1.moveTo(0,0)
        a2 = serge.actor.Actor('a2')
        a2.setPhysical(serge.physical.PhysicalConditions(width=2.0, height=1.0, fixed=True))
        a2.moveTo(3,0)
        self.w.addActor(a1)
        self.w.addActor(a2)
        #
        # Initial run should bounce back along x axis
        self.w.updateWorld(2000)
        self.assertAlmostEqual(0, a1.x)
        self.assertAlmostEqual(0, a1.y)
        #
        # Now rotate the actor by 45 and rerun - should bounce down
        a1.moveTo(0,0)
        a1.getPhysical().velocity = (1,0)
        a1.syncPhysics()
        a2.moveTo(2,0)
        a2.setAngle(45, True)
        #
        self.w.updateWorld(2000)
        self.assertAlmostEqual(-1.49002697, a1.x)
        self.assertAlmostEqual(-1.287928385, a1.y)
    
    ### Visual sync ###
    
    
    def testCanSyncPhysicsWithVisualActor(self):
        """testCanSyncPhysicsWithVisualActor: should be able to sync physics with an actor"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setPhysical(serge.physical.PhysicalConditions(width=50, height=50, mass=1, velocity=(10,0)))
        a.moveTo(50, 50)
        a.setLayerName('test')
        a.active = True
        w = serge.world.World('test')
        z1 = serge.zone.Zone()
        z1.active = True
        w.addZone(z1)
        w.addActor(a)
        w.updateWorld(1000)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('test', 0))
        w.renderTo(r, 1000)
        r.render()
        self.save(r, 1)
        # Check position
        self.assertAlmostEqual(60.0, a.x)
        self.assertAlmostEqual(50.0, a.y)
        # Check rendering
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 60, 50, 50, 50, 'green moved')

        
        
    def testSyncPhysicsVisualNoAngle(self):
        """testSyncPhysicsVisualNoAngle: should be able to avoid syncing the angle with physics"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setPhysical(serge.physical.PhysicalConditions(width=50, height=50, mass=1, velocity=(10,0)))
        a.getPhysical().body.angular_velocity = math.pi/2.0
        a.moveTo(50, 50)
        a.setLayerName('test')
        a.active = True
        w = serge.world.World('test')
        z1 = serge.zone.Zone()
        z1.active = True
        w.addZone(z1)
        w.addActor(a)
        w.updateWorld(1000)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('test', 0))
        w.renderTo(r, 1000)
        r.render()
        self.save(r, 1)
        # Check position
        self.assertAlmostEqual(60.0, a.x)
        self.assertAlmostEqual(50.0, a.y)
        self.assertAlmostEqual(0.0, a.getAngle())
        # Check rendering
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 60, 50, 50, 50, 'green moved')
        
    def testSyncPhysicsVisualWithAngle(self):
        """testSyncPhysicsVisualWithAngle: should be able to sync the physics angle"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setPhysical(serge.physical.PhysicalConditions(width=50, height=50, mass=1, velocity=(10,0), update_angle=True))
        a.getPhysical().body.angular_velocity = math.pi/4.0
        a.moveTo(50, 50)
        a.setLayerName('test')
        a.active = True
        w = serge.world.World('test')
        z1 = serge.zone.Zone()
        z1.active = True
        w.addZone(z1)
        w.addActor(a)
        w.updateWorld(1000)
        r = serge.render.Renderer()
        r.addLayer(serge.render.Layer('test', 0))
        w.renderTo(r, 1000)
        r.render()
        self.save(r, 1)
        # Check position
        self.assertAlmostEqual(60.0, a.x)
        self.assertAlmostEqual(50.0, a.y)
        self.assertAlmostEqual(-45.0, a.getAngle())
        # Check rendering
        self.check45Rect(r.getSurface(), (0, 255, 0, 255), 60, 50, 50, 50, 'green rotated')
    
    
if __name__ == '__main__':
    unittest.main()
