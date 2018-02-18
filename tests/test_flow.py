
from zerem import Flow, Slot, process


class TestFlow(object):
    def test_slots_register(self):
        class MyFlow(Flow):
            slot = Slot()
        
        m = MyFlow()
        assert getattr(m, '__flow_available') == {
            'slot': 0,
        }
    
    def test_processes_register(self):
        class MyFlow(Flow):
            @process
            def step1(self):
                pass

        m = MyFlow()
        assert getattr(m, '__flow_watchers') == [
            (['self'], m.step1),
        ]

    def test_setattr_triggers_methods(self):
        class MyFlow(Flow):
            slot = Slot()
            triggered = False

            @process
            def step1(self, slot):
                self.triggered = True
        
        m = MyFlow()
        m.slot = 'test_value'
        assert m.triggered is True
    
    # TODO: Add support for staticmethods as processes
    # def test_get_setattr_triggers_staticmethods(self):
    #     triggered = False

    #     class MyFlow(Flow):
    #         slot = Slot()

    #         @process
    #         @staticmethod
    #         def step1123(slot):
    #             print('triggered')
    #             triggered = True
        
    #     m = MyFlow()
    #     m.slot = 'test_value'

    def test_setattr_does_not_trigger_when_wrong_args(self):
        class MyFlow(Flow):
            slot = Slot()
            triggered = False

            @process
            def step1(self, slot, nonexistant):
                self.triggered = True
        
        m = MyFlow()
        m.slot = 'test_value'
        assert m.triggered is False
