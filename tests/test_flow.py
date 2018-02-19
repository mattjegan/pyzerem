
from zerem import Flow, Slot, process


class TestFlow(object):
    def test_slots_register(self):
        """
        Tests that slot is added to the flows available slots
        """

        class MyFlow(Flow):
            slot = Slot()
        
        m = MyFlow()
        assert getattr(m, '__flow_available') == {
            'slot': 0,
        }
    
    def test_processes_register(self):
        """
        Test that the process is added to the flows processes/watchers
        """

        class MyFlow(Flow):
            @process
            def step1(self):
                pass

        m = MyFlow()
        assert getattr(m, '__flow_watchers') == [
            (['self'], m.step1),
        ]

    def test_setattr_triggers_methods(self):
        """
        Tests that setting a slot triggers appropriate processes
        """

        class MyFlow(Flow):
            slot = Slot()
            triggered = False

            @process
            def step1(self, slot):
                self.triggered = True
        
        m = MyFlow()
        m.slot = 'test_value'
        assert m.triggered is True

    def test_setattr_does_not_trigger_when_wrong_args(self):
        """
        Tests that setting a slot does not trigger processes it shouldn't
        """

        class MyFlow(Flow):
            slot = Slot()
            triggered = False

            @process
            def step1(self, slot, nonexistant):
                self.triggered = True
        
        m = MyFlow()
        m.slot = 'test_value'
        assert m.triggered is False
