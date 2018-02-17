
class Slot(object):
    def __init__(self, keep_last=False):
        self.keep_last = keep_last
        self.current = 0
        self.queue = []

    def __get__(self, *args):
        if self.queue:
            if not self.keep_last:
                val = self.queue[0]
                del self.queue[0]
                return val
            self.current += 1
            return self.queue[self.current - 1]
        
        return None
    
    def __set__(self, instance, value):
        self.queue.append(value)
