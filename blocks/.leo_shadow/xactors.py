#@+leo-ver=4-thin
#@+node:paul.20120216232750.10711:@shadow actors.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:paul.20120216232750.10712:actors declarations
"""Blocks to help with actors"""

import serge.actor
import serge.engine
import serge.actor
import serge.events


#@-node:paul.20120216232750.10712:actors declarations
#@+node:paul.20120216232750.10713:class InvalidMenu
class InvalidMenu(Exception): """The menu was not valid"""
#@-node:paul.20120216232750.10713:class InvalidMenu
#@+node:paul.20120216232750.10714:class InvalidMenuItem
class InvalidMenuItem(Exception): """The menu item was not understood"""



#@-node:paul.20120216232750.10714:class InvalidMenuItem
#@+node:paul.20120216232750.10715:class ScreenActor
class ScreenActor(serge.actor.CompositeActor):
    """An actor to represent the logic associated with a screen of the game
    
    This actor is useful when encapsulating the logic associated with a specific
    screen in the game. The actor has useful properties and methods that
    make it easy to manage the logic.
    
    """
    #@    @+others
    #@+node:paul.20120216232750.10716:__init__

    def __init__(self, *args, **kw):
        """Initialise the ScreenActor"""
        super(ScreenActor, self).__init__(*args, **kw)
        
    #@-node:paul.20120216232750.10716:__init__
    #@+node:paul.20120216232750.10717:addedToWorld
    def addedToWorld(self, world):
        """The actor was added to the world"""
        super(ScreenActor, self).addedToWorld(world)
        self.world = world
        self.engine = serge.engine.CurrentEngine()
        self.keyboard = self.engine.getKeyboard()
        self.mouse = self.engine.getMouse()
        self.camera = self.engine.getRenderer().getCamera()
        self.broadcaster = serge.events.getEventBroadcaster()
        

    #@-node:paul.20120216232750.10717:addedToWorld
    #@-others
#@-node:paul.20120216232750.10715:class ScreenActor
#@+node:paul.20120216232750.10718:class RepeatedVisualActor
class RepeatedVisualActor(serge.actor.Actor):
    """An actor that shows multiple copies of a visual representation
    
    This actor is useful for showing the number of lives or missiles
    etc in a game.
    
    """
    #@    @+others
    #@+node:paul.20120216232750.10719:__init__

    def __init__(self, tag, name=None, repeat=5, spacing=10, orientation='horizontal'):
        """Initialise the RepeatedVisualActor"""
        super(RepeatedVisualActor, self).__init__(tag, name)
        self._repeat = repeat
        self._spacing = spacing
        self._current = repeat
        self._orientation = orientation

    #@-node:paul.20120216232750.10719:__init__
    #@+node:paul.20120216232750.10720:_resetVisual
    def _resetVisual(self):
        """Reset the visual item on the center point
        
        We need to override this because our size is not determined by our visual
        
        """
        #
        # Adjust our location so that we are positioned and sized appropriately
        cx, cy, _, _ = self.getSpatialCentered()
        #
        if self._orientation == 'horizontal':
            self.setSpatialCentered(cx, cy, 
                self._visual.width + self._spacing*(self._repeat-1), self._visual.height)
        else:
            self.setSpatialCentered(cx, cy, 
                self._visual.width, self._visual.height + self._spacing*(self._repeat-1))
        #
        # Here is a hack - sometimes the visual width changes and we want to update our width
        # so we let the visual know about us so it can update our width. This is almost 
        # certainly the wrong thing to do, but we have some tests in there so hopefully
        # the right thing becomes obvious later!
        self._visual._actor_parent = self
        
    #@-node:paul.20120216232750.10720:_resetVisual
    #@+node:paul.20120216232750.10721:renderTo
    def renderTo(self, renderer, interval):
        """Render ourself to the given renderer"""
        if self._visual:
            layer = renderer.getLayer(self.layer)
            camera = renderer.camera
            if layer.static:
                ox, oy = self.getOrigin()
            elif camera.canSee(self):
                ox, oy = camera.getRelativeLocation(self)
            else: 
                return # Cannot see me
            if self.layer:
                for i in range(self._current):
                    if self._orientation == 'horizontal':
                        x, y = (ox + i*self._spacing, oy)
                    else:
                        x, y = (ox, oy + i*self._spacing)
                    self._visual.renderTo(interval, renderer.getLayer(self.layer).getSurface(), (x, y))

    #@-node:paul.20120216232750.10721:renderTo
    #@+node:paul.20120216232750.10722:reduceRepeat
    def reduceRepeat(self, amount=1):
        """Reduce the repeat by a certain amount"""
        self.setRepeat(self._current - amount)
        
    #@-node:paul.20120216232750.10722:reduceRepeat
    #@+node:paul.20120216232750.10723:increaseRepeat
    def increaseRepeat(self, amount=1):
        """Increase the repeat by a certain amount"""
        self.setRepeat(self._current + amount)
        
    #@-node:paul.20120216232750.10723:increaseRepeat
    #@+node:paul.20120216232750.10724:getRepeat
    def getRepeat(self):
        """Return the current repeat"""
        return self._current

    #@-node:paul.20120216232750.10724:getRepeat
    #@+node:paul.20120216232750.10725:setRepeat
    def setRepeat(self, value):
        """Set the current repeat"""
        if self._current != value:
            self._current = value
            #
            # Reset the visual size
            ox, oy, w, h = self.getSpatial()
            if self._orientation == 'horizontal':
                w = self._visual.width + self._spacing*(self._current-1)
            else:
                h = self._visual.height + self._spacing*(self._current-1)
            self.setSpatial(ox, oy, w, h)
            self.log.debug('New spatial = %s' % self.getSpatial())
        
    #@-node:paul.20120216232750.10725:setRepeat
    #@+node:paul.20120216232750.10726:resetRepeat
    def resetRepeat(self):
        """Reset the repeat to the initial value"""
        self.setRepeat(self._repeat)
        
        
    #@-node:paul.20120216232750.10726:resetRepeat
    #@-others
