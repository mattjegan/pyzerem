
from zerem import Slot

class TestSlots(object):
    def test_init(self):
        slot1 = Slot()
        slot2 = Slot(keep_last=True)

        assert slot1.keep_last is False
        assert slot2.keep_last is True

    def test_set(self):
        test_value = 'test_value'

        slot = Slot()
        slot.__set__(None, test_value)

        assert slot.queue[0] == test_value
    
    def test_get(self):
        test_value1 = 'test_value1'
        test_value2 = 'test_value2'

        slot = Slot()
        slot.__set__(None, test_value1)
        slot.__set__(None, test_value2)

        assert slot.__get__() == test_value1
        assert slot.__get__() == test_value2

    def test_get_keep_last(self):
        test_value1 = 'test_value1'
        test_value2 = 'test_value2'
        unchanged = [test_value1, test_value2]

        slot = Slot(keep_last=True)
        slot.__set__(None, test_value1)
        slot.__set__(None, test_value2)

        assert slot.current == 0
        assert slot.__get__() == test_value1
        assert slot.queue == unchanged
        assert slot.current == 1
        assert slot.__get__() == test_value2
        assert slot.queue == unchanged
        assert slot.current == 2
