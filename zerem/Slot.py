

class Slot(object):
    def __init__(self, keep_last=False):
        """
        Stores a queue, a pointer to the current cursor, and whether
        or not we want to keep all elements after they have been consumed
        """

        self.keep_last = keep_last
        self.current = 0
        self.queue = []

    def __get__(self, *args):
        """
        If the queue is populated:
            - if we want to keep the elements move the cursor along and return the previous value
            - else pop and return the head of the queue
        otherwise return None as a default value
        """

        if self.queue:
            if not self.keep_last:
                val = self.queue[0]
                del self.queue[0]
                return val
            self.current += 1
            return self.queue[self.current - 1]
        
        return None
    
    def __set__(self, instance, value):
        """
        Simply appends the queue
        """

        self.queue.append(value)