#@-node:paul.20120216232750.10718:class RepeatedVisualActor
#@+node:paul.20120216232750.10727:class FormattedText
class FormattedText(serge.actor.Actor):
    """A text display that can be formatted"""
    #@    @+others
    #@+node:paul.20120216232750.10728:__init__

    def __init__(self, tag, name, format, colour, font_name='DEFAULT', font_size=12, justify='center', **kw):
        """Initialise the text"""
        super(FormattedText, self).__init__(tag, name)
        self.visual = serge.visual.Text('', colour, font_name, font_size, justify)
        self.format = format
        self.values = kw
        self.updateText()
        
    #@-node:paul.20120216232750.10728:__init__
    #@+node:paul.20120216232750.10729:updateText
    def updateText(self):
        """Update our text"""
        self.visual.setText(self.format % self.values)

    #@-node:paul.20120216232750.10729:updateText
    #@+node:paul.20120216232750.10730:setValue
    def setValue(self, name, value):
        """Set the value"""
        self.values[name] = value
        self.updateText()
            
    #@-node:paul.20120216232750.10730:setValue
    #@+node:paul.20120216232750.10731:getValue
    def getValue(self, name):
        """Get the values"""
        return self.values[name]

    #@-node:paul.20120216232750.10731:getValue
    #@-others
#@-node:paul.20120216232750.10727:class FormattedText
#@+node:paul.20120216232750.10732:class NumericText
class NumericText(FormattedText):
    """A helper actor to display some text with a single number in there"""
    #@    @+others
    #@+node:paul.20120216232750.10733:__init__

    def __init__(self, *args, **kw):
        """Initialise the text"""
        super(NumericText, self).__init__(*args, **kw)
        
    #@-node:paul.20120216232750.10733:__init__
    #@+node:paul.20120216232750.10734:updateText
    def updateText(self):
        """Update our text"""
        self.visual.setText(self.format % self.values['value'])

    #@-node:paul.20120216232750.10734:updateText
    #@+node:paul.20120216232750.10735:value
    @property
    def value(self): return self.getValue('value')
    #@-node:paul.20120216232750.10735:value
    #@+node:paul.20120216232750.10736:value
    @value.setter
    def value(self, v): self.setValue('value', v)


    #@-node:paul.20120216232750.10736:value
    #@-others
