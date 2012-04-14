#@+leo-ver=4-thin
#@+node:paul.20120216232750.10758:@shadow utils.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:paul.20120216232750.10759:utils declarations
"""Some utilities that speed up common operations"""

import sys
import os
import pygame
import subprocess

import serge
import serge.render
import serge.actor
import serge.world

#@-node:paul.20120216232750.10759:utils declarations
#@+node:paul.20120216232750.10760:createLayers
def createLayers(engine, layers, cls):
    """Create a number of layers in the engine using the given class of layer"""
    renderer = engine.getRenderer()
    #
    # Find the right number of layers so that we can set the order correctly
    n = len(renderer.getLayers())
    for name in layers:
        layer = cls(name, n)
        renderer.addLayer(layer)
        n += 1
    
#@-node:paul.20120216232750.10760:createLayers
#@+node:paul.20120216232750.10761:createLayersForEngine
def createLayersForEngine(engine, layers):
    """Add a number of layers to the engine
    
    The layers parameter is a list of layer names. The layers are added to
    the renderer of the engine as successive layers in order.
    
    """
    createLayers(engine, layers, serge.render.Layer)
    
#@-node:paul.20120216232750.10761:createLayersForEngine
#@+node:paul.20120216232750.10762:createVirtualLayersForEngine
def createVirtualLayersForEngine(engine, layers):
    """Add a number of virtual layers to the engine
    
    The layers parameter is a list of layer names. The layers are added to
    the renderer of the engine as successive layers in order.
    
    The layers are created as virtual, meaning that this will render
    quicker than the real layers version, although compositing
    will not be possible.
    
    """
    createLayers(engine, layers, serge.render.VirtualLayer)        
        
#@-node:paul.20120216232750.10762:createVirtualLayersForEngine
#@+node:paul.20120216232750.10763:createWorldsForEngine
def createWorldsForEngine(engine, worlds):
    """Add a numer of worlds to the engine
    
    The words parameter is a list of names of the worlds to create.
    Each world is created with a single active zone which is quite
    large.
    
    """
    for name in worlds:
        world = serge.world.World(name)
        zone = serge.zone.Zone()
        zone.active = True
        zone.setSpatial(-2000, -2000, 4000, 4000)
        world.addZone(zone)
        engine.addWorld(world)
        

#@-node:paul.20120216232750.10763:createWorldsForEngine
#@+node:paul.20120216232750.10764:addActorToWorld
def addActorToWorld(world, actor, sprite_name=None, layer_name=None, center_position=None, physics=None, origin=None):
    """Create a new actor in the world
    
    If the center position is not specified then it is placed at the center of the screen.
    
    """
    #
    # If not position then put at the center
    if origin is None and center_position is None:
        renderer = serge.engine.CurrentEngine().getRenderer()
        center_position = (renderer.width/2.0, renderer.height/2.0)
    #
    # Create the new actor
    if sprite_name is not None:
        actor.setSpriteName(sprite_name)
    if layer_name is not None:
        actor.setLayerName(layer_name)
    if physics:
        actor.setPhysical(physics)
    if center_position is not None:
        actor.moveTo(*center_position)
    else:
        actor.setOrigin(*origin)
    world.addActor(actor)
    return actor


#@-node:paul.20120216232750.10764:addActorToWorld
#@+node:paul.20120216232750.10765:addSpriteActorToWorld
def addSpriteActorToWorld(world, tag, name, sprite_name, layer_name, center_position=None, physics=None):
    """Create a new actor in the world and set the visual to be the named sprite
    
    If the center position is not specified then it is placed at the center of the screen.
    
    """
    #
    # Create the new actor
    actor = serge.actor.Actor(tag, name)
    return addActorToWorld(world, actor, sprite_name, layer_name, center_position, physics)

#@-node:paul.20120216232750.10765:addSpriteActorToWorld
#@+node:paul.20120216232750.10766:addVisualActorToWorld
def addVisualActorToWorld(world, tag, name, visual, layer_name, center_position=None, physics=None):
    """Create a new actor in the world and set the visual 
    
    If the center position is not specified then it is placed at the center of the screen.
    
    """
    #
    # Create the new actor
    actor = serge.actor.Actor(tag, name)
    actor.visual = visual
    return addActorToWorld(world, actor, None, layer_name, center_position, physics)

