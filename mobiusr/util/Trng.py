# title           :Trng
# description     :TRNG
# author          :Sasha Kacanski
# date            :6/27/20
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
# ==============================================================================

import Config as cf
from Dill import MSGpack
import quantumrandom, time, os, sys, random, csv
import os.path as path
from os import walk

class PropException(object):
  pass


class FTRNG(object):
  """
  do TRNG
  """

  def __init__(self, qRandom):
    self.limit = qRandom.upperLimit
    self.run = qRandom.getRandom
    self.store = qRandom.trngStore
    self.howMuch = qRandom.howMuchtoGrab
    self.repeat = qRandom.howManyTimes
    self.sleep = qRandom.timeOut
    self.trngNums = None
    self.generator = quantumrandom.cached_generator()

  def setupStore(self, store):
    store = MSGpack(store)
    return store

  def setQuantumBanch(self):
    l = list()
    for x in range(self.repeat):
      if cf.d: print("loop now {}".format(x))
      for xx in range(self.howMuch):
        try:
          l.append(round(quantumrandom.randint(1, self.limit, generator=self.generator)))
          ##time.sleep(self.sleep)
        except Exception as cErr:
          raise PropException.cErr

    if cf.d: print("Payload of size {} received".format(len(l)))
    return l

  def getRN(self):
    ## use limit to source random numbers
    ## timeout for xx sec every time you go and fetch
    xx = 0
    dillList = list()

    if self.run:
      ## if the TRNG store has some TRNG dils we will find where we are
      trngs = []
      base = os.path.split(self.store)[0]
      for (dirpath, dirnames, filenames) in walk(base):
        for ff in filenames:
          trngs.append(os.path.join(dirpath, ff))
        break
      ## change xx if directory has some payload
      xx = len(trngs)

      while xx < self.repeat:
        tmpDill = None
        storeTag = '-'.join([self.store, str(xx)])
        store = self.setupStore(storeTag)
        mSet = self.setQuantumBanch()
        print("Obtained random set of {} numbers".format(len(mSet)))
        store.pack(mSet)
        xx += 1

      base = os.path.split(self.store)[0]
      for (dirpath, dirnames, filenames) in walk(base):
        for ff in filenames:
          trngs.append(os.path.join(dirpath, ff))
        break

      mStore = self.setupStore(self.store)
      if not os.path.exists(self.store):
        mStore.compress(trngs)
      else:
        mStore = self.setupStore(self.store)
      self.trngNums = mStore.unpack()
    # else:  ## we already have a collection let's use  it
    #   if path.exists(self.store):
    #     mStore = self.setupStore(self.store)
    #     self.trngNums = mStore.unpack()
    #   else:
    #     print("Turn on gRandom flag to True to collect random numbers")
    #     print("There is no stores available ... Bailing out ...")
    #     sys.exit(1)
    # print("we collected {} TRNG numbers".format(len(self.trngNums)))

    return self.trngNums