#@-node:paul.20120216232750.10732:class NumericText
#@+node:paul.20120216232750.10737:class StringText
class StringText(FormattedText):
    """A helper actor to display some text with text in there"""
    #@    @+others
    #@+node:paul.20120216232750.10738:__init__

    def __init__(self, tag, name, text, format='%s', colour=(255, 255, 255), font_name='DEFAULT', font_size=12, justify='center'):
        """Initialise the text"""
        super(StringText, self).__init__(tag, name, format, colour, font_name, font_size, justify, value=text)
        
    #@-node:paul.20120216232750.10738:__init__
    #@+node:paul.20120216232750.10739:updateText
    def updateText(self):
        """Update our text"""
        self.visual.setText(self.format % self.values['value'])

    #@-node:paul.20120216232750.10739:updateText
    #@+node:paul.20120216232750.10740:value
    @property
    def value(self): return self.getValue('value')
    #@-node:paul.20120216232750.10740:value
    #@+node:paul.20120216232750.10741:value
    @value.setter
    def value(self, v): self.setValue('value', v)


    #@-node:paul.20120216232750.10741:value
    #@-others
#@-node:paul.20120216232750.10737:class StringText
#@+node:paul.20120216232750.10742:class MuteButton
class MuteButton(serge.actor.Actor):
    """A button to mute sound"""
    #@    @+others
    #@+node:paul.20120216232750.10743:__init__

    def __init__(self, sprite_name, layer_name, mute_sound=True, mute_music=True, alpha=1.0):
        """Initialise the button"""
        super(MuteButton, self).__init__('mute-button', 'mute-button')
        self.mute_sound = mute_sound
        self.mute_music = mute_music
        self.setSpriteName(sprite_name)
        self.setLayerName(layer_name)
        self.visual.setAlpha(alpha)
        self.linkEvent(serge.events.E_LEFT_CLICK, self.toggleSound)
        
    #@-node:paul.20120216232750.10743:__init__
    #@+node:paul.20120216232750.10744:toggleSound
    def toggleSound(self, obj=None, arg=None):
        """Clicked on the button"""
        if self.mute_sound:
            serge.sound.Sounds.toggle()
        if self.mute_sound:
            serge.sound.Music.toggle()
        self.visual.setCell(1 if self.visual.getCell() == 0 else 0)


    #@-node:paul.20120216232750.10744:toggleSound
    #@-others
#@-node:paul.20120216232750.10742:class MuteButton
#@+node:paul.20120216232750.10745:class ToggledMenu
class ToggledMenu(serge.actor.MountableActor):
    """Implements a menu of options that can be toggled"""
    #@    @+others
    #@+node:paul.20120216232750.10746:__init__

    def __init__(self, tag, name, items, layout, default, on_colour, off_colour, 
                    width=100, height=100, callback=None, font_colour=(255, 255, 255, 255), 
                    font_name='DEFAULT', font_size=12):
        """Initialise the ToggledMenu"""
        super(ToggledMenu, self).__init__(tag, name)
        #
        # Reality check
        if not items:
            raise InvalidMenu('Menu must have at least one item in it')
        if len(set(items)) != len(items):
            raise InvalidMenu('Menu cannot have duplicates in it (%s)' % (', '.join(items)))         
        #
        # Setup the menu
        self.mountActor(layout, (0, 0))
        self.on_colour = on_colour
        self.off_colour = off_colour
        self.callback = callback
        self.layout = layout
        #
        self._setupMenu(items, width, height, font_colour, font_name, font_size)
        self.selectItem(default)

    #@-node:paul.20120216232750.10746:__init__
    #@+node:paul.20120216232750.10747:_setupMenu
    def _setupMenu(self, items, width, height, font_colour, font_name, font_size):
        """Setup all the menu items"""
        self._menu_items = {}
        self.items = items
        self._selection = None
        #
        for idx, item in enumerate(items):
            new_item = serge.actor.Actor(('%s-menuitem' % self.name), '%s-item-%s' % (self.name, idx))
            new_item.visual = serge.blocks.visualblocks.RectangleText(item, font_colour, (width, height), self.off_colour,
                font_size=font_size, font_name=font_name)
            self._menu_items[item] = new_item
            self.layout.addActor(new_item)
            new_item.linkEvent(serge.events.E_LEFT_CLICK, self._itemClick, item)
        
    #@-node:paul.20120216232750.10747:_setupMenu
    #@+node:paul.20120216232750.10748:selectItem
    def selectItem(self, name):
        """Select an item by name"""
        #
        # Don't select if already selected
        if name == self._selection:
            return
        #
        try:
            the_item = self._menu_items[name]
        except KeyError:
            raise InvalidMenuItem('Menu item "%s" not found in menu %s' % (name, self.getNiceName()))
        #
        # Highlight items
        for item in self._menu_items.values():
            item.visual.rect_visual.colour = self.on_colour if item is the_item else self.off_colour
        #
        self._selection = name
        if self.callback:
            self.callback(self, name)

    #@-node:paul.20120216232750.10748:selectItem
    #@+node:paul.20120216232750.10749:selectItemIndex
    def selectItemIndex(self, index):
        """Select an item by its index"""
        try:
            name = self.items[index]
        except IndexError:
            raise InvalidMenuItem('Index %s is outside the range of menu %s' % (index, self.getNiceName()))
        self.selectItem(name)
        
    #@-node:paul.20120216232750.10749:selectItemIndex
    #@+node:paul.20120216232750.10750:getSelection
    def getSelection(self):
        """Return the current selection"""
        return self._selection
        
    #@-node:paul.20120216232750.10750:getSelection
    #@+node:paul.20120216232750.10751:getSelectionIndex
    def getSelectionIndex(self):
        """Return the current selection index"""
        return self.items.index(self._selection)
        
    #@-node:paul.20120216232750.10751:getSelectionIndex
    #@+node:paul.20120216232750.10752:_itemClick
    def _itemClick(self, obj, name):
        """Clicked on an item"""
        self.selectItem(name)     


    #@-node:paul.20120216232750.10752:_itemClick
    #@-others
