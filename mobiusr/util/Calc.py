# title           :Calc
# description     :TRNG
# author          :Sasha Kacanski
# date            :6/28/20
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
# ==============================================================================
import Config as cf
from collections import defaultdict as dd
import itertools, time
from tqdm import tqdm
import numpy as np
from collections import Counter


class Calculate(object):
  """

  """

  def __init__(self, trueRandomNums, pastWinningsDF):
    self.pastWinningsDF = pastWinningsDF
    self.hits = dict()
    self.trueRandomNums = trueRandomNums
    self.trueRandomNumsLenght = len(trueRandomNums)
    self.odds = list()
    self.numberList = list()
    self.frequency = list()
    self.counts = Counter(self.trueRandomNums)

  def calc(self):
    ## past winning numbers let's go through the one series at the time
    ## adn calculate frequencies of number appearing in TRNG set
    frequencyOfMatchedNumbers = list()
    pastNumbers = list()
    matchedFrequency = list()
    for idx, row in tqdm(self.pastWinningsDF.iterrows()):
      if cf.d: print("Frame row: {}\nNums:\n{}".format(idx, row))
      frequencyOfMatchedNumbers.append(self.matchIt(row.tolist()))

    for eachList in frequencyOfMatchedNumbers:
      for el in eachList:
        for k, v in el.items():
          pastNumbers.append(k)
          matchedFrequency.append(v)

    return (pastNumbers, matchedFrequency)

  def matchIt(self, listOfPastWinnings):
    listOfPastWinnings = list(map(int, listOfPastWinnings))
    appear = list()
    for num in listOfPastWinnings:
      appear.append({num: self.counts[num]})

    return appear


  def matchHistory(self, pastWinningsDF, results):
    matched = list()
    ## convert pastWinningsDF to numpy array for fast processing
    elements = pastWinningsDF.to_numpy()
    ##mask it
    elements = elements.astype(np.int)
    removeList = list()
    oResults = results.copy()
    for index, result in enumerate(results):
      matched = 0
      mask = np.isin(elements, result)
      np.amax(np.count_nonzero(mask, axis=1))
      matched = (np.amax(np.count_nonzero(mask, axis=1)))
      if matched >= 3:
        removeList.append(index)

    for index in sorted(removeList, reverse=True):
      del oResults[index]
    percent = len(oResults) / len(results)  * 100

    return (percent, oResults)
