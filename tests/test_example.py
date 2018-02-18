from .example import MyFlow

class TestExample(object):
    def test_step1_triggers(self):
        m = MyFlow()
        m.input1 = 'a_test_value'
        assert m.intermediary == 'foo'

        m.input1 = 'b_test_value'
        assert m.intermediary == 'bar'
    
    def test_step2_triggers(self):
        m = MyFlow()
        m.input1 = 'b_test_value'
        m.input2 = 'foo'
        assert m.output == 'foobar'