#@-node:paul.20120216232750.10745:class ToggledMenu
#@+node:paul.20120216232750.10753:class AnimateThenDieActor
class AnimateThenDieActor(serge.actor.Actor):
    """An actor that shows its animation and then is removed from the world"""
    #@    @+others
    #@+node:paul.20120216232750.10754:__init__

    def __init__(self, tag, name, sprite_name, layer_name, parent=None):
        """Initialise the AnimateThenDieActor
        
        If the parent is specified then we will be moved to the location of the parent
        
        """
        super(AnimateThenDieActor, self).__init__(tag, name)
        #
        self.parent = parent
        self.setSpriteName(sprite_name)
        self.setLayerName(layer_name)
        
    #@-node:paul.20120216232750.10754:__init__
    #@+node:paul.20120216232750.10755:addedToWorld
    def addedToWorld(self, world):
        """Added the actor to the world"""
        super(AnimateThenDieActor, self).addedToWorld(world)
        #
        if self.parent:
            self.moveTo(self.parent.x, self.parent.y)
            
    #@-node:paul.20120216232750.10755:addedToWorld
    #@+node:paul.20120216232750.10756:updateActor
    def updateActor(self, interval, world):
        """Update the actor"""
        if not self.visual.running:
            # Ok, run its course
            world.scheduleActorRemoval(self)
            
    #@-node:paul.20120216232750.10756:updateActor
    #@-others
#@-node:paul.20120216232750.10753:class AnimateThenDieActor
#@+node:paul.20120216232750.10757:class FPSDisplay
class FPSDisplay(NumericText):
    """Displays the current FPS on the screen"""
    
    #@    @+others
    #@+node:paul.20120216232750.10785:__init__
    def __init__(self, x, y, font_colour, font_size, font_name='DEFAULT'):
        """Initialise the FPS display"""
        super(FPSDisplay, self).__init__('fps', 'fps', 'FPS: %5.2f', colour=font_colour, font_size=font_size,
            value=0, font_name=font_name)
        self.setLayerName('ui')
        self.moveTo(x, y)  
        self.engine = serge.engine.CurrentEngine()
    #@nonl
    #@-node:paul.20120216232750.10785:__init__
    #@+node:paul.20120216232750.10786:updateActor
    def updateActor(self, interval, world):
        """Update the actor"""
        self.value = self.engine.getStats().average_frame_rate
    #@nonl
    #@-node:paul.20120216232750.10786:updateActor
    #@-others
#@nonl
#@-node:paul.20120216232750.10757:class FPSDisplay
#@-others
#@-node:paul.20120216232750.10711:@shadow actors.py
#@-leo
