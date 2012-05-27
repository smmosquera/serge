"""Some helper classes to implement various parallel processing workers"""

import multiprocessing
import pygame
import Queue

import serge.engine

def getSurfaceProcessingPipeline(target, skip_to_last=False):
    """Return a pair of queues to implement a surface processing pipeline
    
    An input and output queue are returned. The queues are passed a tuple of items
    and the first one is a surface which is marshalled to the target function.
    
    The function must also return a tuple, the first of which is assumed to be a surface
    which will be marshalled.
    
    If skip_to_last is True then when the process falls behind it will only process
    the final item in the queue
    
    """
    #
    # The pipeline function
    def pipelineProcessor(qin, qout):
        """Implements the surface processing pipeline"""
        while True:
            #
            # Get the next job
            job = qin.get()
            if job is None:
                break
            if skip_to_last:
                while True:
                    try:
                        job = qin.get(False)
                    except Queue.Empty:
                        #print 'Last job found', qin.qsize()
                        if qin.qsize() == 0:
                            break
                        else:
                            pass#print 'Hmmm, still a queue there'
                    else:
                        pass#print 'Skipped job', qin.qsize()
                        if job is None:
                            return
            surface, args = unmarshallSurface(*job[0]), job[1:]
            #
            # Process it
            results = target(surface, *args)
            if isinstance(results, tuple):
                new_surface, other = results[0], results[1:]
            else:
                new_surface, other = results, []
            #
            # Package back
            qout.put_nowait([marshallSurface(new_surface)] + other)
    #
    # Create queues
    todo = multiprocessing.Queue()
    result = multiprocessing.Queue()
    #
    # Create the worker and start it up
    worker = multiprocessing.Process(target=pipelineProcessor, args=(todo, result))
    worker.daemon = True
    worker.start()
    #
    # Make sure we go away
    def stoppingNow(obj, arg):
        """The engine is stopping"""
        todo.put(None)
    engine = serge.engine.CurrentEngine()
    if engine:
        engine.linkEvent(serge.events.E_BEFORE_STOP, stoppingNow)
    #
    return (todo, result, worker)

FORMAT = 'RGBA'
            
def marshallSurface(surface):
    """Return a surface that can be passed from one process to another"""
    return surface.get_width(), surface.get_height(), FORMAT, pygame.image.tostring(surface, FORMAT)
    
def unmarshallSurface(width, height, fmt, string):
    """Return a surface returned from another process"""
    return pygame.image.fromstring(string, (width, height), fmt)
    
    
    
