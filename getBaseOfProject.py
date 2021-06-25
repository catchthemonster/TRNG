
#title           :getBaseOfProject
#description     :TRNG
#author          :Sasha Kacanski
#date            :6/20/18
#version         :0.0.1
#usage           :
#notes           :
#python_version  :3.6.3
#==============================================================================


import os
import Config as cf

class getBase(object):
    '''
    For all Resources under application root define the root of application
    '''

    def __init__(self):
        self.root = __file__

    def __str__(self):
        ##if cf.d: logger.info(os.path.dirname(self.root))
        return os.path.dirname(self.root)