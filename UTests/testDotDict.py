
#title           :testDotDict
#description     :TRNG
#author          :Sasha Kacanski
#date            :3/10/20
#version         :0.0.1
#usage           :
#notes           :
#python_version  :3.6.3
#==============================================================================

import ast

class dotdict(dict):
  __getattr__ = dict.get
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__


c = 'a'

d =  "{'a-z':1,'b':2}"

d = ast.literal_eval(d)
d = dotdict(d)
##print(d.'{}'.format('a-z'))