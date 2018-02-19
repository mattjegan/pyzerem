

class process(object):
    """
    Basic decorator that only stores the function it wraps
    """

    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
