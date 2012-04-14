"""Tests for the rendering part"""

import unittest
import time
import pygame

import serge.render
import serge.engine
import serge.actor
import serge.visual
import serge.world
import serge.events
import serge.blocks.utils

from helper import *

class TestRender(unittest.TestCase, VisualTester):
    """Tests for the Render"""

    def setUp(self):
        """Set up the tests"""
        serge.visual.Register.clearItems()
        self.r = serge.render.Renderer()
        self.l1 = TestLayer('one')
        self.l2 = TestLayer('two')
        self.l3 = TestLayer('three')
        TestLayer.count = 0
        e = serge.engine.Engine()
        serge.engine.SetCurrentEngine(e)
        
    def tearDown(self):
        """Tear down the tests"""

    ### Layers ###
    
    def testCanAddLayer(self):
        """testCanAddLayer: should be able to add layer"""
        self.r.addLayer(self.l1)
        self.assertEqual(1, len(self.r.layers))
        
    def testCanRemoveLayer(self):
        """testCanRemoveLayer: should be able to remove layer"""
        self.r.addLayer(self.l1)
        self.r.removeLayer(self.l1)
        self.assertEqual(0, len(self.r.layers))

    def testCanRemoveLayerByName(self):
        """testCanRemoveLayerByName: should be able to remove a layer by name"""
        self.r.addLayer(self.l1)
        self.r.removeLayerNamed(self.l1.name)        
        self.assertRaises(serge.render.UnknownLayer, self.r.getLayer, self.l1.name)
    
    def testFailRemoveLayerByBadName(self):
        """testFailRemoveLayerByBadName: should fail when removing a layer by name that isn't recognized"""
        self.assertRaises(serge.render.UnknownLayer, self.r.removeLayerNamed, self.l1.name)                
         
    def testCanClearLayer(self):
        """testCanClearLayer: should be able to clear layer all layers"""
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.clearLayers()
        self.assertEqual(0, len(self.r.layers))

    def testCanIterateLayers(self):
        """testCanIterateLayers: should be able to iterate through layers"""
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.assertEqual(['one', 'two'], [l.name for l in self.r.getLayers()])        
            
    def testFailIfAddDuplicate(self):
        """testFailIfAddDuplicate: should fail if adding duplicate layer"""
        self.r.addLayer(self.l1)
        self.assertRaises(serge.render.DuplicateLayer, self.r.addLayer, self.l1)
        
    def testFailIfRemoveMissingLayer(self):
        """testFailIfRemoveMissingLayer: should fail if removing missing layer"""
        self.assertRaises(serge.render.UnknownLayer, self.r.removeLayer, self.l1)

    def testCanGetLayerByName(self):
        """testCanGetLayerByName: should be able to get layer by name"""
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.assertEqual(self.l1, self.r.getLayer('one'))
        self.assertEqual(self.l2, self.r.getLayer('two'))
        
    def testFailIfGetByMissingName(self):
        """testFailIfGetByMissingName: should fail if try to get missing layer"""
        self.assertRaises(serge.render.UnknownLayer, self.r.getLayer, 'one')
        
            

    ### Rendering order ###
    
    def testCanCallRendering(self):
        """testCanCallRendering: should be able to call the rendering"""
        self.r.addLayer(self.l1)
        self.r.render()
        self.assertEqual(1, self.l1.executed)
        
    def testWithNoOrderShouldBeByAdded(self):
        """testWithNoOrderShouldBeByAdded: should follow order added if no order specified"""
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.addLayer(self.l3)
        self.r.render()
        self.assert_(self.l1.executed < self.l2.executed)
        self.assert_(self.l2.executed < self.l3.executed)
        self.assertEqual(3, self.l3.executed)

    def testCanOrderRendering(self):
        """testCanOrderRendering: should be able to render in order"""
        self.l1.order = 10
        self.l2.order = 20
        self.l3.order = 0
        #
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.addLayer(self.l3)
        self.r.render()
        self.assert_(self.l3.executed < self.l1.executed)
        self.assert_(self.l1.executed < self.l2.executed)
        self.assertEqual(3, self.l2.executed)
        
    def testCanTurnALayerOff(self):
        """testCanTurnALayerOff: should be able to turn a layer off"""
        self.l1.order = 10
        self.l2.order = 20
        self.l3.order = 0
        self.l2.active = False
        #
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.addLayer(self.l3)
        self.r.render()
        self.assert_(self.l3.executed < self.l1.executed)
        self.assertEqual(1e30, self.l2.executed)
        
        
    ### Visual ###
    
    def testCanCreateBackbuffer(self):
        """testCanCreateBackbuffer: should be able to create a back buffer"""
        r = serge.render.Renderer(200,100)
        self.assert_(isinstance(r.getSurface(), pygame.Surface))
        
    def testOneLayerRendersToResult(self):
        """testOneLayerRendersToResult: one layer should render to the overall result"""
        r = serge.render.Renderer(200,100)
        l = serge.render.Layer('one', 1)
        r.addLayer(l)
        pygame.draw.circle(l.getSurface(), (255,255,255), (100,50), 50, 1)
        r.render()
        self.assertEqual((255, 255, 255, 255), r.getSurface().get_at((50, 50)))
        self.assertEqual((0, 0, 0, 255), r.getSurface().get_at((51, 50)))
                
    def testTwoLayersShouldRenderToResult(self):
        """testTwoLayersShouldRenderToResult: two layers should render together"""
        r = serge.render.Renderer(200,100)
        l1 = serge.render.Layer('front', 1)
        r.addLayer(l1)
        l2 = serge.render.Layer('back', 0)
        r.addLayer(l2)
        pygame.draw.circle(l1.getSurface(), (255,0,0), (100,50), 50, 2)
        pygame.draw.circle(l2.getSurface(), (255,255,255), (75,50), 25, 2)
        r.render()
        #
        # At 50,50 we should get the front colour (ie red)
        self.assertEqual((255, 0, 0, 255), r.getSurface().get_at((50, 50)))
        # At 75, 75 we should get the back colour (ie white)
        self.assertEqual((255, 255, 255, 255), r.getSurface().get_at((74, 74)))
        # At 53, 53 we didn't draw so should be black
        self.assertEqual((0, 0, 0, 255), r.getSurface().get_at((53, 53)))
        
    def testRerenderShouldClear(self):
        """testRerenderShouldClear: when re-rendering the old images should be gone"""
        r = serge.render.Renderer(200,100)
        l1 = serge.render.Layer('front', 1)
        r.addLayer(l1)
        l2 = serge.render.Layer('back', 0)
        r.addLayer(l2)
        pygame.draw.circle(l1.getSurface(), (255,0,0), (100,50), 50, 2)
        pygame.draw.circle(l2.getSurface(), (255,255,255), (75,50), 25, 2)
        r.render()
        # Now it is dirty - so remove layers and then rerender, should be nothing there
        r.clearLayers()
        r.preRender()
        r.render()
        #
        self.assertEqual((0, 0, 0, 255), r.getSurface().get_at((50, 50)))
        self.assertEqual((0, 0, 0, 255), r.getSurface().get_at((74, 74)))
        self.assertEqual((0, 0, 0, 255), r.getSurface().get_at((53, 53)))        
        
    def testRerenderLayersShouldBeClear(self):
        """testRerenderLayersShouldBeClear: when re-rendering each layer should be clear"""
        r = serge.render.Renderer(200,100)
        l1 = serge.render.Layer('front', 1)
        r.addLayer(l1)
        l2 = serge.render.Layer('back', 0)
        r.addLayer(l2)
        pygame.draw.circle(l1.getSurface(), (255,0,0), (100,50), 50, 2)
        pygame.draw.circle(l2.getSurface(), (255,255,255), (75,50), 25, 2)
        #
        self.assertEqual((255, 0, 0, 255), l1.getSurface().get_at((50, 50)))
        self.assertEqual((255, 255, 255, 255), l2.getSurface().get_at((50, 50)))
        #
        r.render()
        # Now it is dirty - so move rendering on layers and then rerender, should be nothing there
        r.preRender()
        r.render()
        #
        # We didn't draw so individual layers should be clear
        self.assertEqual((0, 0, 0, 0), l1.getSurface().get_at((50, 50)))
        self.assertEqual((0, 0, 0, 0), l2.getSurface().get_at((50, 50)))
        
    def testCanSetBackcolour(self):
        """testCanSetBackcolour: should be able to set backcolour"""
        r = serge.render.Renderer(200,100, backcolour=(255,0,0))
        r.preRender()
        r.render()
        self.assertEqual((255, 0, 0, 255), r.getSurface().get_at((50, 50)))
    
        
    ### Serialize ###
    
    def testCanSerializeAndRestorCamera(self):
        """testCanSerializeAndRestorCamera: can restore renderer with camera"""
        r = serge.render.Renderer(200,100, backcolour=(255,0,0))
        c = serge.camera.Camera()
        c.setSpatialCentered(50, 60, 70, 80)
        r.setCamera(c)
        r2 = serge.serialize.Serializable.fromString(r.asString())
        #
        self.assertEqual(50, r2.getCamera().x)        
        self.assertEqual(60, r2.getCamera().y)
        self.assertEqual(200, r2.getCamera().width) # Width and height should be reset
        self.assertEqual(100, r2.getCamera().height)
                
    ### General introspection ###
    
    def testCanFindScreenSize(self):
        """testCanFindScreenSize: should be able to find the screen extent"""
        r = serge.render.Renderer()
        self.assertEqual((640, 480), r.getScreenSize())
        
    def testCanCreateEngineWithCertainScreen(self):
        """testCanCreateEngineWithCertainScreen: should be able to create an engine with a screen size"""
        e = serge.engine.Engine(width=50, height=60, title='test', backcolour=(0,0,0))
        self.assertEqual((50, 60), e.getRenderer().getScreenSize())

    def testCanGetLayerBefore(self):
        """testCanGetLayerBefore: should be able to get layer before a given layer"""
        self.l1.order = 10
        self.l2.order = 20
        self.l3.order = 30
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.addLayer(self.l3)
        #
        self.assertEqual(self.l1, self.r.getLayerBefore(self.l2))
        self.assertEqual(self.l2, self.r.getLayerBefore(self.l3))
        
    def testGetLayerBeforeWithNothingShouldFail(self):
        """testGetLayerBeforeWithNothingShouldFail: should fail when getting a layer before the bottom"""
        self.l1.order = 10
        self.l2.order = 20
        self.l3.order = 30
        #
        self.assertRaises(serge.render.NoLayer, self.r.getLayerBefore, self.l1)
        #
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.addLayer(self.l3)
        #
        self.assertRaises(serge.render.NoLayer, self.r.getLayerBefore, self.l1)
 
    def testCanOrderActors(self):
        """testCanOrderActors: should be able to order actors according to rendering order"""
        self.l1.order = 10
        self.l2.order = 20
        self.l3.order = 30
        self.r.addLayer(self.l1)
        self.r.addLayer(self.l2)
        self.r.addLayer(self.l3)
        #
        # Create some actors
        a1 = serge.actor.Actor('a1')
        a1.setLayerName('one')
        a2 = serge.actor.Actor('a2')
        a2.setLayerName('two')
        a3 = serge.actor.Actor('a3')
        a3.setLayerName('three')
        #
        # Get order
        self.assertEqual([a1, a2, a3], self.r.orderActors([a3, a2, a1]))
        #
        # Now switch layers
        a1.setLayerName('three')
        a3.setLayerName('one')
        self.assertEqual([a3, a2, a1], self.r.orderActors([a3, a2, a1]))
        #
        # Now switch layers
        self.l1.order = 30
        self.l3.order = 10
        self.assertEqual([a1, a2, a3], self.r.orderActors([a3, a2, a1]))
        
             
    ### Virtual Layers ###
    
    def testCanUseAVirtualLayer(self):
        """testCanUseAVirtualLayer: should be able to have virtual layers"""
        #
        # Some things to draw
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        serge.visual.Register.registerItem('blue', p('bluerect.png'))
        #
        # Create the world to play in
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        green = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'green', 'front', (75, 75))
        blue = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'blue', 'back', (75, 75))
        #
        # Get rendering surfaces
        r = e.getRenderer()
        l1 = serge.render.VirtualLayer('front', 1)
        r.addLayer(l1)
        l2 = serge.render.VirtualLayer('back', 0)
        r.addLayer(l2)
        #
        # Surfaces should be the same
        self.assertEqual(l1.getSurface(), l2.getSurface())
        self.assertEqual(l1.getSurface(), r.getSurface())
        #
        # Do the rendering
        w.renderTo(r, 0)
        r.render()
        self.save(r, 1)
        #
        # Check that green is in front
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green')
        #
        # Change the order
        green.setLayerName('back')
        blue.setLayerName('front')
        # Trigger reshuffle via adding another actor
        w.addActor(serge.actor.Actor('dummy'))
        #
        r.preRender()
        w.renderTo(r, 0)
        r.render()
        self.save(r, 2)
        #
        # Check that blue is in front
        self.checkRect(r.getSurface(), (0, 0, 255, 255), 75, 75, 50, 50, 'blue')
        
        
    def testCanCombineVirtualWithRealLayers(self):
        """testCanCombineVirtualWithRealLayers: should be able to combine virtual and real layers together"""
        #
        # Some things to draw
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        serge.visual.Register.registerItem('blue', p('bluerect.png'))
        serge.visual.Register.registerItem('red', p('allrect2.png'))
        #
        # Create the world to play in
        e = serge.engine.Engine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        green = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'green', 'front', (75, 75))
        red = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'red', 'middle', (75, 75))
        blue = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'blue', 'back', (75, 75))
        #
        # Get rendering surfaces
        r = e.getRenderer()
        l1 = serge.render.Layer('front', 2)
        r.addLayer(l1)
        l2 = serge.render.Layer('middle', 1)
        r.addLayer(l2)
        l3 = serge.render.VirtualLayer('back', 0)
        r.addLayer(l3)
        #
        # Surfaces should be different
        self.assertNotEqual(l1.getSurface(), l2.getSurface())
        self.assertNotEqual(l2.getSurface(), l3.getSurface())
        self.assertEqual(l3.getSurface(), r.getSurface())
        #
        # Do the rendering
        w.renderTo(r, 0)
        r.render()
        self.save(l1, 1)
        self.save(l2, 2)
        self.save(l3, 3)
        self.save(r, 4)
        #
        # Check that green is in front overall
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green overall')
        # Check that green is in front of layer 1
        self.checkRect(l1.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green front', check_alpha=False)
        # Check that red is in front of layer 2
        self.checkRect(l2.getSurface(), (255, 0, 0, 255), 75, 75, 50, 50, 'red 2', black=(0,0,0,0))
        # Check that red is in front of layer 3
        self.checkRect(l3.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green 3')
        
    def testVirtualLayersAreQuicker(self):
        """testVirtualLayersAreQuicker: should see an increase in render speed when using virtual layers"""
        #
        # Some things to draw
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        serge.visual.Register.registerItem('blue', p('bluerect.png'))
        #
        results = []
        for layer_cls in (serge.render.VirtualLayer, serge.render.Layer):
            #
            # Create the world to play in
            e = serge.engine.Engine()
            serge.blocks.utils.createWorldsForEngine(e, ['one'])
            w = e.getWorld('one')
            green = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'green', 'front', (75, 75))
            blue = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'blue', 'back', (75, 75))
            #
            # Get rendering surfaces
            r = e.getRenderer()
            l1 = layer_cls('front', 1)
            r.addLayer(l1)
            l2 = layer_cls('back', 0)
            r.addLayer(l2)
            #
            # Do the rendering a lot
            start = time.time()
            for i in range(200):
                r.preRender()
                w.renderTo(r, 0)
                r.render()
            results.append(time.time()-start)
        #
        # Compare ratio of rendering times
        ratio = results[0]/results[1]
        w.log.info('Actual ratio obtained was %f' % ratio)
        self.assert_(ratio < 0.5, ('Ratio of speeds too high (%f)' % ratio))
        

    ### Pre and post processing a layer ###
    
    def testCanPreprocessALayer(self):
        """testCanPreprocessALayer: should be able to preprocess a layer"""
        def pre(layer, arg):
            """Sets a couple of pixels"""
            layer.getSurface().set_at((10,10), (255, 0, 0, 255))
            layer.getSurface().set_at((75,75), (255, 0, 0, 255))
        #
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
        l1 = serge.render.Layer('front', 2)
        r.addLayer(l1)
        l1.linkEvent(serge.events.E_BEFORE_RENDER, pre)
        #
        # Do the rendering
        r.preRender()
        w.renderTo(r, 0)
        r.render()
        self.save(l1, 1)
        #
        # Check that green is in front overall
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green overall')
        self.assertEqual((255,0,0,255), self.r.getSurface().get_at((10, 10)))
        self.assertEqual((0,255,0,255), self.r.getSurface().get_at((75, 75)))
        
    def testCanPostProcessALayer(self):
        """testCanPostProcessALayer: should be able to post process a layer"""
        def post(layer, arg):
            """Sets a couple of pixels"""
            layer.getSurface().set_at((10,10), (255, 0, 0, 255))
            layer.getSurface().set_at((75,75), (255, 0, 0, 255))
        #
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
        l1 = serge.render.Layer('front', 2)
        r.addLayer(l1)
        l1.linkEvent(serge.events.E_AFTER_RENDER, post)
        #
        # Do the rendering
        r.preRender()
        w.renderTo(r, 0)
        r.render()
        self.save(r, 1)
        #
        # Check that green is in front overall
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green overall')
        self.assertEqual((255,0,0,255), self.r.getSurface().get_at((10, 10)))
        self.assertEqual((255,0,0,255), self.r.getSurface().get_at((75, 75)))
            
    def testCanPreAndPostProcessLayer(self):
        """testCanPreAndPostProcessLayer: should be able to pre and post process a layer"""
        def pre(layer, arg):
            """Sets a couple of pixels"""
            layer.getSurface().set_at((10,10), (255, 0, 0, 255))
            layer.getSurface().set_at((75,75), (255, 0, 0, 255))
        def post(layer, arg):
            """Sets a couple of pixels"""
            layer.getSurface().set_at((76,76), (255, 0, 0, 255))
        #
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
        l1 = serge.render.Layer('front', 2)
        r.addLayer(l1)
        l1.linkEvent(serge.events.E_BEFORE_RENDER, pre)
        l1.linkEvent(serge.events.E_AFTER_RENDER, post)
        #
        # Do the rendering
        r.preRender()
        w.renderTo(r, 0)
        r.render()
        self.save(l1, 1)
        #
        # Check that green is in front overall
        self.checkRect(r.getSurface(), (0, 255, 0, 255), 75, 75, 50, 50, 'green overall')
        self.assertEqual((255,0,0,255), self.r.getSurface().get_at((10, 10)))
        self.assertEqual((0,255,0,255), self.r.getSurface().get_at((75, 75)))
        self.assertEqual((255,0,0,255), self.r.getSurface().get_at((76, 76)))
        
    def testCanRenderMovieFrames(self):
        """testCanRenderMovieFrame: should be able to render a movie frames"""
        #
        # Some things to draw
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        serge.visual.Register.registerItem('blue', p('bluerect.png'))
        #
        # Create the world to play in
        e = serge.engine.CurrentEngine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        green = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'green', 'front', (75, 75))
        blue = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'blue', 'back', (95, 95))
        #
        # Get rendering surfaces
        r = e.getRenderer()
        l1 = serge.render.VirtualLayer('front', 1)
        r.addLayer(l1)
        l2 = serge.render.VirtualLayer('back', 0)
        r.addLayer(l2)
        #
        # Clear frames
        try: os.remove(os.path.join('test', 'junk', 'movie-0000001.png'))
        except OSError: pass
        try: os.remove(os.path.join('test', 'junk', 'movie-0000002.png'))
        except OSError: pass
        #
        # A post-render movie maker
        maker = serge.blocks.utils.MovieRecorder(os.path.join('test', 'junk', 'movie'))
        #
        self.assertFalse(os.path.isfile(os.path.join('test', 'junk', 'movie-0000001.png')))
        self.assertFalse(os.path.isfile(os.path.join('test', 'junk', 'movie-0000002.png')))
        #
        # Do the rendering
        e.runAsync(60)
        time.sleep(0.5)
        e.stop()
        time.sleep(0.5)
        #
        self.assertTrue(os.path.isfile(os.path.join('test', 'junk', 'movie-0000001.png')))
        self.assertTrue(os.path.isfile(os.path.join('test', 'junk', 'movie-0000002.png')))
        
    def testCanRenderMovie(self):
        """testCanRenderMovie: should be able to render a movie"""
        #
        # Some things to draw
        serge.visual.Register.registerItem('green', p('greenrect.png'))
        serge.visual.Register.registerItem('blue', p('bluerect.png'))
        #
        # Create the world to play in
        e = serge.engine.CurrentEngine()
        serge.blocks.utils.createWorldsForEngine(e, ['one'])
        w = e.getWorld('one')
        green = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'green', 'front', (75, 75))
        blue = serge.blocks.utils.addSpriteActorToWorld(w, 'a1', 'a1', 'blue', 'back', (95, 95))
        #
        # Get rendering surfaces
        r = e.getRenderer()
        l1 = serge.render.VirtualLayer('front', 1)
        r.addLayer(l1)
        l2 = serge.render.VirtualLayer('back', 0)
        r.addLayer(l2)
        #
        # Clear frames
        try: os.remove(os.path.join('test', 'junk', 'movie-0000001.png'))
        except OSError: pass
        try: os.remove(os.path.join('test', 'junk', 'movie-0000002.png'))
        except OSError: pass
        try: os.remove(os.path.join('test', 'junk', 'movie.avi'))
        except OSError: pass
        #
        # A post-render movie maker
        maker = serge.blocks.utils.MovieRecorder(os.path.join('test', 'junk', 'movie.avi'), make_movie=True)
        #
        self.assertFalse(os.path.isfile(os.path.join('test', 'junk', 'movie-0000001.png')))
        self.assertFalse(os.path.isfile(os.path.join('test', 'junk', 'movie-0000002.png')))
        #
        # Do the rendering
        e.runAsync(60)
        time.sleep(0.5)
        e.stop()
        time.sleep(2)
        #
        self.assertFalse(os.path.isfile(os.path.join('test', 'junk', 'movie-0000001.png')))
        self.assertFalse(os.path.isfile(os.path.join('test', 'junk', 'movie-0000002.png')))
        self.assertTrue(os.path.isfile(os.path.join('test', 'junk', 'movie.avi')))
              
        
class TestLayer(serge.render.Layer):
    """A test layer"""
    
    count = 0
    
    def __init__(self, name):
        """Initialise the TestLayer"""
        super(TestLayer, self).__init__(name, 0)
        self.executed = 1e30
        
    def render(self, surface):
        """Render to a surface"""
        TestLayer.count += 1
        self.executed = TestLayer.count
        
if __name__ == '__main__':
    unittest.main()
