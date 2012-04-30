"""Implements drag and drop behaviour"""

import serge.actor
import serge.events
import serge.blocks.actors

class NotDragging(Exception): """No actor is being dragged"""
class DuplicateActor(Exception): """The actor is already controlled"""
class NotATarget(Exception): """The actor is not a target"""
class AlreadyATarget(Exception): """The actor is a target already"""


class DragController(serge.blocks.actors.ScreenActor):
    """Controls objects which are draggable"""
    
    def __init__(self, tag='controller', name='controller', start=None, stop=None, hit=None, miss=None):
        """Initialise the controller"""
        super(DragController, self).__init__(tag, name)
        self.draggables = serge.actor.ActorCollection()
        self.targets = serge.actor.ActorCollection()
        self.dragging = self._last_dragged = None
        self.drag_x = self.drag_y = 0.0
        self.setCallbacks(start, stop)
        self.setDropCallbacks(hit, miss)

    def addActor(self, actor, start=None, stop=None):
        """Add an actor to be controlled and callback to be called when dragging start and stops"""
        if actor in self.draggables:
            raise DuplicateActor('The actor %s is already controlled by %s' % (actor.getNiceName(), self.getNiceName()))
        self.draggables.append(actor)
        actor.linkEvent(serge.events.E_LEFT_MOUSE_DOWN, self.mouseDown, (actor, start))
        actor.linkEvent(serge.events.E_LEFT_CLICK, self.clickedActor, (actor, stop))

    def removeActor(self, actor):
        """Remove an actor from being controlledd"""
        self.draggables.remove(actor)
        actor.unlinkEvent(serge.events.E_LEFT_MOUSE_DOWN, self.mouseDown)
        actor.unlinkEvent(serge.events.E_LEFT_CLICK, self.clickedActor)

    def addDropTarget(self, actor, fn=None):
        """Add a target to drop to"""
        if actor in self.targets:
            raise AlreadyATarget('The target %s is already a drop target for %s' % (actor.getNiceName(), self.getNiceName()))
        else:
            self.targets.append(actor)
            actor.linkEvent(serge.events.E_LEFT_CLICK, self.droppedOn, (actor, fn))

    def removeDropTarget(self, actor):
        """Remove an actor as a drop target"""
        try:
            self.targets.remove(actor)
            actor.unlinkEvent(serge.events.E_LEFT_CLICK, self.droppedOn)
        except ValueError:
            raise NotATarget('The actor %s was not a target in %s' % (actor.getNiceName(), self.getNiceName()))

    def isDragging(self):
        """Return True if we are dragging an object"""
        return self.dragging != None

    def getDraggedActor(self):
        """Return the actor being dragged"""
        if self.isDragging():
            return self.dragging
        else:
            raise NotDragging('No actor is being dragged')        
                
    def mouseDown(self, obj, (actor, fn)):
        """The mouse was down over an actor"""
        if self.active and not self.dragging:
            self.dragging = self._last_dragged = actor
            self.drag_x, self.drag_y = self.mouse.getScreenPos()
            if fn:
                fn(obj, actor)
            if self._start:
                self._start(obj, actor)
            
    def clickedActor(self, obj, (actor, fn)):
        """The mouse was released over an actor"""
        if self.active and self.dragging:
            self.dragging = None
            if fn:
                fn(obj, actor)
            if self._stop:
                self._stop(obj, actor)
            self.checkForMiss(actor)
            
    def checkForMiss(self, actor):
        """Check to see if we dropped our actor and missed all the targets - if so call the miss callback"""
        #
        # Only makes sense to do this if we are going to call a callback
        if not self._miss:
            return
        #
        # This doesn't feel like the implementation is really correct here but it
        # works for the moment
        test = serge.geometry.Point(*self.mouse.getScreenPos())
        for target in self.targets:
            if actor != target and test.isInside(target):
                # Ok, overlaps at least one target
                return
        #
        # No targets were overlapped - so call the miss callback
        self._miss(actor)
        
        
    def updateActor(self, interval, world):
        """Update the controller"""
        super(DragController, self).updateActor(interval, world)
        #
        if self.active and self.dragging:
            mx, my = self.mouse.getScreenPos()
            self.dragging.move(mx-self.drag_x, my-self.drag_y)
            self.drag_x, self.drag_y = self.mouse.getScreenPos()
            
    def setCallbacks(self, start, stop):
        """Set the callbacks to use when starting and stopping a drag"""
        self._start = start
        self._stop = stop           
    
    def setDropCallbacks(self, hit, miss):
        """Set the callback to use when dropping on a target"""
        self._hit = hit
        self._miss = miss

    def droppedOn(self, obj, (actor, fn)):
        """An actor was dropped on a target"""
        if actor != self._last_dragged:
            if fn:
                fn(actor, self._last_dragged)
            if self._hit:
                self._hit(actor, self._last_dragged)
                
