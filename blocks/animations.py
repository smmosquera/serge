"""Classes to help animating actors"""


import fnmatch

import serge.actor
import serge.blocks.effects


class AnimationExists(Exception):
    """An animation already exists with the same name"""


class AnimationNotFound(Exception):
    """The animation was not found"""


class NotPaused(Exception):
    """Tried to start when an animation was not paused"""


class AlreadyPaused(Exception):
    """Tried to pause when an animation was already paused"""


class AnimatedActor(serge.actor.Actor):
    """Implements an actor that can have animations applying to it"""

    def __init__(self, tag, name):
        """Initialise the actor"""
        super(AnimatedActor, self).__init__(tag, name)
        #
        self.animations = {}
        self._paused = False

    def addAnimation(self, animation, name):
        """Add an animation to this actor"""
        if name in self.animations:
            raise AnimationExists('An animation named "%s" already exists for this actor (%s)' % (
                name, self.getNiceName()
            ))
        self.animations[name] = animation
        animation.setActor(self)
        animation.setName(name)
        return animation

    def removeAnimation(self, name):
        """Remove a named animation"""
        try:
            del(self.animations[name])
        except KeyError:
            raise AnimationNotFound('No animation called "%s" found for actor %s' % (
                name, self.getNiceName()
            ))

    def removeAnimations(self):
        """Remove all the animations"""
        self.animations.clear()

    def removeAnimationsMatching(self, pattern):
        """Remove all animations matching a matching pattern"""
        for name in self.animations.keys():
            if fnmatch.fnmatch(name, pattern):
                self.removeAnimation(name)

    def getAnimation(self, name):
        """Return the named animation"""
        try:
            return self.animations[name]
        except KeyError:
            raise AnimationNotFound('No animation called "%s" found for actor %s' % (
                name, self.getNiceName()
            ))

    def getAnimations(self):
        """Return all the animations"""
        return self.animations.values()

    def pauseAnimations(self, safe=False):
        """Pause all animations"""
        if not safe and self._paused:
            raise AlreadyPaused('Animations for %s are already paused' % self.getNiceName())
        self._paused = True

    def unpauseAnimations(self, safe=False):
        """Start all animations"""
        if not safe and not self._paused:
            raise NotPaused('Animations for %s are not paused' % self.getNiceName())
        self._paused = False

    def animationsPaused(self):
        """Return True if our animations are paused"""
        return self._paused

    def restartAnimations(self):
        """Restart all animations"""
        self._paused = False
        for animation in self.getAnimations():
            animation.restart()

    def completeAnimations(self):
        """Complete all animations"""
        self._paused = True
        for animation in self.getAnimations():
            animation.finish()
            animation.update()

    def updateActor(self, interval, world):
        """Update the actor"""
        super(AnimatedActor, self).updateActor(interval, world)
        #
        if not self._paused:
            for animation in self.animations.values():
                if not animation.paused:
                    animation.updateActor(interval, world)


class Animation(serge.blocks.effects.Effect):
    """The basic animation class"""

    def __init__(self, duration=1000, done=None, loop=False):
        """Initialise the animation"""
        super(Animation, self).__init__(done=done, persistent=True)
        #
        self.actor = None
        self.name = None
        self.duration = duration
        self.loop = loop
        self._initProperties()

    def setActor(self, actor):
        """Set our actor"""
        self.actor = actor

    def setName(self, name):
        """Set our name"""
        self.name = name

    def _initProperties(self):
        """Initialise the properties"""
        self.start = 0
        self.end = self.duration
        self.current = 0
        self.iteration = 0
        self.fraction = 0.0
        self.complete = False
        self.direction = 1

    def restart(self):
        """Restart the animation"""
        self._initProperties()
        self.update()

    def updateActor(self, interval, world):
        """Update the animation effect"""
        super(Animation, self).updateActor(interval, world)
        #
        self.current += self.direction * interval
        self.iteration += 1
        #
        # Watch for bouncing
        if self.loop:
            if self.direction == 1 and self.current > self.end:
                self.current = self.duration - (self.current - self.duration)
                self.direction *= -1
            elif self.direction == -1 and self.current < 0:
                self.current = -self.current
                self.direction *= -1
        #
        # Map back into proper space
        # TODO: a proper implementation should also account for going through more than one iteration
        self.current = min(self.duration, max(0, self.current))
        self.fraction = min(1.0, float(self.current) / self.duration)
        #
        self.update()
        #
        if self.fraction == 1.0:
            self.finish()

    def finish(self):
        """Finish the effect"""
        self.current = self.end
        self.fraction = 1.0
        self._effectComplete(None)
        self.complete = True

    def update(self):
        """The main method implementing the animation effect

        This is the method you should implement

        """

#
# Now we have some specific examples of useful animations


class ColourCycle(Animation):
    """Animate the colour property of an object between a beginning and end"""

    def __init__(self, obj, start_colour, end_colour, duration,
                 attribute='colour', loop=False, done=None):
        """Initialise the animation"""
        super(ColourCycle, self).__init__(duration, loop=loop, done=done)
        #
        self.obj = obj
        self.start_colour = start_colour
        self.end_colour = end_colour
        self.attribute = attribute

    def update(self):
        """Update the colour of the object"""
        #
        # Work out the values for each element of the colour
        colours = []
        for x, y in zip(self.start_colour, self.end_colour):
            colours.append(float(x + (y - x) * self.fraction))
        #
        self.setColour(tuple(colours))

    def setColour(self, colour):
        """Set the colour"""
        setattr(self.obj, self.attribute, colour)


class ColourText(ColourCycle):
    """Animate the colour of a text object by calling its setColour method"""

    def setColour(self, colour):
        """Set the colour"""
        self.obj.setColour(colour)
        if len(colour) == 4:
            self.obj.setAlpha(float(colour[-1]) / 255)
