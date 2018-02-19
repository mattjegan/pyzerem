
from zerem import process


class TestProcess(object):
    def test_process_stores_method(self):
        """
        Tests that process stores the function internally.
        """

        def foo():
            pass
        
        p = process(foo)
        assert p.func == foo
    
    def test_process_calls_method(self):
        """
        Tests that the process outputs the same as the function it stores.
        """

        def foo():
            return 'test_value'
        
        p = process(foo)
        assert p() == foo()
        