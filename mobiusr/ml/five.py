# title           :five
# description     :TRNG
# author          :Sasha Kacanski
# date            :6/22/20
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
# ==============================================================================
import random
import Config as cf
from cpt.cpt import Cpt
import pandas as pd
from numpy import genfromtxt
import numpy as np
from tqdm import tqdm

class Five(object):
  """

  """

  def __init__(self, conf, trngNums, pastNumbers, matchedFrequency):
    self.conf = conf
    npTrngNums = np.array_split(np.array(trngNums), len(trngNums)/5)
    npPastNumbers = np.array_split(np.array(pastNumbers), len(pastNumbers)/5)
    npFreq = np.array_split(np.array(matchedFrequency), len(matchedFrequency)/5)
    self.trgnLenght = len(trngNums)
    print("Running collection of {} random numbers".format(self.trgnLenght))
    self.trngNums = self.traverseListOfArrays(npTrngNums)
    self.pastNumbers = self.traverseListOfArrays(npPastNumbers)
    self.frequency = self.traverseListOfArrays(npFreq)

  def traverseListOfArrays(self, aList):
    listOfLists = list()
    for el in aList:
      listOfLists.append(el.tolist())
    return listOfLists


  def calcProbabilities(self):
    model = Cpt(self.conf.split, self.conf.noise, self.conf.mbr)
    model.fit(self.trngNums)
    predictions = model.predict(self.pastNumbers) #,
    ##, self.frequency
    return predictions

  def rangeIt(self, el, ul):
    ##random.seed(el)
    for _ in range(el):
      ##zz = random.randrange(1, ul)
      zz = np.random.randint(1, ul)
    return zz

  def pick(self, freqEl, ul):
    newSet = list()
    for el in freqEl:
      zz = self.rangeIt(el, ul)
      while zz in newSet:
        zz = self.rangeIt(el, ul)
      newSet.append(zz)
    return newSet

  def getNew(self, freq, ul):
    nListOfSets = list()
    for _ in tqdm(range(len(freq))):
      nListOfSets.append(sorted(self.pick(freq[_], ul)))
    return nListOfSets

  def calcNewLoopFrequencies(self, nums, ul):
    return list(zip(*(iter(nums),) * 5))





