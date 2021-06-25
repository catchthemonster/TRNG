##---------------------------------------------
## PROJECT: Dutil   FILE NAME: Dill
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 5/19/17:10:15 AM
##---------------------------------------------

import dill
from functools import update_wrapper, partial
import functools
import os

# class MSGWrapper(object):
# 	def __init__(self, func):
# 		update_wrapper(self, func)
# 		self.func = func
#
# 	def __get__(self, obj, objtype):
# 		"""Support instance methods."""
# 		return functools.partial(self.__call__, obj)
#
# 	def __call__(self, obj, *args, **kwargs):
# 		for k,v in kwargs.items():
# 			if k == 'action':
# 				return self.func(obj)


class PropException(object):
	pass


class MSGpack(object):
	"""
	We want to be able to ship Python object to different type of infrastructure -
	heterogeneous programming - byte streams
	"""


	def __init__(self, store, action=None):
		##print("License {}".format(dill.license()))
		a = os.path.dirname(store)
		if not os.path.exists(a):
			try:
				os.mkdir(a)
			except Exception as osErr:
				raise PropException(osErr)

		self.store = store

	def pack(self, obj):
		"Pack it to bytes as object store it to store"
		saved = False
		try:
			with open (self.store, 'wb') as _f:
				dill.dump(obj, _f)
				saved = True
		except dill.PicklingError as pErr:
			print("Error occurred: {}".format(pErr))

		return saved


	def unpack(self):
		"Unpack it to dill object and get back original object from packed dill store"

		try:
			with open (self.store, 'rb') as _f:
				obj = dill.load(_f)
				return obj
		except dill.PicklingError as pErr:
			print("Error occurred: {}".format(pErr))
			return None

	def compress(self, objList):
		"Pack the list of objects to bytes as object store it to store"
		saved = False
		compress = list()
		try:
			with open(self.store, 'wb') as _ff:
				for el in objList:
					with open (el, 'rb') as _f:
						obj = dill.load(_f)
						compress.extend(obj)

				dill.dump(compress, _ff)
				saved = True
		except dill.PicklingError as pErr:
			print("Error occurred: {}".format(pErr))

		return saved