#@-node:paul.20120216232750.10766:addVisualActorToWorld
#@+node:paul.20120216232750.10767:addTextToWorld
def addTextToWorld(world, text, name, theme, layer_name):
    """Add some text to the world"""
    L = theme.getProperty
    actor = addVisualActorToWorld(world, 'text', name, 
                serge.visual.Text(text, L('%s-colour' % name), 
                font_size=L('%s-font-size' % name)), layer_name, 
                center_position=L('%s-position' % name))
    return actor

#@-node:paul.20120216232750.10767:addTextToWorld
#@+node:paul.20120216232750.10768:addTextItemsToWorld
def addTextItemsToWorld(world, items, theme, layer_name):
    """Add multiple text items to the world"""
    for item in items:
        text, name = item[0:2]
        callback = None if len(item) == 2 else item[2]
        actor = addTextToWorld(world, text, name, theme, layer_name)
        if callback:
            actor.linkEvent(serge.events.E_LEFT_CLICK, callback)    


#@-node:paul.20120216232750.10768:addTextItemsToWorld
#@+node:paul.20120216232750.10769:addMuteButtonToWorlds
def addMuteButtonToWorlds(button, center_position, world_names=None):
    """Add a particular mute button to various worlds
    
    If worlds is not specified then add to all the worlds currently in the engine.
    
    """
    engine = serge.engine.CurrentEngine()
    if world_names is None:
        world_names = [world.name for world in engine.getWorlds()]
    for name in world_names:
        world = engine.getWorld(name)
        addActorToWorld(world, button, center_position=center_position)
    
#@-node:paul.20120216232750.10769:addMuteButtonToWorlds
#@+node:paul.20120216232750.10770:class MovieRecorder
class MovieRecorder(object):
    """Will record a movie of the game"""
    #@    @+others
    #@+node:paul.20120216232750.10771:__init__

    def __init__(self, path, make_movie=False, rate=1, in_memory=False):
        """Initialise the MovieRecorder
        
        If make_movie is True then we will convert the frames to a movie
        
        """
        self.path = path
        self.basename = os.path.splitext(path)[0]
        self.engine = serge.engine.CurrentEngine()
        self.renderer = self.engine.getRenderer()
        self.frame_count = 1
        self.skip_frames = rate
        self.skipped_frames = 0
        self.clearFrames()
        #
        self.engine.linkEvent(serge.events.E_AFTER_RENDER, self.makeFrame)
        if make_movie:
            self.engine.linkEvent(serge.events.E_AFTER_STOP, self.makeMovie)
        #
        self.in_memory = in_memory
        self.frames = []
        
    #@-node:paul.20120216232750.10771:__init__
    #@+node:paul.20120216232750.10772:makeFrame
    def makeFrame(self, obj, arg):
        """Make a frame"""
        self.skipped_frames += 1
        if self.skipped_frames >= self.skip_frames:
            self.skipped_frames = 0
            if self.in_memory:
                self.frames.append(self.renderer.getSurface().copy())
            else:
                pygame.image.save(self.renderer.getSurface(), self._getName(self.frame_count))
            self.frame_count += 1
        
    #@-node:paul.20120216232750.10772:makeFrame
    #@+node:paul.20120216232750.10773:clearFrames
    def clearFrames(self):
        """Clear all current frames"""
        for i in xrange(1, 1000000):
            if os.path.isfile(self._getName(i)):
                os.remove(self._getName(i))
            else:
                break

    #@-node:paul.20120216232750.10773:clearFrames
    #@+node:paul.20120216232750.10774:makeMovie
    def makeMovie(self, obj, arg):
        """Convert the frames to movie"""
        if self.in_memory:
            self._dumpFiles()
        cmd = 'cd %s; mencoder mf://%s -mf w=%d:h=%d:fps=%d:type=png -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o %s' % (
            os.path.dirname(self.path), 
            '*.png', 
            self.renderer.width, self.renderer.height, 
            60/self.skip_frames,
            os.path.basename(self.path)
        )
        subprocess.call(cmd, shell=True)
        self.clearFrames()
                   
    #@-node:paul.20120216232750.10774:makeMovie
    #@+node:paul.20120216232750.10775:_getName
    def _getName(self, idx):
        """Return the filename"""
        return '%s-%07d.png' % (self.basename, idx)
        
    #@-node:paul.20120216232750.10775:_getName
    #@+node:paul.20120216232750.10776:_dumpFiles
    def _dumpFiles(self):
        """Dump all files out from memory"""
        for idx, frame in enumerate(self.frames):
            pygame.image.save(frame, self._getName(idx+1))
            
            
    #@-node:paul.20120216232750.10776:_dumpFiles
    #@-others
