
# title           :test
# description     :TRNG
# author          :Sasha Kacanski
# date            :8/25/20
# version         :0.0.1
# usage           :
# notes           :
# python_version  :3.6.3
# ==============================================================================
from cpt.cpt import Cpt
model = Cpt(0, 0.9, 10)

model.fit([[1,2,3,4,5],
[1,2,3,4,5],
[1,2,3,4,5],
[1,2,3,4,5],
[1,2,3,4,5],
[1,2,3,4,5]])

out = model.predict([[4, 20, 30, 32, 45],
[1, 3, 5, 31, 38],
[10, 15, 20, 36, 41],
[22, 27, 31, 35, 39],
[19, 20, 25, 27, 37],
[9, 10, 29, 31, 45],
[3, 19, 20, 24, 42],
[1, 3, 10, 18, 43],
[1, 2, 10, 14, 29],
[12, 14, 18, 32, 38]])


print(out)