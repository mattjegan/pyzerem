
import inspect

from .process import process


class FlowMeta(type):
    def __init__(cls, name, bases, dct):
        # print('-----------------------------------')
        # print("Initializing class", name)
        # print(cls)
        # print(bases)
        # print(dct)
        watchers = []
        available = {}

        for key, value in dct.items():
            if isinstance(value, process):
                process_args = list(param[0] for param in inspect.signature(value.func).parameters.items())
                
                for arg in process_args:
                    available[arg] = False

                # Register the watchers
                watchers.append((process_args, value, ))  # TODO: Optimize this to use a tree of args since lists can't be hashed
        
        dct['__flow_watchers'] = watchers
        dct['__flow_available'] = available
        #print(watchers)
        super(FlowMeta, cls).__init__(name, bases, dct)


class Flow(object, metaclass=FlowMeta):
    def __setattr__(self, name, value):
        print(f'Setting {name} to {value}')
        super(Flow, self).__setattr__(name, value)

        self.__flow_available[name] = True

        # Check if any watchers are triggered
        for watcher in self.__flow_watchers:
            if self.__args_available(watcher[0]):
                watcher[1](*(self.__getattribute__(arg) for arg in watcher[0]))

    def __args_available(required):
        for arg in required:
            if not self.__args_available[arg]:
                return False
        return True
