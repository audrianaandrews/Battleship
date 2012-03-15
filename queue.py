class Queue(object):
    '''First in first out queue of items.'''

    def __init__(self):
        '''(Queue) -> None
        Queue object constructor.'''

        self.queue = []

    def enqueue(self, o):
        '''(Queue, Object) -> None
        Add object to Queue.'''

        self.queue.append(o)

    def dequeue(self):
        '''(Queue) -> Object
        Remove and return object at front of Queue.'''

        if self.is_empty() == True:
            raise EmptyQueueError()
        else:
            frt = self.front()
            self.queue.remove(frt)
            return frt

    def front(self):
        '''(Queue) -> Object
        Return object at front of Queue. If Queue empty raises error
        EmptyQueueError.'''

        if self.is_empty() == True:
            raise EmptyQueueError()
        else:
            return self.queue[0]

    def is_empty(self):
        '''(Queue) -> boolean
        Return if Queue is empty.'''

        return not self.queue

    def size(self):
        '''(Queue) -> int
        Return size of Queue.'''

        return len(self.queue)


class EmptyQueueError(Exception):
    '''Raised if dequeue() or front() is called on an empty queue.'''
    pass
