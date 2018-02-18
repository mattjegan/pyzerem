
from zerem import process


class TestProcess(object):
    def test_process_stores_method(self):

        def foo():
            pass
        
        p = process(foo)
        assert p.func == foo
    
    def test_process_calls_method(self):

        def foo():
            return 'test_value'
        
        p = process(foo)
        assert p() == 'test_value'
        