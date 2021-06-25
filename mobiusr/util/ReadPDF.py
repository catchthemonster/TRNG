# title           :ReadPDF
# description     :TRNG
# author          :Sasha Kacanski
# date            :6/22/20
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
# ==============================================================================
import fitz, re
import sys
from collections import OrderedDict as od

class pdfManipulation(object):
  """
  PDF reader
  """

  def __init__(self, f):
    self.f = f
    self.pdf = fitz.open(self.f)


  def extractText(self):
    mPages = len(self.pdf)
    pages = od()
    ii = 0
    for page in self.pdf:
      txt = page.getText()
      pages[ii] = txt
      ii += 1

    return pages

if __name__ == '__main__':
    filePath = '/home/sasha/Downloads/cash5/cash5.pdf'
    out = '/home/sasha/Development/PYEXP/TRNG/input/cash5'
    pdfM = pdfManipulation(filePath)
    pages = pdfM.extractText()

    finalList= list()
    for k,v in pages.items():
      a = list()
      print("{}: {}".format(k,v))
      l = re.findall('\n\d\d\s\d\d\s\d\d\s\d\d\s\d\d', v)
      for el in l:
        el = el.strip('\n')
        a.append(el)
        finalList.append(a)

    print(finalList)

    with open(out, 'w') as w:
      for l in finalList:
        for el in l:
          w.write(el + '\n')
