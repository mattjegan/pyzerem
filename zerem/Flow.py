
import inspect

from .process import process
from .Slot import Slot


class FlowMeta(type):
    """
    Provides a metaclass that populates a __flow_watchers list and a __flow_available dict with processes and slots
    """

    def __new__(cls, name, bases, dct):
        watchers = []
        available = {}

        for key, value in dct.items():
            if isinstance(value, process):
                # Get the argument names for the process by inspecting the signature
                process_args = list(param[0] for param in inspect.signature(value.func).parameters.items())

                # Register the watchers (must use tuples as a naive map since lists 
                # aren't hashable and we need to preserve order)
                watchers.append((process_args, value, ))  # TODO: Optimize this to use a tree of args since lists can't be hashed

            if isinstance(value, Slot):
                # Keep a count of how many elements are in the slots queue since we have no access to the information
                # inside a descriptor from within the class instance
                available[key] = 0

        dct['__flow_watchers'] = watchers
        dct['__flow_available'] = available
        return super(FlowMeta, cls).__new__(cls, name, bases, dct)


class Flow(object, metaclass=FlowMeta):
    """
    Provides a base class that overrides __setattr__ to check whether slots have 
    been populated enough to satisfy processes
    """

    @property
    def __flow_available(self):
        return self.__getattribute__('__flow_available')
    
    @property
    def __flow_watchers(self):
        return self.__getattribute__('__flow_watchers')

    def __setattr__(self, name, value):
        super(Flow, self).__setattr__(name, value)
        if name not in self.__flow_available:
            # If the attr is not a registered slot, just return as normal
            return

        self.__flow_available[name] += 1

        # Check if any watchers are triggered
        for watcher in self.__flow_watchers:

            # Check if we have the args needed for this process
            if self.__args_available(watcher[0]):
                
                # Call the watcher with self if needed
                if watcher[0][0] == 'self':
                    args = [self.__getattribute__(arg) for arg in watcher[0][1:]]
                    self.__update_available(watcher[0][1:])
                    watcher[1](self, *args)
                else:
                    args = [self.__getattribute__(arg) for arg in watcher[0]]
                    self.__update_available(watcher[0])
                    watcher[1](*args)

    def __update_available(self, args):
        # Args have been used so decrement our count
        for arg in args:
            self.__flow_available[arg] -= 1

    def __args_available(self, required):
        for arg in required:

            # If the arg is self, continue as it won't be a registered slot
            if arg == 'self':
                continue

            if not self.__flow_available.get(arg, False):
                return False
        return True
