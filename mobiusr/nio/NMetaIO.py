##---------------------------------------------
## PROJECT: MLM   FILE NAME: NMetaIO
## USER: sasha              PRODUCT: PyCharm
##---------------------------------------------
## 12/20/16:10:23 AM
##---------------------------------------------

import csv
import numpy

class RegisterLeafClasses(type):
    """
	Meta class for registration of all classes in this module
	"""
    ## body  of the class is executed as a set of statments with its own namespace (python dictionary)
    ## instantiating the type metaclass passing in the class name, base classes and dictionary as arguments nmspc in this case
    def __init__(cls, name, bases, nmspc):
        ## Return a proxy object that delegates method calls to a parent or sibling class of type
        super(RegisterLeafClasses, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = set()
        cls.registry.add(cls)
        ## Remove base classes
        cls.registry -= set(bases)

    ## Metamethods, called on class objects
    def __iter__(cls):
        return iter(cls.registry)
    def __str__(cls):
        if cls in cls.registry:
            return cls.__name__
        return cls.__name__ + ": " + ", ".join([sc.__name__ for sc in cls])



class MLReader(metaclass=RegisterLeafClasses):
    def __init__(self):
	    self.data = None

    def getPayLoad(self):
	    return self.data



## Register all interfaces
class PslReader(MLReader):
	"""
	Plain Python standara library CSV reader
	"""
	def __init__(self, fn, delim, quote=None):
		print("Workign with standard Python library reader...")
		self.fn = fn
		self.delim = delim
		if quote:
			self.quote = quote
		else:
			self.quote = csv.QUOTE_NONE
		self.reader = None
		self.data = None

	def load(self):
		## load explicitly to reader object
		rawPayload = open(self.fn, 'r')
		self.reader = csv.reader(rawPayload, delimiter=self.delim, quoting=self.quote)

	def loadToNumpy(self, type = 'float'):
		## load implicitly to numpy via type
		print("Loading data to numpy array as type {}".format(type))
		self.data = numpy.array(list(self.reader)).astype(type)

	def showShape(self):
		print("Data shape is: {}".format(self.data.shape))

class NumpyReader(MLReader):
	"""
	Numpy library loadtxt reader
	"""
	def __init__(self, fn, delim):
		print("Workign with Numpy library reader standard...")
		self.fn = fn
		self.delim = delim
		self.data = None

	def load(self, type = float):
		from numpy import loadtxt
		rawPayload = open(self.fn, 'rb')
		self.data = loadtxt(rawPayload, dtype = type, delimiter = self.delim)

	def showShape(self):
		print("Data shape is: {}".format(self.data.shape))


class NumpyReaderFileNode(NumpyReader):
	"""
	Numpy library loadtxt reader
	"""
	pass




class NumpyReaderURL(NumpyReader):
	"""
	Numpy URL loadtxt reader
	"""
	def __init__(self, url, delim):
		print("Workign with Numpy library reader URL...")
		self.url = url
		self.delim = delim
		self.data = None

	def load(self, type = float):
		import urllib
		from numpy import loadtxt
		rawPayload = urllib.request.urlopen(self.url)
		self.data = loadtxt(rawPayload, dtype=type, delimiter=self.delim)

class PandasReader(MLReader):
	def __init__(self, fnOrUrl, delim):
		print("Workign with Pandas library reader standard...")

		## in pandas world url or inode will work the same from prospective of parser
		self.fn = fnOrUrl
		self.delim = delim
		self.data = None


	def load(self, type=float, colNames = None):
		from pandas import read_csv
		if colNames:
			##dtype={'Persid'='str'}, engine='c'
			self.data = read_csv(self.fn, dtype=object, delimiter=self.delim, names = colNames, engine='c')
		else:
			self.data = read_csv(self.fn, dtype=type, delimiter=self.delim)

	def showShape(self):
		print("Data shape is: {}".format(self.data.shape))




def main():
    print (MLReader)
    fn = "/core/apps/MLM/data/pima-indians-diabetes.data.csv"
    url = 'some/url'
    stdReader = PslReader(fn, '\t')
    stdReader.load()
    stdReader.loadToNumpy()
    stdReader.showShape()


    numpyStdReader = NumpyReaderFileNode(fn, ',')
    numpyStdReader.load()
    numpyStdReader.showShape()

    ##numpyUrlReader = NumpyReaderURL(url, ',')
    ##numpyUrlReader.load()
    ##numpyUrlReader.showShape()

    pandasStdReader = PandasReader(fn, ',')
    ## without columns
    pandasStdReader.load()
    pandasStdReader.showShape()

    ## with column names
    colNames = ['preg','plas','pres','skin','test','mass','pedi','age','class']

    pandasStdReader.load(colNames=colNames)
    pandasStdReader.showShape()



if __name__ == '__main__':
	main()