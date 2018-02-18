from zerem import *

# Classes deriving from zerem.Flow are special
class MyFlow(Flow):

    # A Flow class can have slots
    input1 = Slot()
    input2 = Slot()
    intermediary = Slot()
    output = Slot()

    # Functions marked as processes are invoked automatically
    # when their inputs become available. 
    # Inputs to processes are identified by arguments with 
    # the names of slots. 

    @process
    def step1(self, input1):
        # Besides invocation, this is a regular function. the
        # argument it receives is any python object. Let's assume
        # it is a string
        x = input1.lower()
        if x.startswith('a'):
            y = 'foo'
        else:
            y = 'bar'

        # Processes don't return values; they can push values into
        # slots, though. Assignment to a slot pushes a value into it.
        self.intermediary = y

    @process
    def step2(self, input2, intermediary):
        # This will be called automatically when both input2 and 
        # intermediary are available (intermediary will become
        # available after step1 above completes)
        self.output = input2 + intermediary
