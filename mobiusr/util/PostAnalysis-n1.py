
#title           :PostAnalysis
#description     :TRNG
#author          :Sasha Kacanski
#date            :7/27/20
#version         :0.0.1
#usage           :
#notes           :
#python_version  :3.6.3
#==============================================================================

import pickle, sys
from itertools import tee
import random
import glob, os, copy
import operator
from cpt.cpt import Cpt
from types import SimpleNamespace
from statistics import mode

def partition(lst, n):
    division = len(lst) / n
    return [lst[round(division * i):round(division * (i + 1))] for i in range(n)]

def predict( origins, silos):
  predictSilo = list()
  mbrL = [x for x in range(5000, 10000, 10)]
  split = 2
  noiseL = [x / 10.0 for x in range(0, 11)]
  mm = 0
  nn = 0
  silos = partition(silos, 250)
  ii = 0
  while ii < 500:
    mbr = mbrL[mm]
    noise = noiseL[nn]
    split = split
    print("Running with {} {} {}".format(split, noise, mbr))
    model = Cpt(split, noise, mbr)
    model.fit(silos)
    silo = model.predict(origins)
    print("Use numbers from {} set!".format(silo))
    predictSilo.append(silo)
    del model
    if nn == 9:
      nn = 0
    else:
      nn += 1
    if mm >= 499:
      mm = 0
    else:
      mm += 1
    ii += 1

  return predictSilo


def analize(whatNum, wins):
  d =  dict()
  for el in wins:
    d.update(el)

  itemMaxValue = max(d.items(), key=lambda x: x[1])
  print("\nWining combination '{}' numers:".format(whatNum))
  if itemMaxValue[1] != 0:
    print("Hit obtained: {} times on {} our random winning sample".format(itemMaxValue[1], itemMaxValue[0]))
  return (itemMaxValue[1], itemMaxValue[0])

def match(fResults, win, whatMatch ):
  cnt = 0
  results = list()
  fList = list()
  mainIndex = 0
  for cnt, res in enumerate(fResults):
    gotIt = False
    mainIndex += 1
    match = set(res).intersection(win)
    if len(match) == whatMatch:
      index = cnt
      cnt += 1
      gotIt = True
    elif len(match) == whatMatch:
      index = cnt
      cnt += 1
      gotIt = True
    elif len(match) == whatMatch:
      index = cnt
      cnt += 1
      gotIt = True
    if gotIt:
      results.append((index, match, res))
      dcResults = copy.deepcopy(results)
      results = list()
      fList.append(dcResults)

  return(fList)


def pairwise(iterable):
  a, b = tee(iterable)
  next(b, None)
  return zip(a, b)

def main():
  wins = [[3, 8, 11, 25, 39]]
  ##,[8, 9, 25, 32, 43]]

  pay3 = {3: 11}
  pay4 = {4:327}
  pay5 = {5:182000}


  ## figure out how many files you have in directory
  allCurrentFiles = list()
  os.chdir("/core/apps/Dill")
  allSilos = glob.glob("awn*")
  latestSilo = 'awn' + str(len(allSilos)-1)
  if latestSilo not in allSilos:
    print('missed it!')
  else:
    print("found latest...")

  print("-------------------------------------------------------------------")
  print("-------------------------------------------------------------------")
  print("-------------------------------------------------------------------")
  indexThree = list()
  indexFour = list()
  indexFive = list()

  mainIndex = dict()
  for win in wins:
      allWinningNums = '/'.join(["/core/apps/Dill", latestSilo])
      finalWinings = dict()
      with open(allWinningNums, 'rb') as fp:

        fResults = pickle.load(fp)
        finalWinings[3] = match(fResults, win, 3)
        finalWinings[4] = match(fResults, win, 4)
        finalWinings[5] = match(fResults, win, 5)

        print("Current winnings are for matched\n3 numbers = {}\n4 numbers = {}\n5 numbers = {}".
              format(pay3[3], pay4[4],pay5[5]))

        for whatMatch, aResults in finalWinings.items():
          print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
          print("{} matched {} times in combination {}".format(whatMatch, len(aResults), latestSilo))
          print("\nMatched {} numbers\n".format(whatMatch))
          if whatMatch == 3:
            indexThree.append({latestSilo:len(aResults)})
          elif whatMatch == 4:
            indexFour.append({latestSilo: len(aResults)})
          elif whatMatch == 5:
            indexFive.append({latestSilo: len(aResults)})

          for res in aResults:
            pRes = res[0]
            print("{} | matchIndex = {} | Matched Numbers: {} |  Results: {}\n".format(whatMatch * '*', pRes[0],
                             pRes[1], pRes[2]))
          print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
          if whatMatch in pay3.keys():
            pay = pay3[whatMatch]
          elif  whatMatch in pay4.keys():
            pay = pay4[whatMatch]
          elif whatMatch in pay5.keys():
            pay = pay5[whatMatch]

          print("Playing all {} games wil cost you ${} and you would win ${} for {} ({}) number matches".format(
            len(fResults), len(fResults), len(aResults) * pay, len(aResults), whatMatch))
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


        # try:
        #   print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        #   print("\n\nWinning numbers:\n")
        #   for ww in range(10):
        #     r = random.randint(1, len(fResults))
        #     print("{} ->Sequence: {} index number is: {}".format(sorted(fResults[r]), ww ,r))
        #   print("-------------------------------------------------------------------")
        #   print("-------------------------------------------------------------------")
        #   print("-------------------------------------------------------------------")
        # except:
        #   pass

      iThree = copy.deepcopy(indexThree)
      iFour = copy.deepcopy(indexFour)
      iFive = copy.deepcopy(indexFive)
      mainIndex[str(win)[1:-1]] = {'3': iThree, '4':iFour,'5':iFive}
      # print("------------------------------------------------------------------------")
      # print("All wining numbers {} are:\n".format(len(fResults)))
      # for result in fResults:
      #   print(result)
      # print("------------------------------------------------------------------------")
  silos = list()
  origins = list()
  origin = list()
  for kk, vv in mainIndex.items():
    origin = list()
    print("\n#################################################################")
    print("winning game {}".format(kk))
    for hit, lDict in vv.items():
      if int(hit) == 5:
        hits, silo = analize("Five", lDict)
      elif int(hit) == 4:
        hits, silo = analize("Four", lDict)
      elif int(hit) == 3:
        hits, silo = analize("Three", lDict)
      if hits != 0:
        origin.append(silo)

      dOrigin = copy.deepcopy(origin)
    origins.append(dOrigin)
    print("#################################################################\n")

  # for gg in range(0, 500):
  #   silos.append( 'awn' + str(gg))
  #
  # final = predict(origins, silos)
  # print(final)
  # for el in final:
  #   print("choose numbers from {} silo".format(max(set(el), key = el.count)))



if __name__ == "__main__":
  main()
  sys.exit(0)
