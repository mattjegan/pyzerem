
from zerem import Slot

class TestSlots(object):
    def test_init(self):
        """
        Tests that slots can be created
        """

        slot1 = Slot()
        slot2 = Slot(keep_last=True)

        assert slot1.keep_last is False
        assert slot2.keep_last is True

    def test_set(self):
        """
        Tests that assigning to a slot populates the queue
        """

        test_value = 'test_value'

        slot = Slot()
        slot.__set__(None, test_value)

        assert slot.queue[0] == test_value
    
    def test_get(self):
        """
        Tests that we can retrieve from the slot in a FIFO fashion
        """

        test_value1 = 'test_value1'
        test_value2 = 'test_value2'

        slot = Slot()
        slot.__set__(None, test_value1)
        slot.__set__(None, test_value2)

        assert slot.__get__() == test_value1
        assert slot.__get__() == test_value2

    def test_get_keep_last(self):
        """
        Tests that we can iterate through the queue rather than removing the head element
        """

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

    def test_get_is_none_if_queue_empty(self):
        slot = Slot()
        assert slot.__get__() is None
