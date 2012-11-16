"""Tests for Camera"""

import unittest
import os
import pygame

from helper import *

import serge.camera
import serge.world
import serge.zone
import serge.actor
import serge.render

def p(f):
    """Return full path to file"""
    return os.path.join(os.path.abspath(os.curdir), 'test', 'images', f)

class TestCamera(unittest.TestCase, VisualTester):
    """Tests for the Camera"""

    def setUp(self):
        """Set up the tests"""
        self.c = serge.camera.Camera()
        self.w = serge.world.World('main')
        self.z = serge.zone.Zone()
        self.w.addZone(self.z)
        for x in range(11):
            for y in range(11):
                a = serge.actor.Actor('a', '%d_%d' % (x, y))
                a.setSpatialCentered(x*10, y*10, 5, 5)
                self.z.addActor(a)
        serge.visual.Register.clearItems()
                
    def tearDown(self):
        """Tear down the tests"""


    ### Tests ###
    
    def testCanCreate(self):
        """testCanCreate: should be able to create a camera"""
    
    def getActors(self, *names):
        """Return a list of actors"""
        return [self.w.findActorByName(n) for n in names]

    def checkRect(self, surface, colour, cx, cy, w, h, name):
        """Check that a rectangle is in the right place"""
        for dy in (-1, +1):
            for dx in (-1, +1):
                self.assertEqual((0,0,0,255), surface.get_at((cx + dx*(w/2+2), cy + dy*(h/2+2))), 
                        '%s - Failed black test at %d, %d' % (name, dx, dy))
                self.assertEqual(colour, surface.get_at((cx + dx*(w/2-2), cy + dy*(h/2-2))), 
                        '%s - Failed colour test at %d, %d' % (name, dx, dy))

    ### Tests ###
        
    def testCanSetSpatialRange(self):
        """testCanSetSpatialRange: should be able to set spatial range"""
        self.c.setSpatial(50, 60, 10, 11)
        x, y, w, h = self.c.getSpatial()
        self.assertEqual(50, x)
        self.assertEqual(60, y)
        self.assertEqual(10, w)
        self.assertEqual(11, h)
        
    def testCanSeeObjects(self):
        """testCanSeeObjects: should be able to see objects"""
        # Direct containment
        self.c.setSpatial(50, 50, 2, 2)
        self.assertEqual(set(self.getActors('5_5')), set(self.c.canSeeActors(self.w.findActorsByTag('a'))))
        # Overlapping        
        self.c.setSpatial(50, 50, 11, 2)
        self.assertEqual(set(self.getActors('5_5', '6_5')), set(self.c.canSeeActors(self.w.findActorsByTag('a'))))
        # Move overlapping
        self.c.setSpatial(50, 50, 11, 11)
        self.assertEqual(set(self.getActors('5_5', '6_5', '5_6', '6_6')), set(self.c.canSeeActors(self.w.findActorsByTag('a'))))
                
    def testCanScale(self):
        """testCanScale: should be able to scale and see more / less objects"""
        # Direct containment
        self.c.setSpatialCentered(50, 50, 9, 9)
        self.assertEqual(set(self.getActors('5_5')), set(self.c.canSeeActors(self.w.findActorsByTag('a'))))
        # Double the size
        self.c.scale(2.0)
        self.assertEqual(set(self.getActors('4_4', '4_5', '4_6', '5_4', '5_5', '5_6', '6_4', '6_5', '6_6')), 
                    set(self.c.canSeeActors(self.w.findActorsByTag('a'))))
        # Back
        self.c.scale(0.5)
        self.assertEqual(set(self.getActors('5_5')), set(self.c.canSeeActors(self.w.findActorsByTag('a'))))
        
        
    ### Converting world to camera coordinates ###
    
    def testCanSeeOffsets(self):
        """testCanSeeOffsets: should be able to see offsets from the camera"""
        self.c.setSpatialCentered(50, 50, 9, 9)
        a = self.w.findActorByName('5_5')
        self.assertEqual((2, 2), self.c.getRelativeLocation(a))
        a.move(1, -1)
        self.assertEqual((3, 1), self.c.getRelativeLocation(a))
        
    def testCanSeeOffsetsCentered(self):
        """testCanSeeOffsetsCentered: should be able to see offsets from the camera centered"""
        self.c.setSpatialCentered(50, 50, 10, 20)
        a = self.w.findActorByName('5_5')
        self.assertEqual((0, 0), self.c.getRelativeLocationCentered(a))
        a.move(2, -2)
        self.assertEqual((2, -2), self.c.getRelativeLocationCentered(a))
        
        
    ### Serializing ###
            
    def testCanSerialize(self):
        """testCanSerialize: should be able to serialize the camera"""
        self.c.setSpatial(50, 60, 10, 20)
        a = serge.serialize.Serializable.fromString(self.c.asString()) 
        x, y, w, h = a.getSpatial()
        self.assertEqual(50, x)
        self.assertEqual(60, y)
        self.assertEqual(10, w)
        self.assertEqual(20, h)

    ### Camera movement ###
    
    def testCanSetDesiredLocation(self):
        """testCanSetDesiredLocation: should be able to set desired location"""
        self.c.setTarget(serge.geometry.Point(0, 10))
        self.assertEqual(0, self.c.getTarget().x)
        self.assertEqual(10, self.c.getTarget().y)
                
        
    def testCanMoveTowardsDesiredLocation(self):
        """testCanMoveTowardsDesiredLocation: should be able to move towards the desired location"""
        #
        # Go to target in 10 steps of 10
        self.c.setSpatialCentered(50, 50, 10, 20)
        self.c.setTarget(serge.geometry.Point(0, 10))
        for i in range(10):
            self.c.update(20)
        first = self.c.getSpatial()
        #
        # Now go in 20 steps of 5
        self.c.setSpatialCentered(50, 50, 10, 20)
        self.c.setTarget(serge.geometry.Point(0, 10))
        for i in range(20):
            self.c.update(10)
        second = self.c.getSpatial()
        #
        self.assertEqual(first.x, second.x)
        self.assertEqual(first.y, second.y)
                    
    def testCanGetToDesiredLocation(self):
        """testCanGetToDesiredLocation: should eventually get to the desired location"""
        self.c.setSpatialCentered(50, 50, 10, 20)
        self.c.setTarget(serge.geometry.Point(0, 10))
        for i in range(1000):
            self.c.update(10)
        self.assertEqual(0, self.c.x)
        self.assertEqual(10, self.c.y)
        
    ### Camera rendering ###
    
    def testCanRenderWithBigCamera(self):
        """testCanRenderWithBigCamera: should render transparently with a big camera"""
        self.c.setSpatial(0, 0, 500, 500)
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.setCamera(self.c)
        r.addLayer(serge.render.Layer('main', 0))
        z = serge.zone.Zone()
        z.addActor(a)
        self.w.addZone(z)
        self.w.renderTo(r, 100)
        r.render()
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'initial')
        
    def testOutsideOfCameraDoesNotRender(self):
        """testOutsideOfCameraDoesNotRender: objects out of the range of camera should not render"""
        self.c.setSpatial(0, 0, 5, 5)
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.setCamera(self.c)
        r.addLayer(serge.render.Layer('main', 0))
        z = serge.zone.Zone()
        z.addActor(a)
        self.w.addZone(z)
        self.w.renderTo(r, 100)
        r.render()
        self.checkRect(r.getSurface(), (0,0,0,255), 60, 60, 50, 50, 'invisible')
        
    def testOffsetCameraShouldOffsetSpriteNames(self):
        """testOffsetCameraShouldOffsetSpriteNames: sprites should be moved according to the camera offset"""
        self.c.setSpatial(-5, -10, 500, 500)
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.setCamera(self.c)
        r.addLayer(serge.render.Layer('main', 0))
        z = serge.zone.Zone()
        z.addActor(a)
        self.w.addZone(z)
        self.w.renderTo(r, 100)
        r.render()
        self.checkRect(r.getSurface(), (0,255,0,255), 65, 70, 50, 50, 'invisible')

    def testBlankLayerShouldNotRender(self):
        """testBlankLayerShouldNotRender: if have a blank layer then should not try to render"""
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('')
        a.moveTo(60, 60)
        z = serge.zone.Zone()
        z.addActor(a)
        r = serge.render.Renderer()
        self.w.addZone(z)
        self.w.renderTo(r, 100)
        
    def testCanScaleCameraToZoomIn(self):
        """testCanScaleCameraToZoomIn: camera can zoom in and out"""
        self.c.setSpatial(0, 0, 500, 500)
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(120, 120)
        r = serge.render.Renderer()
        r.setCamera(self.c)
        r.addLayer(serge.render.Layer('main', 0))
        z = serge.zone.Zone()
        z.addActor(a)
        z.active = True
        w = serge.world.World('main')
        w.addZone(z)
        #
        w.setZoom(2.0, 120, 120)
        w.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 120, 120, 100, 100, 'zoomed 2')
        #
        r.preRender()
        w.setZoom(1.0, 120, 120)
        w.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.checkRect(r.getSurface(), (0,255,0,255), 120, 120, 50, 50, 'zoomed back to 1')
        #
        r.preRender()
        w.setZoom(0.5, 120, 120)
        w.renderTo(r, 100)
        r.render()
        self.save(r, 3)
        self.checkRect(r.getSurface(), (0,255,0,255), 120, 120, 25, 25, 'zoomed to 0.5')
        
    def testCanSetLayerToStaticCamera(self):
        """testCanSetLayerToStaticCamera: should be able to have a layer that doesn't move with the camera"""
        self.c.setSpatial(0, 0, 500, 500)
        s = serge.visual.Register.registerItem('green', p('greenrect.png'))
        a = serge.actor.Actor('a')
        a.setSpriteName('green')
        a.setLayerName('main')
        a.moveTo(60, 60)
        r = serge.render.Renderer()
        r.setCamera(self.c)
        r.addLayer(serge.render.Layer('main', 0))
        static = r.addLayer(serge.render.Layer('static', 0))
        static.setStatic(True)
        z = serge.zone.Zone()
        z.addActor(a)
        self.w.addZone(z)
        #
        # Original location
        self.w.renderTo(r, 100)
        r.render()
        self.save(r, 1)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'original')
        #
        # Should move when camera moves
        r.preRender()
        self.c.move(20, 20)
        self.w.renderTo(r, 100)
        r.render()
        self.save(r, 2)
        self.checkRect(r.getSurface(), (0,255,0,255), 60-20, 60-20, 50, 50, 'shifted')
        #
        # Now move actor to static layer
        a.setLayerName('static')
        r.preRender()
        self.w.renderTo(r, 100)
        r.render()
        self.save(r, 3)
        self.checkRect(r.getSurface(), (0,255,0,255), 60, 60, 50, 50, 'shifted but static')
        
    def testStaticLayersMouseEvents(self):
        """testStaticLayersMouseEvents: mouse events should work on static layers"""
        e = serge.engine.Engine()
        self.c.setSpatial(0, 0, 500, 500)
        a = serge.actor.Actor('a')
        a.setLayerName('main')
        a.setSpatialCentered(60, 60, 10, 10)
        r = e.getRenderer()
        r.setCamera(self.c)
        r.addLayer(serge.render.Layer('main', 0))
        static = r.addLayer(serge.render.Layer('static', 0))
        static.setStatic(True)
        z = serge.zone.Zone()
        z.addActor(a)
        w = serge.world.World('test')
        w.addZone(z)
        #        
        m = serge.input.Mouse(e)
        m.isClicked = lambda x : True
        pygame.mouse.get_pos = lambda : (60, 60)
        #
        # Initial should be on it
        m._actors_under_mouse = None
        e = m.getActorEvents(w)
        self.assertEqual(a, e[0][1])
        self.assertEqual(4, len(e))
        #
        # Move camera should not be there
        self.c.move(20, 20)
        m._actors_under_mouse = None
        e = m.getActorEvents(w)
        self.assertEqual([], e)
        #
        # Move to static layer should be there again
        a.setLayerName('static')
        m._actors_under_mouse = None
        e = m.getActorEvents(w)
        self.assertEqual(a, e[0][1])
        self.assertEqual(4, len(e))    

if __name__ == '__main__':
    unittest.main()
