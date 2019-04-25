# content of test_class.py
class TestClass(object):
    def test_one(self):
        x = "this"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        #assert that object 'x' does not have attribute 'check'
        assert not hasattr(x, 'check')