# title           :Main
# description     :TRNG
# author          :Sasha Kacanski
# date            :6/18/18
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
# ==============================================================================

import  sys, os, time
from NMetaIO import PandasReader
from Dill import MSGpack
import Config as cf
import pandas as pd
from five import Five
from Trng import FTRNG as trg
from types import SimpleNamespace
from Calc import Calculate as cc
import random, pickle

def processPastWinnings(fn, columns):
  pandasStdReader = PandasReader(fn, ' ')
  pandasStdReader.load(colNames=columns)
  df = pandasStdReader.getPayLoad()
  shape = df.shape
  print("Processing collection of {} past winning numbers".format(shape[0]))
  return df


def writeResults(win, allWinningNums, idx):
  ## print results
  # print("------------------------------------------------------------------------")
  # print("All wining numbers {} are:\n".format(len(win)))
  # for result in win:
  #   print(result)
  # print("------------------------------------------------------------------------")

  fName = ''.join([allWinningNums, str(idx)])
  with open(fName, 'wb') as fp:
    pickle.dump(win,fp)


def main():
  print("""
This little app could take a long time to crunch winning numbers depending on how you set it up!
I mean it a long time and it might need resources like cores and memory as we go...
So best option is to play with configuration parameters until you think you are happy...

  """)

  ## to see debug messages enable d flag
  cf.d = False

  ## to pull more random true numbers enable gRandom and chage qRanom params to higvher values
  getRandom = True

  ## complex number cruncher
  fn = "/home/sasha/Development/PYEXP/TRNG/conf/cash5"
  trngStore = "/core/apps/Dill/TRNG/trng"
  pastNumbersStore  = "/core/apps/Dill/Numbers"
  freqStore = "/core/apps/Dill/Freq"
  allWinningNums = "/core/apps/Dill/AWN/awn"

  upperLimit = 46 ## what is upper limit on numbers

  ## in one batch how many numbers we get from TRNG source
  qRandom = SimpleNamespace()
  qRandom.howMuchtoGrab = 1024
  qRandom.howManyTimes = 100 ## 16 loops is pretty good estimate
  qRandom.timeOut = 2
  qRandom.trngStore = trngStore
  qRandom.upperLimit = upperLimit
  qRandom.getRandom = getRandom

  ##some exotic configs
  winThreshold = 500 ##higher float takes more cycles and if too high will never happen


  ## load numbers to pandas
  ## shape is number of rows + each number is column

  colNames = ['1', '2', '3', '4', '5']
  df = processPastWinnings(fn, colNames)

  ##if getRandom:
  ## get true random ints
  trng = trg(qRandom)
  trngNums = trng.getRN()

  ## calculate a hit rate
  calc = cc(trngNums, df)
  pastNumbers,matchedFrequency = calc.calc()
  # hits = calc.getHits()
  # if cf.d: print(hits)

  ## cache pastNumbers,matchedFrequency
  store = MSGpack(freqStore)
  store.pack(matchedFrequency)
  pnStore = MSGpack(pastNumbersStore)
  pnStore.pack(pastNumbers)
  ##calc.prepOdds(frequencyOfMatchedNumbers)
  ##calc.prepNewOdds()
  ##numbers, frequency = calc.getOdds()
  # nStore = MSGpack(numberStore)
  # fStore = MSGpack(freqStore)
  # nStore.pack(numbers)
  # fStore.pack(frequency)
  ##else:
  tStore = MSGpack(trngStore)
  pnStore = MSGpack(pastNumbersStore)
  fStore = MSGpack(freqStore)
  trngNums = tStore.unpack()
  pastNumbers = pnStore.unpack()
  matchedFrequency = fStore.unpack()
  trgnLenght = len(trngNums)
  calc = cc(trngNums, df)

  mbr = [x for x in range(5000,10000,10)]
  split = 5
  noise = [x/10.0 for x in range(0,11)]
  mm = 0
  nn = 0

  pastPercents = list()
  fResult = [0]
  counter = 0
  while len(fResult) < winThreshold:
    # ##run ML
    ## predict a sequence of numbers that will represnt number of loops to take to predict new number
    ##
    ##very important constants

    print("Starting mbr {} split {} and noise {}".format(mbr[mm], split, noise[nn]))
    ##print("Starting mbr {} split {} and noise {}".format(mbr, split, noise))

    fiveConf = SimpleNamespace()
    fiveConf.mbr = mbr[mm]  ## number of sequences that needs to be found before predicitng value higher is longer
    fiveConf.noise = noise[nn]  ## noise ration is 0 - 1 which elements in seq should not be taken into account
    fiveConf.split = split  ## num of el in seq to be stored in model

    five = Five(fiveConf, trngNums, pastNumbers, matchedFrequency)
    predictSequenceLoopsForNumbers = five.calcProbabilities()
    time.sleep(60)
    loopFreq = five.calcNewLoopFrequencies(predictSequenceLoopsForNumbers, upperLimit)
    results = five.getNew(loopFreq, upperLimit)


    ##find any matches against history with new set of numbers
    percent, fResult = calc.matchHistory(df, results)
    pastPercents.append(percent)
    print("We preformed matching on {} sequences of 5 numbers against {} random sequences!"
          "with {} sequences that matched 4 or more numbers.".format(df.size, len(results), len(fResult)))
    print("Your success rate is going to be: {}%".format(percent))
    writeResults(results, allWinningNums, counter)


    if len(pastPercents) == 1:
      latest = pastPercents[-1]
    else:
      latest = pastPercents[-2]
    if  latest > percent:
      if nn == 9:
        nn = 0
      else:
        nn += 1
      if mm >= 499:
        mm = 0
      else:
        mm += 1
    else:
      if mm >= 499:
        mm = 0
      else:
        mm += 1


    print("changing mbr to {} split to {} and noise to {}".format(mbr[mm], split, noise[nn]))
    print("------------------------------------------------------------------------")
    counter += 1



if __name__ == "__main__":
  main()
  sys.exit(0)
