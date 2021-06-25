
# title           :testMSGpack
# description     :TRNG
# author          :Sasha Kacanski
# date            :1/13/20
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
from unittest import TestCase
from Dill import MSGpack

# ==============================================================================
class Foo(object):
	def bar(self, x):
		return x + self.y

	y = 1



class TestMSGpack(TestCase):
  def setUp(self):
    self.f = Foo()
    self.d = MSGpack('/core/test')
    self.assertIsInstance(self.d,  object)


  def test_pack(self):
    doIt = self.d.pack(self.f)
    self.assertIs(doIt, True)


  def test_unpack(self):
    newObj = self.d.unpack()
    self.assertIsInstance(newObj, object)
    self.assertIs(newObj.y,1)