#@-node:paul.20120216232750.10770:class MovieRecorder
#@+node:paul.20120216232750.10777:class RecordDesktop
class RecordDesktop(serge.common.Loggable):
    """Use record my desktop to record the action"""
    #@    @+others
    #@+node:paul.20120216232750.10778:__init__

    def __init__(self, filename):
        """Initialise the RecordDesktop"""
        self.addLogger()
        #
        # Highly system specific!
        #
        # Find our window
        self.log.info('Looking for the main window')
        engine = serge.engine.CurrentEngine()
        #
        windows = subprocess.check_output(['wmctrl', '-lG']).splitlines()
        for window in windows:
            parts = window.split()
            x, y, width, height = parts[2:6]
            name = ' '.join(parts[7:])
            if name == engine.title:
                break
        else:
            raise ValueError('Could not find the main window!')
        #import pdb; pdb.set_trace()
        #
        # Now start the recording
        self.log.info('Starting "recordmydesktop"')
        self.child = subprocess.Popen(['recordmydesktop', '--width', width, '--height', height,
            '-x', x, '-y', y, '-o', filename, '--fps', '60'])
        #
        # Hook completion so we can quit
        engine.linkEvent(serge.events.E_AFTER_STOP, self.stop)
        
    #@-node:paul.20120216232750.10778:__init__
    #@+node:paul.20120216232750.10779:stop
    def stop(self, obj, arg):
        """Stop the recording"""
        self.log.info('Asking "recordmydesktop" to compile the video now')
        self.child.terminate()
        self.child.wait()


    #@-node:paul.20120216232750.10779:stop
    #@-others
#@-node:paul.20120216232750.10777:class RecordDesktop
#@+node:paul.20120216232750.10780:checkPythonVersion
def checkPythonVersion():
    """Check a suitable Python version is installed"""
    if sys.version_info[0] == 3:
        print 'Python 3 is not supported'
        return False
    elif sys.version_info[1] <= 5:
        print 'Python 2.6+ is required'
        return False
    return True

#@-node:paul.20120216232750.10780:checkPythonVersion
#@+node:paul.20120216232750.10781:checkNetworkXVersion
def checkNetworkXVersion(need_version):
    """Check a suitable version of NetworkX is installed"""
    try:
        import networkx
    except ImportError:
        print 'networkx is required.\nTry "easy_install networkx" or visit http://networkx.lanl.gov/'
        return False
        
    # Attempt to check correct version
    try:
        version = float(networkx.__version__)
    except:
        # Ok, this didn't work so probably we will fail later with a more direct error!
        pass
    else:
        if version < need_version:
            print '\n\nnetworkx >= version 1.5 is required. Found %s.\n' % version
            print 'Try "easy_install networkx" or visit http://networkx.lanl.gov/' 
            print 'You may have to remove your version using synaptic first.\n\n'
            return False
    return True
    


#@-node:paul.20120216232750.10781:checkNetworkXVersion
#@+node:paul.20120216232750.10782:worldCallback
def worldCallback(name, sound=None):
    """Return an event callback to switch to a certain world"""
    def callback(obj, arg):
        if sound:
            serge.sound.Sounds.play(sound)
        serge.engine.CurrentEngine().setCurrentWorldByName(name)
    #
    return callback
    
#@-node:paul.20120216232750.10782:worldCallback
#@+node:paul.20120216232750.10783:backToPreviousWorld
def backToPreviousWorld(sound=None):
    """Return an event callback to switch back to the previous world"""
    def callback(obj, arg):
        if sound:
            serge.sound.Sounds.play(sound)
        serge.engine.CurrentEngine().goBackToPreviousWorld()
    #
    return callback

#@-node:paul.20120216232750.10783:backToPreviousWorld
#@+node:paul.20120216232750.10784:getGamePath
def getGamePath(*parts):
    """Return a path based on the main game folder"""
    return os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(serge.__file__)), '..', *parts))
    
#@-node:paul.20120216232750.10784:getGamePath
#@-others
#@-node:paul.20120216232750.10758:@shadow utils.py
#@-leo
